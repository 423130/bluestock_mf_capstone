import requests
import pandas as pd
from pathlib import Path
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def fetch_live_nav():
    """
    Fetches live NAV data for specific mutual fund schemes from mfapi.in
    and saves the results as CSV files.
    """
    # Scheme codes to fetch
    schemes = {
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip",
        "125497": "HDFC Top 100 Direct"
    }

    # Define paths
    base_dir = Path(__file__).parent
    raw_dir = base_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    base_url = "https://api.mfapi.in/mf/"

    print("\n" + "="*50)
    print(f"{'SCHEME NAME':<25} | {'LATEST NAV':<10} | {'DATE':<12}")
    print("-" * 50)

    for code, name in schemes.items():
        url = f"{base_url}{code}"
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status() # Raise exception for HTTP errors
            
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                # Extract meta and latest data
                meta = data['meta']
                latest_point = data['data'][0]
                
                scheme_name = meta.get('scheme_name', name)
                nav = latest_point.get('nav')
                date = latest_point.get('date')
                
                # Print output
                print(f"{name:<25} | {nav:<10} | {date:<12}")
                
                # Convert all historical data to DataFrame and save to CSV
                df = pd.DataFrame(data['data'])
                # Ensure the CSV name includes the scheme code for uniqueness
                csv_filename = f"live_nav_{code}.csv"
                df.to_csv(raw_dir / csv_filename, index=False)
                
            else:
                logger.warning(f"No data found for scheme code {code}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching code {code} ({name}): {e}")
        except Exception as e:
            logger.error(f"Unexpected error for code {code}: {e}")

    print("="*50 + "\n")
    logger.info(f"Live NAV fetch completed. CSVs saved to {raw_dir}")

if __name__ == "__main__":
    fetch_live_nav()
