# Outlook Rule Configuration

This guide describes how to set up the Outlook rule that automatically routes incoming financial data emails into a dedicated folder, which Power Automate then monitors.

## Step 1 — Create the destination folder

In the Outlook web app:

1. Right-click your mailbox in the left navigation pane.
2. Click **Create new folder**.
3. Name it `FinanceVault` (or any folder name you prefer — just make sure to update the Power Automate flow to match).

## Step 2 — Set up the rule

1. Click **Settings** (gear icon, top right) → **Mail** → **Rules**.
2. Click **Add new rule**.

Configure the rule as follows:

| Setting | Value |
|---|---|
| Rule name | Field Agent Data |
| Condition | Subject or body includes "Credit Score" |
| Action | Move to → FinanceVault |
| Stop processing more rules | Enabled |

3. Click **Save**.

## Step 3 — Test the rule

1. Send yourself a test email with the keyword `Credit Score` in the subject and a CSV attachment.
2. Within seconds, the email should appear in the `FinanceVault` folder rather than the inbox.

## Why a rule, not manual sorting

With ~25 field agents emailing daily, manual sorting would be slow and error-prone. The rule guarantees every matching mail lands in `FinanceVault` within seconds of arrival — which is the trigger point Power Automate needs.

## Adapting for your project

- Change the keyword (`Credit Score`) to whatever your project uses to identify relevant mails.
- Multiple keywords can be combined with OR conditions if your senders use different subject lines.
- Always enable **Stop processing more rules** so this rule doesn't conflict with others.
