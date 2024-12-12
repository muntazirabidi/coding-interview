```python
import mysql.connector
import pandas as pd
from typing import Optional, List, Dict, Union
from dataclasses import dataclass
import logging
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

class MySQLManager:
    """Class to manage MySQL database operations with pandas integration"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        try:
            connection = mysql.connector.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                port=self.config.port
            )
            yield connection
        finally:
            if connection and connection.is_connected():
                connection.close()

    def execute_query(self, query: str, params: tuple = None) -> Optional[pd.DataFrame]:
        """Execute a query and return results as a pandas DataFrame"""
        try:
            with self.get_connection() as conn:
                if query.strip().upper().startswith('SELECT'):
                    return pd.read_sql_query(query, conn, params=params)
                else:
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    conn.commit()
                    return None
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    def create_table(self, table_name: str, columns: Dict[str, str]):
        """Create a new table with specified columns"""
        columns_str = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.execute_query(query)
        logger.info(f"Table {table_name} created successfully")

    def insert_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
        """Insert a pandas DataFrame into MySQL table"""
        try:
            with self.get_connection() as conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            logger.info(f"Successfully inserted {len(df)} rows into {table_name}")
        except Exception as e:
            logger.error(f"Error inserting DataFrame: {e}")
            raise

    def bulk_insert(self, table_name: str, data: List[Dict]):
        """Bulk insert data into a table"""
        if not data:
            return

        columns = ", ".join(data[0].keys())
        placeholders = ", ".join(["%s"] * len(data[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        values = [tuple(row.values()) for row in data]

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, values)
                conn.commit()
            logger.info(f"Successfully bulk inserted {len(data)} rows into {table_name}")
        except Exception as e:
            logger.error(f"Error in bulk insert: {e}")
            raise

    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """Get the schema of a table"""
        query = f"DESCRIBE {table_name}"
        return self.execute_query(query)

    def get_table_stats(self, table_name: str) -> Dict:
        """Get basic statistics about a table"""
        count_query = f"SELECT COUNT(*) as count FROM {table_name}"
        size_query = f"""
            SELECT
                data_length/1024/1024 as size_mb,
                index_length/1024/1024 as index_size_mb
            FROM information_schema.tables
            WHERE table_schema = '{self.config.database}'
            AND table_name = '{table_name}'
        """

        row_count = self.execute_query(count_query).iloc[0]['count']
        size_stats = self.execute_query(size_query).iloc[0]

        return {
            'row_count': row_count,
            'data_size_mb': round(size_stats['size_mb'], 2),
            'index_size_mb': round(size_stats['index_size_mb'], 2)
        }

# Example usage
if __name__ == "__main__":
    # Configuration
    config = DatabaseConfig(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    # Initialize database manager
    db = MySQLManager(config)

    # Create a table
    columns = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "name": "VARCHAR(255)",
        "age": "INT",
        "email": "VARCHAR(255) UNIQUE"
    }
    db.create_table("users", columns)

    # Create sample DataFrame
    df = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith'],
        'age': [30, 25],
        'email': ['john@example.com', 'jane@example.com']
    })

    # Insert DataFrame into table
    db.insert_dataframe(df, "users")

    # Query data
    query = "SELECT * FROM users WHERE age > %s"
    result_df = db.execute_query(query, params=(25,))
    print("\nQuery Results:")
    print(result_df)

    # Get table statistics
    stats = db.get_table_stats("users")
    print("\nTable Statistics:")
    print(stats)

```

## Basic MySQL Commands

```sql
-- Database Operations
CREATE DATABASE database_name;
USE database_name;
DROP DATABASE database_name;

-- Table Operations
CREATE TABLE table_name (
    column1 datatype constraints,
    column2 datatype constraints
);
DROP TABLE table_name;
ALTER TABLE table_name ADD column_name datatype;

-- Data Operations
SELECT * FROM table_name WHERE condition;
INSERT INTO table_name (column1, column2) VALUES (value1, value2);
UPDATE table_name SET column1 = value1 WHERE condition;
DELETE FROM table_name WHERE condition;

-- Joins
SELECT * FROM table1
INNER JOIN table2 ON table1.id = table2.id;

-- Aggregations
SELECT column1, COUNT(*) as count
FROM table_name
GROUP BY column1
HAVING count > 5;
```

## Practical Usage Tip

```python
# Using the class
db = MySQLManager(config)

# Reading data into pandas
df = db.execute_query("SELECT * FROM users")

# Processing with pandas
processed_df = df.groupby('category').agg({
    'amount': ['sum', 'mean'],
    'quantity': 'count'
})

# Writing back to MySQL
db.insert_dataframe(processed_df, 'summary_table')

```

