import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseAdapter:
    """Adapter pattern for database interactions, abstracting database specifics."""
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.connection = None

    def __enter__(self):
        self.connection = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str, params: Optional[Dict] = None):
        """Execute SQL query with optional parameters."""
        try:
            if params:
                return pd.read_sql_query(text(query), self.connection, params=params)
            return pd.read_sql_query(text(query), self.connection)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    def write_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = 'replace'):
        """Write DataFrame to SQL with options for handling existing tables."""
        try:
            df.to_sql(table_name, self.connection, if_exists=if_exists, index=False)
            logger.info(f"Successfully wrote {len(df)} rows to {table_name}")
        except Exception as e:
            logger.error(f"Error writing DataFrame: {e}")
            raise

    def chunked_operation(self, query: str, chunk_size: int, callback):
        """Template Method pattern for chunked operations."""
        try:
            for chunk in pd.read_sql_query(text(query), self.connection, chunksize=chunk_size):
                callback(chunk)
        except Exception as e:
            logger.error(f"Error in chunked operation: {e}")
            raise

class SQLManager:
    """Facade pattern to manage SQL operations, providing a simpler interface."""
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        self.adapter = DatabaseAdapter(self.connection_string)

    def read_data(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        with self.adapter as db:
            return db.execute_query(query, params)

    def write_data(self, df: pd.DataFrame, table_name: str, if_exists: str = 'replace'):
        with self.adapter as db:
            db.write_dataframe(df, table_name, if_exists)

    def chunked_read(self, query: str, chunk_size: int = 10000, callback=None):
        with self.adapter as db:
            if callback:
                db.chunked_operation(query, chunk_size, callback)
            else:
                logger.warning("No callback provided for chunked operation")

    def upsert_data(self, df: pd.DataFrame, table_name: str, unique_columns: List[str]):
        """
        Performs an upsert operation using a temporary table strategy.
        """
        temp_table = f"temp_{table_name}"
        with self.adapter as db:
            db.write_dataframe(df, temp_table)
            update_columns = [col for col in df.columns if col not in unique_columns]
            update_clause = ", ".join([f"{col} = VALUES({col})" for col in update_columns])
            upsert_query = f"""
                INSERT INTO {table_name} ({', '.join(df.columns)})
                SELECT {', '.join(df.columns)} FROM {temp_table}
                ON DUPLICATE KEY UPDATE {update_clause}
            """
            db.connection.execute(text(upsert_query))
            db.connection.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))
        logger.info(f"Successfully upserted {len(df)} rows to {table_name}")

# Usage examples for interview
if __name__ == "__main__":
    sql_manager = SQLManager(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    
    # Basic read
    result = sql_manager.read_data("SELECT * FROM sample_table WHERE id < 100")
    print(result.head())

    # Write data
    sample_df = pd.DataFrame({
        'id': range(1, 101),
        'value': [f'item_{i}' for i in range(1, 101)]
    })
    sql_manager.write_data(sample_df, "test_table")

    # Chunked read with a callback for processing
    def process_chunk(chunk):
        print(f"Processing chunk with {len(chunk)} rows")
        # Example operation: increase value by 1
        chunk['value'] = chunk['value'].apply(lambda x: x + 1)
        sql_manager.write_data(chunk, "processed_data", if_exists='append')

    sql_manager.chunked_read("SELECT * FROM large_table", chunk_size=10000, callback=process_chunk)

    # Upsert
    update_df = pd.DataFrame({
        'id': [1, 2, 3, 101], 
        'value': ['update1', 'update2', 'update3', 'new_item']
    })
    sql_manager.upsert_data(update_df, "test_table", unique_columns=['id'])