# Bluestock MF Analytics Platform
### Mutual Fund Analytics Capstone — Bluestock Fintech Pvt. Ltd.


An end-to-end **data engineering and analytics platform** for the Indian Mutual Fund industry, built on real public data from **AMFI India** and **mfapi.in**. Covers the complete pipeline from raw ingestion through a Python ETL pipeline, normalised SQLite star schema, advanced risk analytics, and an interactive 4-page Power BI dashboard.

---

## Project Highlights

| Metric | Value |
|--------|-------|
| Datasets | 10 files from AMFI India and mfapi.in |
| NAV Records | 46,000+ daily records (Jan 2022 – May 2026) |
| Fund Schemes | 40 schemes across 10 AMCs |
| Investor Transactions | 32,778 records · 5,000 investors · 12 states |
| Peak SIP Inflow | Rs.31,002 Crore (Dec 2025) |
| SBI AUM | Rs.12.5 Lakh Crore (No.1 AMC) |
| Industry Folios | 26.12 Crore (Dec 2025) |

---

## Project Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/                          ← 10 original AMFI CSVs + 6 live NAV CSVs
│   ├── processed/                    ← Cleaned CSVs for Power BI and analysis
│   └── db/                           ← bluestock_mf.db (SQLite, gitignored)
├── notebooks/
│   ├── eda_notebook.ipynb            ← 15+ EDA charts
│   ├── performance_analytics.ipynb   ← Sharpe, Sortino, Alpha, Beta, VaR, Scorecard
│   └── advanced_analytics.ipynb     ← VaR/CVaR, cohorts, HHI, SIP continuity
├── scripts/
│   ├── etl_pipeline.py               ← Master ETL pipeline (run this first)
│   ├── live_nav_fetch.py             ← Fetches live NAV from mfapi.in
│   └── recommender.py               ← Fund recommender by risk appetite
├── sql/
│   ├── schema.sql                    ← Star schema DDL
│   └── queries.sql                   ← 10 analytical SQL queries
├── reports/
│   ├── Bluestock_MF_Final_Report.docx
│   ├── Bluestock_MF_Presentation.pptx
│   ├── page1_industry_overview.png
│   ├── page2_fund_performance.png
│   ├── page3_investor_analytics.png
│   └── page4_sip_market_trends.png
├── mutual_funds_analytics.pbix       ← Power BI dashboard (4 pages)
├── mutual_funds_analytics.pdf        ← Exported dashboard PDF
├── data_dictionary.md                ← Column definitions for all 6 tables
├── requirements.txt
└── README.md
```

---

## Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/423130/bluestock_mf_capstone.git
cd bluestock_mf_capstone
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Add raw data files
Place all 10 CSV files into `data/raw/`:
```
01_fund_master.csv
02_nav_history.csv
03_aum_by_fund_house.csv
04_monthly_sip_inflows.csv
05_category_inflows.csv
06_industry_folio_count.csv
07_scheme_performance.csv
08_investor_transactions.csv
09_portfolio_holdings.csv
10_benchmark_indices.csv
```

### 4. Run the ETL pipeline
```bash
python etl_pipeline.py
```
This will:
- Load and clean all 10 datasets
- Create `data/db/bluestock_mf.db` with 6 star schema tables
- Export processed CSVs to `data/processed/`

### 5. Fetch live NAV data
```bash
python live_nav_fetch.py
```
Fetches real-time NAV for 6 key schemes from mfapi.in and saves to `data/raw/`.

### 6. Run the notebooks
Open Jupyter Lab and run in this order:
```bash
jupyter lab
```
1. `notebooks/eda_notebook.ipynb`
2. `notebooks/performance_analytics.ipynb`
3. `notebooks/advanced_analytics.ipynb`

### 7. Get fund recommendations
```bash
python recommender.py
```
Enter your risk appetite (Low / Moderate / High) and get the top 3 fund recommendations ranked by Sharpe ratio.

### 8. Open the Power BI Dashboard
Open `mutual_funds_analytics.pbix` in Power BI Desktop. Data is pre-connected to `data/processed/` CSVs.

---

## Database Schema

The database follows a normalised star schema with 6 tables:

| Table | Rows | Description |
|-------|------|-------------|
| dim_fund | 40 | Master attributes: scheme code, name, AMC, category, risk grade, expense ratio |
| dim_date | 1,297 | Date dimension for time-series slicing |
| fact_nav | 46,000 | Daily NAV values and computed daily returns |
| fact_transactions | 32,778 | SIP, Lumpsum, and Redemption investor activity |
| fact_aum | 90 | Quarterly AUM per AMC in crores |
| fact_performance | 40 | Pre-computed Sharpe, Sortino, Alpha, Beta, CAGR, Max Drawdown |

See `data_dictionary.md` for full column-level documentation.

---

## Deliverables

| ID | Deliverable | File | Weight |
|----|-------------|------|--------|
| D1 | ETL pipeline | `etl_pipeline.py`, `live_nav_fetch.py` | 15% |
| D2 | SQLite database | `schema.sql`, `queries.sql`, `data_dictionary.md` | 10% |
| D3 | EDA notebook | `notebooks/eda_notebook.ipynb` | 15% |
| D4 | Performance metrics | `notebooks/performance_analytics.ipynb`, `fund_scorecard.csv`, `alpha_beta.csv` | 15% |
| D5 | Interactive dashboard | `mutual_funds_analytics.pbix`, dashboard PDF + 4 PNGs | 20% |
| D6 | Advanced analytics | `notebooks/advanced_analytics.ipynb`, `var_cvar_report.csv`, `recommender.py` | 10% |
| D7 | Report and slides | `Final_Report.docx`, `Presentation.pptx` | 15% |

---

## Performance Metrics

| Metric | Formula |
|--------|---------|
| Sharpe Ratio | (Rp - Rf) / sigma x sqrt(252), Rf = 6.5% |
| Sortino Ratio | (Rp - Rf) / sigma_downside x sqrt(252) |
| Alpha | OLS intercept x 252 vs Nifty 100 |
| Beta | OLS slope vs Nifty 100 daily returns |
| Max Drawdown | min(NAV / running_max - 1) |
| VaR (95%) | 5th percentile of daily return distribution |
| CVaR | Mean of returns below VaR threshold |

### Fund Scorecard (0-100)
```
Score = 30% x 3yr CAGR rank
      + 25% x Sharpe rank
      + 20% x Alpha rank
      + 15% x Expense ratio rank (inverse)
      + 10% x Max Drawdown rank (inverse)
