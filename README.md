# USA Financial Data Pipeline & Dashboard

End-to-end automated data pipeline that ingests daily financial reports from 25 field agents via email, processes them through cloud services, and surfaces insights through a 4-page interactive Power BI dashboard. Eliminated ~$144K/year in manual processing costs and reduced report turnaround from 5 hours to 30 minutes.

![Dashboard preview](docs/dashboard-page1-profile.png)

## The problem

A financial analytics firm received ~25 attachments daily from field agents across the US. The manual workflow — download from email, combine files, clean data, build dashboard — took 5 hours per day, required two dedicated employees ($12K/month), and produced frequent errors that delayed insight delivery to the client.

## The solution

A four-stage pipeline that runs unattended:

![Architecture](docs/architecture.png)

1. **Outlook** receives mails. A rule routes attachments matching the keyword to a dedicated folder.
2. **Power Automate** monitors the folder, extracts attachments, and writes each one to Google Drive.
3. **Google Cloud service account** authorizes programmatic Drive access via the Drive API.
4. **Power BI** ingests the files via a Python script, combines them with pandas, and powers the dashboard.

## Tech stack

- **Microsoft Outlook** — entry point, rule-based mail routing
- **Microsoft Power Automate** — no-code workflow orchestration
- **Google Drive** — intermediate cloud storage
- **Google Cloud Console** — service account, IAM, Drive API
- **Python** — `google-auth`, `google-api-python-client`, `pandas`, `requests`
- **Power BI Desktop** — DAX measures, Power Query, custom theme
- **Power BI Python connector** — bridges Drive API output into the model

## Dashboard

Four pages, each answering a distinct business question:

| Page | Question answered |
|---|---|
| Profile | Who are our customers and how do they manage credit? |
| Customers | Which segments are potential customers for new products? |
| Portfolio | Which products are most popular and how do holdings change with age? |
| Insights | What are the key takeaways and recommended actions? |

### Page 1 — Customer profile and credit behavior
![Profile](docs/dashboard-page1-profile.png)

### Page 2 — Customer value
![Customers](docs/dashboard-page2-customers.png)

### Page 3 — Promotions and loan portfolio
![Portfolio](docs/dashboard-page3-portfolio.png)

### Page 4 — Insights and recommendations
![Insights](docs/dashboard-page4-insights.png)

## Key DAX work

- **LTV Score calculation** with bucketed promotion tiers (Premium, Mid, Entry) using SWITCH and FILTER patterns
- **Threshold-based credit inquiry analysis** with conditional bar coloring driven by a measure
- **Rolling-window smoothing** on age-binned trend lines using context-manipulation DAX
- **Data quality wrappers** to handle non-numeric values (`Data Missing`) inline using `NOT(ISERROR(VALUE()))` patterns
- **Sort-by-column setup** for credit mix and age groups, with circular dependency resolved via Power Query

Full DAX library: [`powerbi/measures.dax`](powerbi/measures.dax)

## Data

- **Volume:** 12,000 records, 3,000 customers
- **Fields:** 27 attributes per record (demographics, credit history, payment behavior, loan portfolio)
- **Source:** Daily CSV/XLSX files from field agents (data not committed for privacy)
- **Schema:** [`data/sample_data_schema.md`](data/sample_data_schema.md)

## Insights surfaced

1. Customers aged 14–25 are the credit acquisition segment, averaging 10.2+ credit inquiries
2. Credit limit growth declines 52% from younger to older customers
3. Standard credit mix segment (1,127 customers) shows no clear behavioral pattern
4. 412 customers qualify for the premium LTV promotion tier (LTV > $80K)
5. Loan portfolio is well-diversified across 9 product types

Page 4 of the dashboard contains the full written analysis.

## Repository structure

```
.
├── docs/                  Architecture and dashboard screenshots
├── pipeline/              Step-by-step setup guides for each stage
├── scripts/               Python ingestion script
├── powerbi/               DAX measures and data model documentation
└── data/                  Schema documentation (no real data)
```

## Recreating this pipeline

If you want to set up a similar pipeline:

1. Outlook rule setup → [`pipeline/outlook_rule_config.md`](pipeline/outlook_rule_config.md)
2. Power Automate flow → [`pipeline/power_automate_flow.md`](pipeline/power_automate_flow.md)
3. Google Cloud service account → [`pipeline/google_cloud_setup.md`](pipeline/google_cloud_setup.md)
4. Python ingestion script → [`scripts/drive_to_powerbi.py`](scripts/drive_to_powerbi.py)

## Challenges solved during the build

- **Imputation bias detection:** Identified that age 34 was over-represented by 90% vs surrounding ages (696 records vs ~370 average), indicating median-fill of missing values upstream. Filtered affected records from demographic visualizations.
- **Circular dependency in DAX sort-by-column:** Resolved by moving order columns from calculated columns to Power Query custom columns.
- **Non-numeric values in numeric columns:** Wrapped affected DAX measures in error-tolerant patterns; later cleaned at the Power Query layer for performance.

## License

MIT — see [LICENSE](LICENSE)

## Contact

Built by **Protoy Debroy**

If you want to discuss this project or related work, reach out via [LinkedIn](#) or email.
