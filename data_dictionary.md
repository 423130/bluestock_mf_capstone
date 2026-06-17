# Bluestock Mutual Fund Platform: Data Dictionary

This document provides a detailed definition of the data model used in the Bluestock Mutual Fund Analytics Platform. The schema follows a **Star Schema** architecture optimized for financial analytics.

---

## Table: dim_fund
**Description:** Master table containing descriptive attributes of each mutual fund scheme.

| Column Name | Data Type | Business Definition | Example Value | Source File |
| :--- | :--- | :--- | :--- | :--- |
| scheme_code | INTEGER | Unique AMFI identifier for the mutual fund scheme (Primary Key). | 119551 | 01_fund_master.csv |
| name | TEXT | Full official name of the mutual fund scheme. | SBI Bluechip Fund - Growth | 01_fund_master.csv |
| amc | TEXT | Asset Management Company (Fund House) managing the scheme. | SBI Mutual Fund | 01_fund_master.csv |
| category | TEXT | Broad classification of the fund (e.g., Equity, Debt, Hybrid). | Equity | 01_fund_master.csv |
| sub_category | TEXT | Specific investment style or market cap focus. | Large Cap | 01_fund_master.csv |
| risk_grade | TEXT | Risk classification as per SEBI risk-o-meter. | Very High | 01_fund_master.csv |
| expense_ratio | REAL | Annual fee charged by the fund to manage assets (in %). | 1.54 | 01_fund_master.csv |
| benchmark | TEXT | The index against which the fund's performance is measured. | NIFTY 100 TRI | 01_fund_master.csv |
| fund_manager | TEXT | Name of the lead portfolio manager. | Sohini Andani | 01_fund_master.csv |

---

## Table: dim_date
**Description:** Temporal dimension table for time-series analysis and slicing.

| Column Name | Data Type | Business Definition | Example Value | Source |
| :--- | :--- | :--- | :--- | :--- |
| date_id | TEXT | Unique date identifier in YYYY-MM-DD format (Primary Key). | 2024-01-01 | Generated |
| date | DATE | The actual calendar date. | 2024-01-01 | Generated |
| year | INTEGER | The calendar year. | 2024 | Generated |
| quarter | INTEGER | The calendar quarter (1, 2, 3, or 4). | 1 | Generated |
| month | INTEGER | The month number (1 to 12). | 1 | Generated |
| month_name | TEXT | Full name of the month. | January | Generated |
| week | INTEGER | The ISO week number of the year. | 1 | Generated |

---

## Table: fact_nav
**Description:** Fact table containing daily Net Asset Value (NAV) records and daily returns.

| Column Name | Data Type | Business Definition | Example Value | Source File |
| :--- | :--- | :--- | :--- | :--- |
| nav_id | INTEGER | Auto-incrementing unique record identifier (Primary Key). | 4501 | ETL Output |
| scheme_code | INTEGER | Foreign Key linking to `dim_fund(scheme_code)`. | 119551 | 02_nav_history.csv |
| nav_date | TEXT | Foreign Key linking to `dim_date(date_id)`. | 2024-01-01 | 02_nav_history.csv |
| nav_value | REAL | The price per unit of the mutual fund on that date. | 54.38 | 02_nav_history.csv |
| daily_return | REAL | Percentage change in NAV from the previous trading day. | 0.0015 | ETL Calculated |

---

## Table: fact_transactions
**Description:** Fact table recording granular investor transaction activity.

| Column Name | Data Type | Business Definition | Example Value | Source File |
| :--- | :--- | :--- | :--- | :--- |
| txn_id | INTEGER | Auto-incrementing unique transaction ID (Primary Key). | 10234 | 08_investor_transactions.csv |
| investor_id | TEXT | Unique identifier for the individual investor. | INV003054 | 08_investor_transactions.csv |
| scheme_code | INTEGER | Foreign Key linking to `dim_fund(scheme_code)`. | 119551 | 08_investor_transactions.csv |
| txn_date | TEXT | Foreign Key linking to `dim_date(date_id)`. | 2024-01-01 | 08_investor_transactions.csv |
| amount | REAL | The value of the transaction in INR. | 5000.0 | 08_investor_transactions.csv |
| txn_type | TEXT | Type of movement (SIP, Lumpsum, or Redemption). | SIP | 08_investor_transactions.csv |
| state | TEXT | Indian state where the investor is registered. | Maharashtra | 08_investor_transactions.csv |
| city_tier | TEXT | Classification of the city (e.g., T30 for Top 30, B30 for Beyond 30). | T30 | 08_investor_transactions.csv |
| age_group | TEXT | Demographic age bracket of the investor. | 26-35 | 08_investor_transactions.csv |

---

## Table: fact_aum
**Description:** Periodic fact table containing Assets Under Management (AUM) by Fund House.

| Column Name | Data Type | Business Definition | Example Value | Source File |
| :--- | :--- | :--- | :--- | :--- |
| aum_id | INTEGER | Unique record identifier (Primary Key). | 88 | 03_aum_by_fund_house.csv |
| amc_name | TEXT | Name of the fund house. | HDFC Mutual Fund | 03_aum_by_fund_house.csv |
| quarter_date | TEXT | Date marking the end of the reporting quarter. | 2024-03-31 | 03_aum_by_fund_house.csv |
| aum_crores | REAL | Total assets managed by the AMC in Crore INR. | 435000.0 | 03_aum_by_fund_house.csv |

---

## Table: fact_performance
**Description:** Fact table containing pre-computed analytical and risk metrics for each scheme.

| Column Name | Data Type | Business Definition | Example Value | Source |
| :--- | :--- | :--- | :--- | :--- |
| perf_id | INTEGER | Unique record identifier (Primary Key). | 40 | ETL Output |
| scheme_code | INTEGER | Foreign Key linking to `dim_fund(scheme_code)`. | 119551 | dim_fund |
| sharpe | REAL | Reward-to-volatility ratio (Risk-adjusted return). | 0.88 | Calculated |
| sortino | REAL | Downside risk-adjusted return ratio. | 1.29 | Calculated |
| alpha | REAL | Excess return generated relative to the benchmark. | 0.87 | Calculated |
| beta | REAL | Sensitivity of the fund's returns to market movements. | 0.89 | Calculated |
| max_drawdown | REAL | Maximum peak-to-trough decline (in %). | -21.7 | Calculated |
| cagr_1yr | REAL | 1-Year Compounded Annual Growth Rate. | 0.124 | Calculated |
| cagr_3yr | REAL | 3-Year Compounded Annual Growth Rate. | 0.145 | Calculated |
| cagr_5yr | REAL | 5-Year Compounded Annual Growth Rate. | 0.152 | Calculated |
