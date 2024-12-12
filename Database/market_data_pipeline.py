import requests
import pandas as pd
import mysql.connector
from typing import Optional, Dict, List
from dataclasses import dataclass
import logging
from datetime import datetime, timedelta
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration parameters"""
    host: str
    user: str
    password: str
    database: str
    port: int = 3306

class MarketDataPipeline:
    """
    Pipeline for fetching, processing, and storing market data.
    Demonstrates handling API data, efficient processing, and database operations.
    """
    
    def __init__(self, config: DatabaseConfig, api_key: str):
        self.config = config
        self.api_key = api_key
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                port=self.config.port
            )
            yield conn
        finally:
            if conn and conn.is_connected():
                conn.close()

    def fetch_market_data(self, symbol: str, start_date: str) -> pd.DataFrame:
        """
        Fetch market data from a public API
        Using Alpha Vantage as an example, but could be any market data API
        """
        try:
            # Example API endpoint (Alpha Vantage)
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_key,
                "outputsize": "full"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Convert API response to DataFrame
            data = response.json()
            df = pd.DataFrame.from_dict(
                data['Time Series (Daily)'],
                orient='index'
            )
            
            # Clean column names and data types
            df.columns = [col.split('. ')[1] for col in df.columns]
            df = df.astype(float)
            df.index = pd.to_datetime(df.index)
            
            # Filter by start date
            df = df[df.index >= start_date]
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            raise

    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate common financial metrics
        Demonstrates efficient pandas operations
        """
        # Calculate returns
        df['daily_return'] = df['close'].pct_change()
        
        # Calculate rolling metrics
        df['volatility_20d'] = df['daily_return'].rolling(20).std() * (252 ** 0.5)
        df['sma_50d'] = df['close'].rolling(50).mean()
        df['sma_200d'] = df['close'].rolling(200).mean()
        
        # Calculate trading signals
        df['signal'] = np.where(df['sma_50d'] > df['sma_200d'], 1, -1)
        
        return df

    def setup_database(self):
        """Create necessary database tables"""
        market_data_schema = {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "symbol": "VARCHAR(10)",
            "date": "DATE",
            "open": "DECIMAL(10,2)",
            "high": "DECIMAL(10,2)",
            "low": "DECIMAL(10,2)",
            "close": "DECIMAL(10,2)",
            "volume": "BIGINT",
            "daily_return": "DECIMAL(10,4)",
            "volatility": "DECIMAL(10,4)",
            "signal": "INT",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            columns_str = ", ".join([f"{col} {dtype}" for col, dtype in market_data_schema.items()])
            query = f"""
            CREATE TABLE IF NOT EXISTS market_data (
                {columns_str},
                INDEX idx_symbol_date (symbol, date)
            )
            """
            cursor.execute(query)
            conn.commit()

    def store_market_data(self, df: pd.DataFrame, symbol: str):
        """Store processed market data in MySQL"""
        # Prepare data for insertion
        df_to_insert = df.reset_index()
        df_to_insert.columns = df_to_insert.columns.str.lower()
        df_to_insert['symbol'] = symbol
        
        # Insert data efficiently using executemany
        insert_query = """
        INSERT INTO market_data 
        (symbol, date, open, high, low, close, volume, 
         daily_return, volatility, signal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = [
            (symbol, row['date'], row['open'], row['high'], 
             row['low'], row['close'], row['volume'],
             row['daily_return'], row['volatility_20d'], 
             row['signal'])
            for _, row in df_to_insert.iterrows()
        ]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_query, values)
            conn.commit()

    def get_latest_signals(self, symbols: List[str]) -> pd.DataFrame:
        """
        Retrieve latest trading signals for multiple symbols
        Demonstrates efficient SQL query
        """
        query = """
        WITH LatestData AS (
            SELECT 
                symbol,
                date,
                close,
                signal,
                volatility,
                ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) as rn
            FROM market_data
            WHERE symbol IN ({})
        )
        SELECT 
            symbol,
            date,
            close,
            signal,
            volatility
        FROM LatestData
        WHERE rn = 1
        """.format(','.join(['%s'] * len(symbols)))
        
        with self.get_connection() as conn:
            return pd.read_sql(query, conn, params=symbols)

def main():
    # Initialize pipeline
    config = DatabaseConfig(
        host="localhost",
        user="your_username",
        password="your_password",
        database="market_data"
    )
    pipeline = MarketDataPipeline(config, api_key="your_api_key")
    
    # Setup database
    pipeline.setup_database()
    
    # Process data for multiple symbols
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    start_date = '2023-01-01'
    
    for symbol in symbols:
        # Fetch and process data
        df = pipeline.fetch_market_data(symbol, start_date)
        df_processed = pipeline.calculate_metrics(df)
        
        # Store in database
        pipeline.store_market_data(df_processed, symbol)
    
    # Get latest signals
    latest_signals = pipeline.get_latest_signals(symbols)
    print("\nLatest Trading Signals:")
    print(latest_signals)

if __name__ == "__main__":
    main()