"""
db_connect.py
=============
Reusable database connection — reads credentials from .env file.
Copy into any project. Never hardcode passwords.

SETUP:
    1. Copy .env.example to .env
    2. Fill in your credentials in .env
    3. from db_connect import query, pull_table, get_engine
"""

import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

# Load credentials from .env file automatically
load_dotenv()


# ── PostgreSQL ────────────────────────────────────────────────

def get_engine():
    """
    Returns a SQLAlchemy engine using credentials from .env file.
    
    Required .env variables:
        DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    """
    url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 5432)}/{os.getenv('DB_NAME')}"
    )
    return sqlalchemy.create_engine(url)


def query(sql):
    """
    Run any SQL query and return a pandas DataFrame.
    
    Example:
        from db_connect import query
        df = query('SELECT * FROM sales_orders LIMIT 100')
    """
    engine = get_engine()
    return pd.read_sql(sql, engine)


def pull_table(table_name, schema='public'):
    """
    Pull an entire table into a DataFrame.
    
    Example:
        from db_connect import pull_table
        df_sales = pull_table('sales_orders')
        df_reps  = pull_table('reps')
    """
    return query(f'SELECT * FROM {schema}.{table_name}')


def write_table(df, table_name, schema='analytics', if_exists='replace'):
    """
    Write a DataFrame to the database as a table.
    
    if_exists options:
        'replace' — drop and recreate the table
        'append'  — add rows to existing table
        'fail'    — raise error if table exists
    
    Example:
        from db_connect import write_table
        write_table(df_clean, 'processed_sales', schema='analytics')
    """
    engine = get_engine()
    df.to_sql(table_name, engine, schema=schema,
              if_exists=if_exists, index=False)
    print(f"Written {len(df):,} rows to {schema}.{table_name}")


def test_connection():
    """
    Test database connection. Run this first on any new project.
    
    Example:
        python db_connect.py
    """
    try:
        result = query('SELECT 1 AS connected')
        print(f"Connected to {os.getenv('DB_NAME')} on {os.getenv('DB_HOST')}")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


# ── Snowflake (uncomment if using Snowflake) ──────────────────

# def get_snowflake_engine():
#     from snowflake.sqlalchemy import URL
#     return sqlalchemy.create_engine(URL(
#         account   = os.getenv('SNOWFLAKE_ACCOUNT'),
#         user      = os.getenv('SNOWFLAKE_USER'),
#         password  = os.getenv('SNOWFLAKE_PASSWORD'),
#         database  = os.getenv('SNOWFLAKE_DATABASE'),
#         schema    = os.getenv('SNOWFLAKE_SCHEMA'),
#         warehouse = os.getenv('SNOWFLAKE_WAREHOUSE'),
#     ))


if __name__ == '__main__':
    test_connection()
