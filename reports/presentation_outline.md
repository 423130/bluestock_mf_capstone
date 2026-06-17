# Bluestock MF Analytics Platform: 12-Slide Presentation Outline

## Slide 1: Title Slide
*   **Title:** Bluestock MF Analytics Platform
*   **Subtitle:** Unlocking Insights into Indian Mutual Fund Performance & Investor Behavior
*   **Presenter Name:** [Your Name]
*   **Key Points:** Capstone Project Overview, June 2026.
*   **Visual:** High-resolution professional background (e.g., stylized financial data visualization or stock market silhouette).

## Slide 2: The Mutual Fund Revolution in India
*   **Title:** Industry at a Glance: Massive Financialization
*   **Key Points:**
    *   Total Folios: **26.12 Cr** (Industry-wide growth).
    *   SIP Adoption: Monthly inflows peaking at **₹31,002 Cr** (Dec 2025).
    *   Market Dominance: **SBI Mutual Fund** AUM at **₹12.5L Cr**.
*   **Visual:** KPI Cards showing Folios, SIP Peak, and Total Industry AUM.

## Slide 3: Project Objectives & Scope
*   **Title:** Data-Driven Decision Support
*   **Key Points:**
    *   Automate ETL for 10 heterogeneous datasets.
    *   Perform risk-adjusted audit for **40 premium schemes**.
    *   Analyze behavior for **5,000 investors** across **12 states**.
    *   Establish a proprietary **Fund Scorecard (0-100)**.
*   **Visual:** Icon-based flow: Data Collection -> Engineering -> Analytics -> Insights.

## Slide 4: Data Pipeline & Star Schema
*   **Title:** Robust Engineering Architecture
*   **Key Points:**
    *   **ETL:** Python, Pandas, SQLAlchemy.
    *   **Storage:** SQLite Star Schema with 6 optimized tables.
    *   **Scale:** 46,000+ daily NAV records processed.
*   **Visual:** Star Schema Diagram (central fact tables connected to dim_fund and dim_date).

## Slide 5: Market Performance: The 2023 Bull Run
*   **Title:** Historical NAV Trends (2022-2025)
*   **Key Points:**
    *   Visualizing the impact of the **2023 Bull Run**.
    *   Outperformance of Small/Mid-cap schemes vs Large-cap benchmarks.
    *   High resilience observed in top-tier funds.
*   **Visual:** **Plotly Line Chart** showing NAV trends of 40 schemes with a shaded "2023 Bull Run" annotation.

## Slide 6: Risk-Adjusted Returns: Beyond CAGR
*   **Title:** Performance Analytics Audit
*   **Key Points:**
    *   **Sharpe Ratio:** Reward per unit of total risk.
    *   **Sortino Ratio:** Downside risk efficiency.
    *   **Alpha & Beta:** Market outperformance and sensitivity (Nifty 50).
*   **Visual:** **Alpha vs. Beta Scatter Plot** or a Horizontal Bar Chart of top 10 funds by Sharpe Ratio.

## Slide 7: The Bluestock Fund Scorecard
*   **Title:** Our Proprietary Ranking System
*   **Key Points:**
    *   30% Weight: 3-Year CAGR.
    *   25% Weight: Sharpe Ratio.
    *   20% Weight: Alpha Generation.
    *   15% Weight: Expense Ratio (Inverse).
    *   10% Weight: Max Drawdown (Inverse).
*   **Visual:** **Donut Chart** showing the weighting distribution of the scorecard.

## Slide 8: Tail Risk & Market Resilience
*   **Title:** Tail Risk Assessment: VaR & CVaR
*   **Key Points:**
    *   **VaR (95%):** Minimum expected loss in a single day.
    *   **CVaR (Expected Shortfall):** Average loss beyond the VaR threshold.
    *   Identification of "Stress Tested" funds.
*   **Visual:** **Seaborn Bar Chart** showing CVaR (Expected Shortfall) for the top 10 most volatile schemes.

## Slide 9: Investor Demographic Trends
*   **Title:** Who is the Indian Investor?
*   **Key Points:**
    *   **Core Cohort:** 26-35 age group (Digital First).
    *   **Geographic Diversity:** Analysis across 12 states.
    *   **Tier Analysis:** T30 (Top 30 cities) vs B30 (Beyond 30) growth.
*   **Visual:** **Pie Chart** for age distribution and a **Bar Chart** of average investment size by City Tier.

## Slide 10: Portfolio Concentration & HHI
*   **Title:** Sector Diversification Audit
*   **Key Points:**
    *   **HHI Index:** Measuring sector concentration.
    *   Identifying over-exposure to specific industries (e.g., Banking/IT).
    *   Comparing well-diversified vs. concentrated portfolios.
*   **Visual:** **Seaborn Heatmap** of sector weights or a **Histogram** of Sector HHI scores across all funds.

## Slide 11: Benchmarking & Recommendation
*   **Title:** Beating the Market
*   **Key Points:**
    *   Comparison: Top 5 Funds vs **Nifty 50** & **Nifty 100**.
    *   Simple Risk-Based Recommender (Low/Moderate/High).
    *   Strategic shift from Passive to Active selection.
*   **Visual:** **Normalized Growth Chart** (Base 100) comparing Top 5 Funds against Nifty 50.

## Slide 12: Summary & Future Roadmap
*   **Title:** Building the Future of MF Wealthtech
*   **Key Points:**
    *   Conclusion: Data engineering is the foundation of smart investing.
    *   Future: Real-time API integration & Predictive ML Churn models.
    *   Impact: Scalable analytics for retail investors and AMCs.
*   **Visual:** High-level summary graphic: "Data -> Intelligence -> Wealth."
