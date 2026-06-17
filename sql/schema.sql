-- schema.sql
-- Star Schema for Mutual Fund Analytics
-- Target Database: SQLite

-- 1. Dimension Tables

-- dim_fund: Contains descriptive attributes of each mutual fund scheme
CREATE TABLE dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    amc TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT,
    expense_ratio REAL,
    benchmark TEXT,
    fund_manager TEXT
);

-- dim_date: Date dimension for time-series analysis
CREATE TABLE dim_date (
    date_id TEXT PRIMARY KEY, -- Formatted as 'YYYY-MM-DD'
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    week INTEGER NOT NULL
);

-- 2. Fact Tables

-- fact_nav: Daily Net Asset Value and daily returns
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER NOT NULL,
    nav_date TEXT NOT NULL,
    nav_value REAL NOT NULL,
    daily_return REAL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (nav_date) REFERENCES dim_date(date_id)
);

-- fact_transactions: Investor transaction records
CREATE TABLE fact_transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT NOT NULL,
    scheme_code INTEGER NOT NULL,
    txn_date TEXT NOT NULL,
    amount REAL NOT NULL,
    txn_type TEXT CHECK(txn_type IN ('SIP', 'Lumpsum', 'Redemption')),
    state TEXT,
    city_tier TEXT,
    age_group TEXT,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (txn_date) REFERENCES dim_date(date_id)
);

-- fact_aum: Assets Under Management by Fund House
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amc_name TEXT NOT NULL,
    quarter_date TEXT NOT NULL,
    aum_crores REAL NOT NULL,
    FOREIGN KEY (quarter_date) REFERENCES dim_date(date_id)
);

-- fact_performance: Performance and Risk metrics for each scheme
CREATE TABLE fact_performance (
    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER NOT NULL,
    sharpe REAL,
    sortino REAL,
    alpha REAL,
    beta REAL,
    max_drawdown REAL,
    cagr_1yr REAL,
    cagr_3yr REAL,
    cagr_5yr REAL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

-- 3. Indexes for Optimization

-- Indexes for dim_fund
CREATE INDEX idx_fund_amc ON dim_fund(amc);
CREATE INDEX idx_fund_category ON dim_fund(category);

-- Indexes for fact_nav
CREATE INDEX idx_nav_scheme_date ON fact_nav(scheme_code, nav_date);

-- Indexes for fact_transactions
CREATE INDEX idx_txn_investor ON fact_transactions(investor_id);
CREATE INDEX idx_txn_scheme_date ON fact_transactions(scheme_code, txn_date);
CREATE INDEX idx_txn_state ON fact_transactions(state);

-- Indexes for fact_aum
CREATE INDEX idx_aum_amc_date ON fact_aum(amc_name, quarter_date);

-- Indexes for fact_performance
CREATE INDEX idx_perf_scheme ON fact_performance(scheme_code);
