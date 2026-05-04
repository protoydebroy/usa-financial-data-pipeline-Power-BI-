# Power Automate Flow Setup

This guide walks through building the automated cloud flow that connects Outlook to Google Drive, so attachments arriving in the `FinanceVault` folder are automatically copied to a Google Drive folder.

## Prerequisites

- Microsoft Power Automate account (free tier is sufficient)
- Outlook account with `FinanceVault` folder configured (see `outlook_rule_config.md`)
- Google account with a destination folder created in Drive (this guide uses `Financial Project`)

## Step 1 — Create the flow

1. Go to [make.powerautomate.com](https://make.powerautomate.com)
2. Click **My flows** → **+ New flow** → **Automated cloud flow**

## Step 2 — Configure the trigger

1. Name the flow (e.g. `FinanceVault Sync`)
2. In the trigger search, type `mail` and select **When a new email arrives (V2)** for Outlook.com
3. Click **Create**

## Step 3 — Authorize the Outlook connection

The trigger card initially shows "Invalid connection". Click it and sign in with the Outlook account that owns the `FinanceVault` folder.

## Step 4 — Configure trigger parameters

| Parameter | Value |
|---|---|
| Folder | FinanceVault |
| Include Attachments | Yes |
| Only with Attachments | Yes (recommended, under advanced parameters) |

## Step 5 — Add the Google Drive action

1. Click the **+** below the trigger → **Add an action**
2. Search for `drive` → select **Google Drive** → **Create file**
3. Sign in with the Google account that owns the destination Drive folder

## Step 6 — Configure Create File

Power Automate automatically wraps the Create File action inside a `For each` loop because each mail can carry multiple attachments. Map the parameters as follows:

| Parameter | Value |
|---|---|
| Folder Path | `/Financial Project` |
| File Name | `Attachments Name` (dynamic content from trigger) |
| File Content | `Attachments Content` (dynamic content from trigger) |

## Step 7 — Save and test

1. Click **Save**
2. Send a test email with an attachment to the Outlook mailbox
3. Within a minute, the file should appear inside the Google Drive folder
4. Power Automate's Run history will show every attachment processed

## Troubleshooting

**Flow doesn't trigger:** Verify the Outlook rule is moving mails into `FinanceVault`. Power Automate watches the folder, not the inbox.

**Files arrive empty:** The "Include Attachments" trigger setting must be set to Yes. Without it, Power Automate strips attachments.

**Permission errors:** Re-authorize both connections (Outlook and Google Drive) by clicking the flow's connection icons.

**Multiple files per mail not all uploading:** Confirm the Create File action is inside a `For each` loop iterating over `Attachments`. If it's not, delete the action and re-add it; Power Automate auto-generates the loop.
