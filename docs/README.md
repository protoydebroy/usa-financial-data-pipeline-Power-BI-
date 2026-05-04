# Documentation assets

This folder holds the architecture diagram and dashboard screenshots that the README references.

## Required files

To make the README render correctly on GitHub, this folder needs:

- `architecture.svg` — the pipeline flowchart (Outlook → Power Automate → Google Drive → Power BI). Vector format renders crisp at any zoom level
- `architecture.png` — high-res PNG fallback of the same diagram
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

## Architecture diagram source

The architecture diagram is included in this repo as both SVG (`architecture.svg`, vector) and PNG (`architecture.png`, 1440×2640 raster). The SVG is the source of truth — open it in any browser, Figma, or Inkscape to edit. The PNG is a rendered export for environments that don't display SVG.
