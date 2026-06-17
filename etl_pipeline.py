import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    """
    ETL Pipeline for Bluestock Mutual Fund data.
    Extracts data from CSVs, cleans and transforms it, and loads into a SQLite database.
    """
    def __init__(self, raw_data_dir: Path, db_path: Path):
        self.raw_data_dir = raw_data_dir
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.dataframes = {}

    def extract(self):
        """
        Loads all 10 CSVs from data/raw/ using pandas.
        Uses pathlib.Path for file handling.
        """
        logger.info("Starting extraction phase...")
        # Ensure the directory exists
        if not self.raw_data_dir.exists():
            logger.error(f"Raw data directory does not exist: {self.raw_data_dir}")
            return

        csv_files = list(self.raw_data_dir.glob("*.csv"))
        
        if not csv_files:
            logger.warning(f"No CSV files found in {self.raw_data_dir}")
            return

        for file_path in csv_files:
            df_name = file_path.stem
            try:
                # Use low_memory=False to avoid DtypeWarning for large files
                self.dataframes[df_name] = pd.read_csv(file_path, low_memory=False)
                logger.info(f"Loaded {file_path.name} with {len(self.dataframes[df_name])} rows.")
            except Exception as e:
                logger.error(f"Error loading {file_path.name}: {e}")
        
        logger.info(f"Extracted {len(self.dataframes)} files.")

    def transform(self):
        """
        Cleans and transforms the extracted data.
        Performs specific cleaning for nav_history and investor_transactions.
        Generates dim_date table.
        """
        logger.info("Starting transformation phase...")
        
        # 1. Clean nav_history (02_nav_history)
        if '02_nav_history' in self.dataframes:
            df_nav = self.dataframes['02_nav_history'].copy()
            df_nav['date'] = pd.to_datetime(df_nav['date'])
            
            # Remove duplicates
            before_dup = len(df_nav)
            df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
            after_dup = len(df_nav)
            if before_dup != after_dup:
                logger.info(f"Removed {before_dup - after_dup} duplicate rows from nav_history.")

            # Forward-fill missing NAVs per fund
            # We sort by amfi_code and date first to ensure ffill works correctly in chronological order
            df_nav = df_nav.sort_values(['amfi_code', 'date'])
            df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
            self.dataframes['fact_nav'] = df_nav
        
        # 2. Clean investor_transactions (08_investor_transactions)
        if '08_investor_transactions' in self.dataframes:
            df_tx = self.dataframes['08_investor_transactions'].copy()
            df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])
            
            # Standardise transaction_type (SIP, Lumpsum, Redemption)
            tx_type_map = {
                'sip': 'SIP',
                'lumpsum': 'Lumpsum',
                'redemption': 'Redemption'
            }
            df_tx['transaction_type'] = df_tx['transaction_type'].str.strip().str.lower().map(tx_type_map).fillna(df_tx['transaction_type'])
            
            # Validate amounts (ensure positive)
            before_val = len(df_tx)
            df_tx = df_tx[df_tx['amount_inr'] > 0]
            after_val = len(df_tx)
            if before_val != after_val:
                logger.warning(f"Removed {before_val - after_val} rows with non-positive amounts from transactions.")
                
            self.dataframes['fact_transactions'] = df_tx

        # 3. Create dim_date
        # Collect all unique dates from relevant tables
        date_sources = []
        if 'fact_nav' in self.dataframes:
            date_sources.append(self.dataframes['fact_nav']['date'])
        if 'fact_transactions' in self.dataframes:
            date_sources.append(self.dataframes['fact_transactions']['transaction_date'])
        if '03_aum_by_fund_house' in self.dataframes:
            date_sources.append(pd.to_datetime(self.dataframes['03_aum_by_fund_house']['date']))

        if date_sources:
            all_dates = pd.concat(date_sources).unique()
            dim_date = pd.DataFrame({'date': all_dates})
            dim_date['date'] = pd.to_datetime(dim_date['date'])
            dim_date = dim_date.sort_values('date').dropna()
            
            dim_date['day'] = dim_date['date'].dt.day
            dim_date['month'] = dim_date['date'].dt.month
            dim_date['year'] = dim_date['date'].dt.year
            dim_date['quarter'] = dim_date['date'].dt.quarter
            dim_date['is_weekend'] = dim_date['date'].dt.dayofweek >= 5
            self.dataframes['dim_date'] = dim_date
            logger.info(f"Generated dim_date with {len(dim_date)} unique dates.")

        # 4. Map other tables as requested
        if '01_fund_master' in self.dataframes:
            self.dataframes['dim_fund'] = self.dataframes['01_fund_master']
        
        if '07_scheme_performance' in self.dataframes:
            self.dataframes['fact_performance'] = self.dataframes['07_scheme_performance']
            
        if '03_aum_by_fund_house' in self.dataframes:
            self.dataframes['fact_aum'] = self.dataframes['03_aum_by_fund_house']

    def load(self):
        """
        Loads all cleaned data into the SQLite DB and saves as processed CSVs.
        Uses SQLAlchemy for database interaction and pandas for CSV export.
        """
        logger.info("Starting load phase...")
        # Create directories if they don't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        processed_dir = self.db_path.parent.parent / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        tables_to_load = [
            'dim_fund', 'dim_date', 'fact_nav', 
            'fact_transactions', 'fact_performance', 'fact_aum'
        ]
        
        # Also include other raw tables that might be useful for EDA but weren't explicitly in the schema
        all_tables = tables_to_load + ['04_monthly_sip_inflows', '05_category_inflows', '06_industry_folio_count', '09_portfolio_holdings', '10_benchmark_indices']

        for table_name in all_tables:
            if table_name in self.dataframes:
                df = self.dataframes[table_name]
                try:
                    # Save to SQLite (only for those in schema)
                    if table_name in tables_to_load:
                        df.to_sql(table_name, self.engine, if_exists='replace', index=False)
                        logger.info(f"Successfully loaded table '{table_name}' to DB.")
                    
                    # Save to processed CSV
                    csv_name = f"{table_name}.csv"
                    df.to_csv(processed_dir / csv_name, index=False)
                    logger.info(f"Successfully saved '{csv_name}' to processed directory.")
                except Exception as e:
                    logger.error(f"Error loading/saving {table_name}: {e}")
            else:
                if table_name in tables_to_load:
                    logger.warning(f"Required table data for '{table_name}' was not found.")

    def run(self):
        """Executes the full ETL pipeline: Extract -> Transform -> Load."""
        try:
            self.extract()
            self.transform()
            self.load()
            logger.info("ETL Pipeline execution completed.")
            self.print_row_counts()
        except Exception as e:
            logger.error(f"ETL Pipeline encountered a critical error: {e}")
            raise

    def print_row_counts(self):
        """Prints row counts for verification from the database."""
        print("\n" + "="*40)
        print("DATABASE ROW COUNTS VERIFICATION")
        print("="*40)
        tables = ['dim_fund', 'dim_date', 'fact_nav', 'fact_transactions', 'fact_performance', 'fact_aum']
        
        with self.engine.connect() as conn:
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"{table:25}: {count:,} rows")
                except Exception:
                    print(f"{table:25}: [Table not found]")
        print("="*40 + "\n")

if __name__ == "__main__":
    # Define paths relative to the script location
    BASE_DIR = Path(__file__).parent
    RAW_DIR = BASE_DIR / "data" / "raw"
    DB_FILE = BASE_DIR / "data" / "db" / "bluestock_mf.db"
    
    # Initialize and run the pipeline
    pipeline = ETLPipeline(RAW_DIR, DB_FILE)
    pipeline.run()