## Pandas-SQL Integration Guide

```python
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
from typing import Optional, List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PandasSQLTools:
    """
    A comprehensive toolkit for working with Pandas and SQL databases.
    Demonstrates all major patterns for data transfer between pandas and SQL.
    """

    def __init__(self, host: str, user: str, password: str, database: str):
        """Initialize database connections and SQLAlchemy engine"""
        # Connection string for SQLAlchemy
        self.connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        self.engine = create_engine(self.connection_string)

        # Connection details for mysql-connector
        self.connection_params = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def read_sql_basic(self, query: str) -> pd.DataFrame:
        """
        Basic SQL query to DataFrame using pandas.read_sql()
        Best for simple queries and small to medium datasets
        """
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            logger.error(f"Error in read_sql_basic: {e}")
            raise

    def read_sql_chunked(self, query: str, chunksize: int = 10000) -> pd.DataFrame:
        """
        Read large SQL tables in chunks to manage memory
        Returns concatenated DataFrame after processing each chunk
        """
        chunks = []
        try:
            # Read the query in chunks
            for chunk in pd.read_sql(query, self.engine, chunksize=chunksize):
                # Process each chunk as needed
                processed_chunk = self._process_chunk(chunk)
                chunks.append(processed_chunk)

            # Combine all chunks
            return pd.concat(chunks, ignore_index=True)
        except Exception as e:
            logger.error(f"Error in read_sql_chunked: {e}")
            raise

    def _process_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """Example chunk processing - customize as needed"""
        # Add your chunk processing logic here
        return chunk

    def write_to_sql_basic(self, df: pd.DataFrame, table_name: str,
                          if_exists: str = 'replace') -> None:
        """
        Basic DataFrame to SQL using to_sql()
        Good for small to medium datasets
        if_exists options: 'fail', 'replace', 'append'
        """
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Successfully wrote {len(df)} rows to {table_name}")
        except Exception as e:
            logger.error(f"Error in write_to_sql_basic: {e}")
            raise

    def write_to_sql_chunked(self, df: pd.DataFrame, table_name: str,
                            chunk_size: int = 1000) -> None:
        """
        Write large DataFrames to SQL in chunks
        Better memory management for large datasets
        """
        try:
            # First chunk replaces table, rest append
            if_exists = 'replace'

            # Process DataFrame in chunks
            for i in range(0, len(df), chunk_size):
                chunk = df.iloc[i:i + chunk_size]
                chunk.to_sql(table_name, self.engine,
                           if_exists=if_exists, index=False)
                if_exists = 'append'  # Switch to append after first chunk

            logger.info(f"Successfully wrote {len(df)} rows to {table_name} in chunks")
        except Exception as e:
            logger.error(f"Error in write_to_sql_chunked: {e}")
            raise

    def upsert_to_sql(self, df: pd.DataFrame, table_name: str,
                      unique_columns: List[str]) -> None:
        """
        Upsert (INSERT ... ON DUPLICATE KEY UPDATE) operation
        Updates existing records and inserts new ones based on unique columns
        """
        try:
            # Create temporary table
            temp_table = f"temp_{table_name}"
            df.to_sql(temp_table, self.engine, if_exists='replace', index=False)

            # Prepare column lists
            all_columns = df.columns.tolist()
            update_columns = [col for col in all_columns if col not in unique_columns]

            # Prepare UPDATE clause
            update_clause = ", ".join([f"{col} = VALUES({col})"
                                     for col in update_columns])

            # Perform upsert
            upsert_query = f"""
                INSERT INTO {table_name} ({', '.join(all_columns)})
                SELECT {', '.join(all_columns)} FROM {temp_table}
                ON DUPLICATE KEY UPDATE {update_clause}
            """

            with self.engine.connect() as conn:
                conn.execute(upsert_query)

            # Clean up temporary table
            with self.engine.connect() as conn:
                conn.execute(f"DROP TABLE IF EXISTS {temp_table}")

            logger.info(f"Successfully upserted {len(df)} rows to {table_name}")
        except Exception as e:
            logger.error(f"Error in upsert_to_sql: {e}")
            raise

    def read_sql_with_params(self, query: str, params: Dict) -> pd.DataFrame:
        """
        Execute parameterized SQL queries with pandas
        Safer than string formatting for handling user input
        """
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Error in read_sql_with_params: {e}")
            raise

    def execute_sql_operations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Demonstrate common SQL operations using pandas
        Shows equivalent pandas operations for SQL commands
        """
        # SELECT equivalent - DataFrame column selection
        selected_df = df[['column1', 'column2']]

        # WHERE equivalent - DataFrame filtering
        filtered_df = df[df['column1'] > 100]

        # GROUP BY equivalent - DataFrame grouping
        grouped_df = df.groupby('category').agg({
            'value': ['sum', 'mean', 'count'],
            'other_col': 'max'
        })

        # JOIN equivalent - DataFrame merging
        # Assuming another DataFrame df2
        merged_df = df.merge(
            df2,
            how='left',  # 'left', 'right', 'inner', 'outer'
            on='key_column'  # or left_on='col1', right_on='col2'
        )

        return merged_df

# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_df = pd.DataFrame({
        'id': range(1, 1001),
        'value': np.random.randn(1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000)
    })

    # Initialize tools
    tools = PandasSQLTools(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    # Basic write
    tools.write_to_sql_basic(sample_df, "sample_table")

    # Read with parameters
    param_query = "SELECT * FROM sample_table WHERE value > %(min_value)s"
    result_df = tools.read_sql_with_params(param_query, {'min_value': 0})

    # Chunked read of large table
    large_df = tools.read_sql_chunked(
        "SELECT * FROM large_table",
        chunksize=10000
    )

    # Upsert example
    tools.upsert_to_sql(
        sample_df,
        "sample_table",
        unique_columns=['id']
    )
```

