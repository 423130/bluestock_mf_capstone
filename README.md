# 📊 Bluestock MF Analytics Platform
### Mutual Fund Analytics Capstone — Bluestock Fintech Pvt. Ltd.

An end-to-end **data engineering & analytics platform** for the Indian Mutual Fund industry, built on real public data from **AMFI India** and **mfapi.in**. Covers the full pipeline from raw ingestion → SQL star schema → advanced risk analytics → interactive Power BI dashboard.

---

## 🏆 Project Highlights

| Metric | Value |
|--------|-------|
| 📁 Datasets | 10 files (AMFI + mfapi.in) |
| 📈 NAV Records | 46,000+ daily records (Jan 2022 – May 2026) |
| 🏦 Fund Schemes | 40 schemes across 10 AMCs |
| 👥 Investor Transactions | 32,778 records · 5,000 investors · 12 states |
| 💰 Peak SIP Inflow | ₹31,002 Crore (Dec 2025) |
| 🏢 SBI AUM | ₹12.5 Lakh Crore (#1 AMC) |
| 📊 Industry Folios | 26.12 Crore (Dec 2025) |

---

## 📁 Project Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/                        ← 10 original AMFI CSV files
│   ├── processed/                  ← Cleaned CSVs for Power BI
│   └── db/                         ← bluestock_mf.db (SQLite)
├── notebooks/
│   ├── eda_notebook.ipynb          ← 15+ EDA charts
│   ├── performance_analytics.ipynb ← Sharpe, Alpha, Beta, VaR
│   └── advanced_analytics.ipynb    ← VaR/CVaR, cohorts, HHI, recommender
├── scripts/
│   └── etl_pipeline.py             ← Automated ETL pipeline
├── sql/
│   └── schema.sql                  ← Star schema DDL
├── reports/
│   ├── Bluestock_MF_Final_Report.docx
│   └── Bluestock_MF_Presentation.pptx
├── mutual_funds_analytics.pbix     ← Power BI dashboard (4 pages)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

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
- `01_fund_master.csv`
- `02_nav_history.csv`
- `03_aum_by_fund_house.csv`
- `04_monthly_sip_inflows.csv`
- `05_category_inflows.csv`
- `06_industry_folio_count.csv`
- `07_scheme_performance.csv`
- `08_investor_transactions.csv`
- `09_portfolio_holdings.csv`
- `10_benchmark_indices.csv`

### 4. Run the ETL pipeline
```bash
python etl_pipeline.py
```
This will:
- Load and clean all 10 datasets
- Create `data/db/bluestock_mf.db` with 6 star schema tables
- Export processed CSVs to `data/processed/`

### 5. Open the notebooks
```bash
jupyter lab
```
Run notebooks in this order:
1. `notebooks/eda_notebook.ipynb`
2. `notebooks/performance_analytics.ipynb`
3. `notebooks/advanced_analytics.ipynb`

### 6. Open the Power BI Dashboard
Open `mutual_funds_analytics.pbix` in **Power BI Desktop**.
Data is pre-connected to `data/processed/` CSVs.

---

## 🗄️ Database Schema (Star Schema)

```
                    ┌─────────────┐
                    │  dim_fund   │
                    │  (40 rows)  │
                    └──────┬──────┘
                           │ scheme_code
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
   │  fact_nav   │  │fact_transact│  │fact_perform │
   │(46,000 rows)│  │(32,778 rows)│  │  (40 rows)  │
   └─────────────┘  └─────────────┘  └─────────────┘
          │
   ┌──────▼──────┐  ┌─────────────┐
   │  dim_date   │  │  fact_aum   │
   │(1,297 rows) │  │  (90 rows)  │
   └─────────────┘  └─────────────┘
```

---

## 📊 Key Deliverables

### ETL Pipeline (`etl_pipeline.py`)
- Extracts from AMFI CSVs + mfapi.in REST API
- Cleans NAV data (forward-fill missing days, parse dates, remove duplicates)
- Loads into SQLite using SQLAlchemy ORM
- Exports processed CSVs for Power BI

### EDA Notebook (15+ charts)
- NAV trend lines with 2023 bull run annotation
- AUM bar chart — SBI dominance at ₹12.5L Cr
- SIP inflow time-series — ₹31,002 Cr milestone
- Category inflow heatmap
- Investor age/gender/state demographics
- NAV return correlation matrix (10 funds)
- Folio count growth 13.26 Cr → 26.12 Cr

### Performance Analytics
| Metric | Formula |
|--------|---------|
| Sharpe Ratio | (Rp − Rf) / σ × √252, Rf = 6.5% |
| Sortino Ratio | (Rp − Rf) / σ_downside × √252 |
| Alpha | OLS intercept × 252 vs Nifty 100 |
| Beta | OLS slope vs Nifty 100 daily returns |
| Max Drawdown | min(NAV / running_max − 1) |
| VaR (95%) | 5th percentile of daily return distribution |

### Fund Scorecard (0–100)
```
Score = 30% × 3yr CAGR rank
      + 25% × Sharpe rank
      + 20% × Alpha rank
      + 15% × Expense ratio rank (inverse)
      + 10% × Max Drawdown rank (inverse)
```

### Power BI Dashboard (4 Pages)
| Page | Content |
|------|---------|
| Industry Overview | AUM KPIs, SIP trend, AUM by AMC, slicers |
| Fund Performance | Scatter plot, scorecard table, drawdown chart |
| Investor Analytics | State bar, donut, age group, transaction timeline |
| SIP & Market Trends | SIP trend, category inflows, benchmark comparison |

---

## 🔗 Data Sources

| Source | URL | Usage |
|--------|-----|-------|
| AMFI India | [amfiindia.com](https://www.amfiindia.com) | AUM, SIP, folio data |
| mfapi.in | [mfapi.in](https://www.mfapi.in) | Daily NAV history |
| NSE/BSE | Public indices | Nifty 50, Nifty 100, BSE SmallCap |

> All sources are **free and publicly accessible** — no API keys required.

---

## 🧰 Tech Stack

```
Python 3.11    pandas    numpy    matplotlib    seaborn
plotly         scipy     sqlalchemy    sqlite3    requests
jupyter        openpyxl  Power BI Desktop
```

---

## 📌 AMCs Covered

SBI MF · HDFC MF · ICICI Prudential · Nippon India · Kotak · Axis · Aditya Birla Sun Life · UTI · Mirae Asset · DSP MF

---

## 🚀 Future Scope

- **B1** — Cron job for real-time NAV polling from mfapi.in
- **B2** — Streamlit web app for retail investor access
- **B3** — Monte Carlo NAV projections (5-year, uncertainty bands)
- **B4** — Markowitz Efficient Frontier portfolio optimisation
- **B5** — Automated weekly HTML email performance reports

---

## 📄 Reports

- 📘 `reports/Bluestock_MF_Final_Report.docx` — 15-page professional report
- 📊 `reports/Bluestock_MF_Presentation.pptx` — 12-slide capstone presentation

---

*Bluestock Fintech Pvt. Ltd. · Capstone Project · June 2026 · Data from AMFI India, mfapi.in, NSE/BSE public records*
