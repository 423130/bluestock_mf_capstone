-- queries.sql
-- Analytical SQL Queries for Bluestock Mutual Fund Platform
-- Database: SQLite

-- 1. Top 5 Funds by latest AUM
SELECT 
    f.name AS fund_name, 
    a.amc_name, 
    MAX(a.aum_crores) AS latest_aum_crores
FROM fact_aum a
JOIN dim_fund f ON a.amc_name = f.amc
GROUP BY f.name
ORDER BY latest_aum_crores DESC
LIMIT 5;

-- 2. Average NAV per month for each scheme (Time-series summary)
SELECT 
    f.name AS fund_name,
    d.year,
    d.month_name,
    AVG(n.nav_value) AS avg_monthly_nav
FROM fact_nav n
JOIN dim_fund f ON n.scheme_code = f.scheme_code
JOIN dim_date d ON n.nav_date = d.date_id
GROUP BY f.name, d.year, d.month
ORDER BY f.name, d.year, d.month;

-- 3. SIP Year-over-Year (YoY) Growth in Transaction Volume
WITH sip_annual AS (
    SELECT 
        d.year,
        COUNT(t.txn_id) AS sip_count,
        SUM(t.amount) AS total_sip_amount
    FROM fact_transactions t
    JOIN dim_date d ON t.txn_date = d.date_id
    WHERE t.txn_type = 'SIP'
    GROUP BY d.year
)
SELECT 
    curr.year,
    curr.sip_count,
    prev.sip_count AS prev_year_count,
    ROUND(((CAST(curr.sip_count AS REAL) - prev.sip_count) / prev.sip_count) * 100, 2) AS yoy_volume_growth_pct
FROM sip_annual curr
LEFT JOIN sip_annual prev ON curr.year = prev.year + 1
WHERE prev.year IS NOT NULL;

-- 4. Count of transactions by State
SELECT 
    state,
    COUNT(txn_id) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_invested
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- 5. Schemes with Expense Ratio less than 1% (Low-cost funds)
SELECT 
    name, 
    amc, 
    category, 
    expense_ratio
FROM dim_fund
WHERE expense_ratio < 1.0
ORDER BY expense_ratio ASC;

-- 6. Top 5 Funds with the best Risk-Adjusted Returns (Sharpe Ratio)
SELECT 
    f.name, 
    f.category, 
    p.sharpe, 
    p.cagr_3yr
FROM fact_performance p
JOIN dim_fund f ON p.scheme_code = f.scheme_code
WHERE p.sharpe IS NOT NULL
ORDER BY p.sharpe DESC
LIMIT 5;

-- 7. High Alpha Funds (Top 5 schemes beating the benchmark)
SELECT 
    f.name, 
    f.amc, 
    p.alpha, 
    p.beta
FROM fact_performance p
JOIN dim_fund f ON p.scheme_code = f.scheme_code
ORDER BY p.alpha DESC
LIMIT 5;

-- 8. Monthly Transaction Volume and Value Trend
SELECT 
    d.year,
    d.month_name,
    COUNT(t.txn_id) AS txn_count,
    ROUND(SUM(t.amount), 2) AS total_amount
FROM fact_transactions t
JOIN dim_date d ON t.txn_date = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 9. Top 5 States by Total SIP Investment Amount
SELECT 
    state,
    ROUND(SUM(amount), 2) AS total_sip_amount
FROM fact_transactions
WHERE txn_type = 'SIP'
GROUP BY state
ORDER BY total_sip_amount DESC
LIMIT 5;

-- 10. Top 5 Most Resilient Funds (Lowest Maximum Drawdown)
-- Note: Max Drawdown is stored as a negative number, so 'DESC' gives the smallest loss
SELECT 
    f.name, 
    f.category, 
    p.max_drawdown, 
    p.cagr_3yr
FROM fact_performance p
JOIN dim_fund f ON p.scheme_code = f.scheme_code
ORDER BY p.max_drawdown DESC
LIMIT 5;
