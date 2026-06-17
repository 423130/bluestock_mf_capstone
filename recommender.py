import pandas as pd
from pathlib import Path
import sys

def get_recommendations(risk_appetite: str, funds_df: pd.DataFrame, performance_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter and rank funds based on risk appetite and Sharpe ratio.
    """
    # Define risk mapping
    risk_map = {
        'low': ['Low', 'Low to Moderate'],
        'moderate': ['Moderate', 'Moderately High'],
        'high': ['High', 'Very High']
    }
    
    selected_grades = risk_map.get(risk_appetite.lower())
    if not selected_grades:
        return pd.DataFrame()

    # Merge performance with fund details
    merged_df = pd.merge(
        performance_df, 
        funds_df[['amfi_code', 'scheme_name', 'risk_category', 'expense_ratio_pct']], 
        on='amfi_code'
    )
    
    # Filter by risk grade
    filtered_df = merged_df[merged_df['risk_category'].isin(selected_grades)]
    
    # Sort by Sharpe Ratio (Highest first)
    recommended = filtered_df.sort_values(by='sharpe_ratio', ascending=False).head(3)
    
    return recommended

def main():
    # Setup paths
    base_dir = Path(__file__).parent
    processed_dir = base_dir / "data" / "processed"
    
    funds_path = processed_dir / "dim_fund.csv"
    perf_path = processed_dir / "fact_performance.csv"
    
    # Check if files exist
    if not funds_path.exists() or not perf_path.exists():
        print(f"Error: Required files not found in {processed_dir}")
        print("Please run the ETL pipeline and performance analytics first.")
        return

    # Load data
    try:
        funds_df = pd.read_csv(funds_path)
        # Use performance from scorecard if fact_performance doesn't exist or is empty
        # Actually the user asked for fact_performance.csv
        performance_df = pd.read_csv(perf_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print("\n" + "="*50)
    print("BLUESTOCK MUTUAL FUND RECOMMENDER")
    print("="*50)
    
    risk_input = input("Enter your Risk Appetite (Low / Moderate / High): ").strip()
    
    if risk_input.lower() not in ['low', 'moderate', 'high']:
        print("Invalid input. Please choose from Low, Moderate, or High.")
        return

    recommendations = get_recommendations(risk_input, funds_df, performance_df)

    if recommendations.empty:
        print(f"\nNo funds found for '{risk_input}' risk appetite.")
    else:
        print(f"\nTop 3 Recommended Funds for {risk_input.capitalize()} Risk Profile:")
        print("-" * 80)
        print(f"{'Scheme Name':<45} | {'Sharpe':<8} | {'3Yr Ret':<8} | {'Exp Ratio':<8}")
        print("-" * 80)
        for _, row in recommendations.iterrows():
            ret_3yr = f"{row['return_3yr_pct']:.2f}%" if not pd.isna(row['return_3yr_pct']) else "N/A"
            sharpe = f"{row['sharpe_ratio']:.2f}" if not pd.isna(row['sharpe_ratio']) else "N/A"
            exp = f"{row['expense_ratio_pct']:.2f}%"
            print(f"{row['scheme_name'][:43]:<45} | {sharpe:<8} | {ret_3yr:<8} | {exp:<8}")
        print("-" * 80)

if __name__ == "__main__":
    main()
