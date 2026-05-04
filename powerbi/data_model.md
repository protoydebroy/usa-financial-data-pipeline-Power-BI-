# Power BI Data Model

## Tables

The model uses three tables in a star schema centered on `combined_df` (the fact table).

### combined_df (fact table)

Loaded via the Python connector from Google Drive. Contains 12,000 rows × 27 columns.

Key columns used in measures and visuals:
- `Customer_ID` — unique customer identifier
- `Age` — customer age (numeric)
- `Age Groups` — categorical bucket (Teen, Young Adult, Adult, Middle-Aged, Senior)
- `Annual_Income`, `Monthly_Balance`, `Monthly_In-hand_Salary`
- `Credit_Mix` — Good / Above Standard / Standard / Bad
- `Credit_Utilization_Ratio` (numeric, 0–100)
- `Delay_from_due_date`, `Num of Credit Inqueries`
- `Changed_Credit_Limit` — used for credit limit trend chart
- `Num_of_Loan`, `Num_Credit_Card` — used for product-holding chart
- `Payment_Behaviour` — categorical (renamed from raw values to short forms)
- `Amount_invested_monthly`

Helper columns added in Power Query:
- `Credit Mix Order` (1–4) — for sort-by-column on Credit_Mix
- `Age Group Order` (1–5) — for sort-by-column on Age Groups

### LoanTypeTable (dimension)

Loan-type dimension, one row per customer-loan combination. Used for the loan portfolio chart on Page 3.

Columns: `Customer_ID`, `LoanType`

### DateTable (date dimension)

Generated via `CALENDAR()`. Required for proper time-intelligence DAX.

Columns: `Date`, `Year`, `MonthNumber`, `MonthName`

Marked as a date table via Modeling → Mark as date table → Date column.

## Relationships

| From | To | Type | Direction |
|---|---|---|---|
| DateTable[Date] | combined_df[Date] | One-to-many | Single |
| LoanTypeTable[Customer_ID] | combined_df[Customer_ID] | Many-to-many or one-to-many | Single |

The DateTable relationship is the foundation for all time-intelligence functions (DATEADD, LASTDATE, etc.), even though the current dataset only spans a few months.

## Custom theme

Applied via View → Themes → Browse for themes. Sets:
- Page background: `#F1F1EE` (warm off-white)
- Visual background: `#FFFFFF` (pure white)
- Primary data color: `#1F4E79` (deep navy)
- Accent: `#D97706` (amber, used for callouts and warnings)
- Positive: `#0F766E` (teal)
- Negative: `#B91C1C` (deep red)
- Slate gray scale (4 shades) for secondary categorical data

## Power Query transformations

Applied in the Transform Data editor:

1. **Payment_Behaviour rename:** Long category names like `High_spent_Large_value_payments` replaced with `High / Large` for legend readability.

2. **Credit Mix Order column:** Added via Conditional Column to enable sort-by-column without circular dependency in DAX.

3. **Age Group Order column:** Same pattern as above for Age Groups.

4. **Numeric type enforcement:** Columns like `Num of Credit Inqueries` and `Amount_invested_monthly` cleaned to numeric where possible. Rows with `Data Missing` text become null, which DAX AVERAGE skips automatically.

## Filter strategy by page

| Page | Slicers active | Notes |
|---|---|---|
| Profile | Yes | All four slicers filter all visuals |
| Customers | Yes | Same slicer set as Profile |
| Portfolio | Yes | Same slicer set |
| Insights | No | Slicers removed — page contains static written analysis |

The credit limit trend chart on Profile uses **Edit interactions** to ignore slicers, because its peak/trough annotations are static. This is a deliberate design pattern: a "context visual" that maintains a full-population baseline while the rest of the page responds to filters.
