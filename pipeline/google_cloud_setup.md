# Google Cloud Service Account Setup

Power BI cannot read Google Drive directly. This guide creates a Google Cloud service account — a non-human identity that the Python ingestion script uses to authenticate against the Google Drive API.

## Step 1 — Open Google Cloud Console

Go to [console.cloud.google.com](https://console.cloud.google.com).

## Step 2 — Create a new project

1. From the project picker (top left), click **New Project**
2. Project name: `Drive Bridge financial Data` (or any descriptive name)
3. Click **Create**
4. Once provisioned, switch into the project

## Step 3 — Enable the Google Drive API

1. Navigate to **APIs & Services** → **Library**
2. Search for `Google Drive API`
3. Click **Enable**

## Step 4 — Create the service account

1. Navigate to **APIs & Services** → **Credentials**
2. Click **+ Create credentials** → **Service account**
3. Service account name: `Financial Project`
4. Click **Create and Continue**, accept default roles, and finish

## Step 5 — Generate a JSON key

1. Click on the new service account from the list
2. Go to the **Keys** tab → **Add key** → **Create new key**
3. Key type: **JSON**
4. Click **Create**

A `.json` file will download to your computer. **Store this file securely.** It contains a private key that grants access to your Google Drive.

> ⚠️ **NEVER commit this file to source control.** The `.gitignore` in this repo blocks it by default, but always double-check before pushing.

## Step 6 — Share the Drive folder with the service account

This is the step most people forget.

1. Open the JSON key file in a text editor
2. Find the `client_email` field — it ends with `@<project>.iam.gserviceaccount.com`
3. Copy that email address
4. In Google Drive, right-click the destination folder (`Financial Project` in this guide) → **Share**
5. Paste the service account email and set access to **Viewer**
6. Click **Share**

Without this step, the Python script will get a `404 Not Found` or `403 Forbidden` error when it tries to list the folder's contents.

## Step 7 — Find the folder ID

The Python script needs the Google Drive folder ID to know what to read. To get it:

1. Open the Drive folder in your browser
2. Look at the URL: `https://drive.google.com/drive/folders/15UYA2eHZpuVPtGsmmJ0b5g4UGEXjRZaG`
3. The ID is the last segment after `/folders/`

Copy this ID into the `FOLDER_ID` constant in `scripts/drive_to_powerbi.py`.

## Security checklist

- [ ] JSON key is stored outside the repository folder
- [ ] `.gitignore` is in place and includes `*.json`
- [ ] Service account has **Viewer** access only (not Editor or Owner)
- [ ] No other accounts have unnecessary access to the Drive folder
- [ ] Service account email is documented in your project notes for future reference
