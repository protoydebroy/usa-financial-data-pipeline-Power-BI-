# Data Schema

The pipeline ingests daily files containing customer financial records. Each file follows the schema below — 27 columns. Real customer data is **not** committed to this repo for privacy reasons.

## Schema

| # | Column | Type | Description |
|---|---|---|---|
| 1 | ID | string | Record identifier (per-row) |
| 2 | Customer_ID | string | Unique customer identifier (e.g. `CUS_0xd40`) |
| 3 | Month | string | Reporting month (text: January, February, etc.) |
| 4 | Name | string | Customer name |
| 5 | Age | numeric | Customer age (some values may be imputed) |
| 6 | SSN | string | Social Security Number (masked in production) |
| 7 | Occupation | string | Customer occupation |
| 8 | Annual_Income | numeric | Annual income in USD |
| 9 | Monthly_In-hand_Salary | numeric | Net monthly take-home pay |
| 10 | Num_Bank_Accounts | numeric | Number of bank accounts held |
| 11 | Num_Credit_Card | numeric | Number of credit cards held |
| 12 | Interest_Rate | numeric | Average interest rate on borrowing |
| 13 | Num_of_Loan | numeric | Number of active loans |
| 14 | Type_of_Loan | string | Comma-separated list of loan types |
| 15 | Delay_from_due_date | numeric | Average days late on payments |
| 16 | Num_of_Delayed_Payment | numeric | Count of delayed payments |
| 17 | Changed_Credit_Limit | numeric | % change in credit limit |
| 18 | Num of Credit Inqueries | numeric* | Number of credit inquiries (*may contain "Data Missing") |
| 19 | Credit_Mix | categorical | Good / Above Standard / Standard / Bad |
| 20 | Outstanding_Debt | numeric | Total outstanding debt in USD |
| 21 | Credit_Utilization_Ratio | numeric | Credit utilization percentage (0–100) |
| 22 | Credit_History_Age | string | Free-text e.g. "22 Years and 9 Months" |
| 23 | Payment_of_Min_Amount | string | Yes / No |
| 24 | Total_EMI_per_month | numeric | Total monthly EMI obligations |
| 25 | Amount_invested_monthly | numeric* | Monthly investment amount (*may contain "Data Missing") |
| 26 | Payment_Behaviour | categorical | Compound category, see below |
| 27 | Monthly_Balance | numeric | End-of-month balance |
| 28 | Credit_Score | string | Customer's overall credit score classification |

## Payment_Behaviour values

The raw column contains 7 categories with verbose names. They are renamed in Power Query for readability.

| Raw value | Renamed in Power Query |
|---|---|
| High_spent_Large_value_payments | High / Large |
| High_spent_Medium_value_payments | High / Medium |
| High_spent_Small_value_payments | High / Small |
| Low_spent_Large_value_payments | Low / Large |
| Low_spent_Medium_value_payments | Low / Medium |
| Low_spent_Small_value_payments | Low / Small |
| Data Missing | Unknown |

## Known data quality issues

Identified and handled during the build:

1. **Age 34 over-represented** — 696 records vs ~370 average for surrounding ages. Almost certainly a median-fill imputation upstream. Filtered out of the age distribution histogram on Page 1.

2. **`Num of Credit Inqueries` contains text** — some rows have "Data Missing" instead of a number. DAX measures wrap conversions in `NOT(ISERROR(VALUE(...)))` to handle this without errors.

3. **`Amount_invested_monthly` contains text** — same issue as above. Same wrapper pattern used in the LTV calculation.

4. **`Age` column has trailing underscores** — values like `24_` in some rows. Cleaned in Power Query with text trimming.

5. **`Occupation` column has placeholder values** — values like `_______` (underscore strings) for missing occupations. Treated as null in Power Query.

## Dataset volume

- **Total rows:** 12,000
- **Distinct customers:** 3,000
- **Distinct months:** 4 (varies)
- **Records per customer:** 4 on average (one per month per customer)
