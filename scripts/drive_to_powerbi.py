"""
USA Financial Data — Drive to Power BI Ingestion Script
=========================================================

Reads CSV, Excel, and Google Sheets files from a Google Drive folder
using a service account, combines them into a single pandas DataFrame,
and exposes the result for Power BI's Python connector to import.

Usage in Power BI Desktop:
    1. Get data → Python script
    2. Paste this entire script into the editor
    3. Update SERVICE_ACCOUNT_FILE and FOLDER_ID below
    4. Click OK — Power BI will detect the `combined_df` DataFrame

Dependencies (install via pip — see requirements.txt):
    google-auth
    google-auth-oauthlib
    google-auth-httplib2
    google-api-python-client
    pandas
    requests
    openpyxl
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import requests
from io import StringIO, BytesIO


# ============================================================
# CONFIG — update these two values for your environment
# ============================================================

# Path to the JSON key file downloaded from Google Cloud Console.
# This file authorizes the script to read your Drive folder.
SERVICE_ACCOUNT_FILE = r"C:\Users\<you>\Downloads\drive-bridge-financial-data-XXXX.json"

# Read-only access to Google Drive — minimum scope needed for this script.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Drive folder ID. Get this from the folder's URL after /folders/
# Example: https://drive.google.com/drive/folders/<this-part-here>
FOLDER_ID = "15UYA2eHZpuVPtGsmmJ0b5g4UGEXjRZaG"


# ============================================================
# AUTHENTICATION
# ============================================================

# Build credentials from the service account file.
# This reads the JSON key and authenticates using the scopes defined above.
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Initialize the Drive API v3 service. This is the entry point for
# all subsequent API calls.
service = build("drive", "v3", credentials=credentials)


# ============================================================
# FILE LISTING
# ============================================================

def list_files(service, folder_id):
    """List all files inside the specified Drive folder.

    Returns a list of dicts with keys: id, name, mimeType.
    """
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()
    return results.get("files", [])


# Fetch the file inventory from Drive
files = list_files(service, FOLDER_ID)


# ============================================================
# FILE READING — CSV, Excel, and Google Sheets
# ============================================================

# Each downloaded file becomes a DataFrame. We combine them at the end.
file_dataframes = []

for file in files:
    file_id = file["id"]
    file_name = file["name"]
    mime_type = file["mimeType"]

    # Pick the right URL pattern based on file type
    if mime_type == "application/vnd.google-apps.spreadsheet":
        # Google Sheets — export as CSV
        download_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    elif mime_type == "text/csv":
        # Plain CSV file
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Excel .xlsx file
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    else:
        # Skip anything that's not a spreadsheet
        continue

    # Download the file using the authenticated session is unnecessary here
    # because Drive's "uc?export=download" link is publicly accessible to the
    # service account. Plain requests.get works as long as the service account
    # has Viewer permission on the folder.
    response = requests.get(download_url)

    if response.status_code == 200:
        if mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # Excel needs binary handling
            df = pd.read_excel(BytesIO(response.content))
        else:
            # CSV and exported Sheets
            df = pd.read_csv(StringIO(response.content.decode("utf-8")))

        # Track the source file — useful for later debugging
        df["source_file"] = file_name
        file_dataframes.append(df)
    else:
        print(f"Error downloading file: {file_name} (HTTP {response.status_code})")


# ============================================================
# COMBINE
# ============================================================

# Concatenate all DataFrames into one. Power BI will pick this up as a table.
if file_dataframes:
    combined_df = pd.concat(file_dataframes, ignore_index=True)
else:
    # Fail loudly — empty data is usually a config issue
    raise RuntimeError(
        "No files were loaded. Check that:\n"
        "  1. SERVICE_ACCOUNT_FILE points to a valid JSON key\n"
        "  2. FOLDER_ID matches the Drive folder URL\n"
        "  3. The service account has Viewer access on the folder"
    )

# combined_df is now available to Power BI's Python connector.
# When Power BI evaluates this script, it offers all DataFrame variables
# in the Navigator pane. Select combined_df and click Load.