# SQL Commands

## Basic SELECT Queries - The Foundation

```sql
-- This is like asking "Show me all the books in the library"
SELECT * FROM books;

-- This is like saying "Show me just the titles and authors"
SELECT title, author FROM books;

-- Adding conditions with WHERE (like saying "only show mystery books")
SELECT title, author
FROM books
WHERE genre = 'Mystery';

-- You can use multiple conditions
SELECT title, author, publication_year
FROM books
WHERE genre = 'Mystery'
AND publication_year > 2000;
```

## Sorting Results - ORDER BY

```sql
-- Sort books by publication year (newest first)
SELECT title, publication_year
FROM books
ORDER BY publication_year DESC;  -- DESC for descending, ASC for ascending

-- Sort by multiple columns
SELECT title, author, rating
FROM books
ORDER BY rating DESC, title ASC;
```

## Filtering Unique Values - DISTINCT

```sql
-- Show all unique genres in our library
SELECT DISTINCT genre FROM books;

-- Unique combinations
SELECT DISTINCT author, genre
FROM books;

```

## Limiting Results - LIMIT

```sql
-- Show only the first 5 books
SELECT title
FROM books
LIMIT 5;

-- Skip first 5 and show next 5 (pagination)
SELECT title
FROM books
LIMIT 5 OFFSET 5;
```

## Aggregation Functions - Counting and Summarizing

```sql
-- Count total books
SELECT COUNT(*) AS total_books FROM books;

-- Average rating by genre
SELECT genre,
       AVG(rating) AS avg_rating,
       COUNT(*) AS book_count
FROM books
GROUP BY genre;

-- Find genres with more than 10 books
SELECT genre, COUNT(*) AS book_count
FROM books
GROUP BY genre
HAVING COUNT(*) > 10;
```

## Joining Tables - Combining Related Data

Think of this like connecting information from different filing cabinets:

```sql
-- Join books with their authors
SELECT books.title, authors.name
FROM books
INNER JOIN authors ON books.author_id = authors.id;

-- Different types of joins:
-- INNER JOIN: Only matches in both tables
-- LEFT JOIN: All from left table, matching from right
-- RIGHT JOIN: All from right table, matching from left
-- FULL JOIN: Everything from both tables

-- Example of LEFT JOIN
SELECT books.title, reviews.rating
FROM books
LEFT JOIN reviews ON books.id = reviews.book_id;
```

## Inserting Data - Adding New Records

```sql
-- Add a single book
INSERT INTO books (title, author, genre)
VALUES ('1984', 'George Orwell', 'Fiction');

-- Add multiple books at once
INSERT INTO books (title, author, genre) VALUES
    ('Dune', 'Frank Herbert', 'Science Fiction'),
    ('Pride and Prejudice', 'Jane Austen', 'Romance');
```

## Updating Data - Modifying Existing Records

```sql
-- Update a single record
UPDATE books
SET rating = 5
WHERE title = '1984';

-- Update multiple records
UPDATE books
SET genre = 'Classic Fiction'
WHERE publication_year < 1950;
```

## Deleting Data - Removing Record

```sql
-- Delete specific records
DELETE FROM books
WHERE rating < 3;

-- Delete all records (be careful!)
DELETE FROM books;
```

## Advanced Concepts - Subqueries and More

```sql
-- Find books with above-average ratings
SELECT title, rating
FROM books
WHERE rating > (SELECT AVG(rating) FROM books);

-- Find authors who have written more than 3 books
SELECT author
FROM books
GROUP BY author
HAVING COUNT(*) > 3;
```
