# Documentation assets

This folder holds the architecture diagram and dashboard screenshots that the README references.

## Required files

To make the README render correctly on GitHub, this folder needs:

- `architecture.png` — the pipeline flowchart (Outlook → Power Automate → Google Drive → Power BI)
- `dashboard-page1-profile.png` — Profile page screenshot
- `dashboard-page2-customers.png` — Customers page screenshot
- `dashboard-page3-portfolio.png` — Portfolio page screenshot
- `dashboard-page4-insights.png` — Insights page screenshot
- `dashboard-page5-recommendations.png` — Recommendations page screenshot

## How to capture clean screenshots

1. Open the `.pbix` file in Power BI Desktop.
2. Maximize the window so the dashboard fills the screen at native resolution.
3. Click the page tab you want to capture.
4. Press **Win + Shift + S** to open the Snipping Tool.
5. Drag a rectangle around the dashboard area (exclude the Power BI ribbon and tab strip).
6. Save as PNG (not JPEG — PNG is lossless and looks better on GitHub).

## How to capture the architecture diagram

The flowchart was originally generated as an interactive SVG. To save it as a PNG:

1. Right-click the diagram in your chat.
2. Save image as → `architecture.png`.
3. Drop it in this folder.

Alternatively, recreate it using draw.io, Lucidchart, or Excalidraw with the same five stages.