```

---

## Power BI Dashboard Pages

| Page | Visuals | Slicers |
|------|---------|---------|
| Industry Overview | AUM KPI cards, SIP trend line, AUM by AMC bar chart | Category, Fund House |
| Fund Performance | Scatter plot (return vs Sharpe), scorecard table, drawdown bar | Category, Risk Grade |
| Investor Analytics | State bar, SIP/Lumpsum/Redemption donut, age group columns, transaction timeline | State, City Tier |
| SIP and Market Trends | SIP inflow trend, category inflows, benchmark comparison line | Month, Category |

---

## Analytical SQL Queries

The `sql/queries.sql` file contains 10 ready-to-run queries:

1. Top 5 funds by AUM
2. Average NAV per month per scheme
3. SIP year-over-year growth
4. Transactions by state
5. Funds with expense ratio below 1%
6. Top funds by Sharpe ratio
7. Highest alpha funds (benchmark beaters)
8. Monthly transaction volume trend
9. Top states by SIP investment amount
10. Most resilient funds by lowest max drawdown

---

## Data Sources

| Source | URL | Usage |
|--------|-----|-------|
| AMFI India | amfiindia.com | AUM, SIP inflows, folio count, scheme master |
| mfapi.in | mfapi.in | Daily NAV history for all schemes |
| NSE/BSE | Public indices | Nifty 50, Nifty 100, Nifty Midcap 150, BSE SmallCap |

All sources are free and publicly accessible — no API keys required.

---

## Tech Stack

```
Python 3.11    pandas       numpy        matplotlib   seaborn
plotly         scipy        sqlalchemy   sqlite3      requests
jupyter        openpyxl     Power BI Desktop
```

---

## AMCs Covered

SBI MF · HDFC MF · ICICI Prudential · Nippon India · Kotak · Axis · Aditya Birla Sun Life · UTI · Mirae Asset · DSP MF

---

## Future Scope

- **B1** — Cron job scheduling ETL to auto-fetch NAV from mfapi.in every weekday at 8 PM
- **B2** — Streamlit web app as a retail investor-facing alternative to Power BI
- **B3** — Monte Carlo simulation projecting NAV growth over 5 years with uncertainty bands
- **B4** — Markowitz Efficient Frontier portfolio optimisation for 5 selected funds
- **B5** — Automated weekly HTML email report generator with performance summaries

---

*Bluestock Fintech Pvt. Ltd. · Capstone Project · June 2026 · Data from AMFI India, mfapi.in, and NSE/BSE public records*
