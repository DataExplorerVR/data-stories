from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd
from typing import Optional

def get_db_connection():
    """Create and return a database connection"""
    load_dotenv()
    connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(connection_string)

def aggregate_monthly_sinkings(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Aggregate sinkings by month, including count and total tonnage.
    
    Args:
        start_date (str, optional): Start date in format 'YYYY-MM-DD'
        end_date (str, optional): End date in format 'YYYY-MM-DD'
    
    Returns:
        pandas.DataFrame: Monthly aggregations with columns:
            - sunk_month_year: Month and year of sinking
            - total_sinkings: Count of vessels sunk
            - total_tonnage: Sum of standard tonnage
    """
    engine = get_db_connection()
    
    # Build the base query
    query = """
    SELECT 
        sunk_month_year,
        COUNT(*) as total_sinkings,
        SUM(CAST(REPLACE(REPLACE(sunk_standard_tonnage, ',', ''), ' ', '') AS DECIMAL(10,2))) as total_tonnage
    FROM japan_naval_sinkings
    """
    
    # Add WHERE clause if dates are provided
    where_clauses = []
    if start_date:
        where_clauses.append(f"sunk_date >= '{start_date}'")
    if end_date:
        where_clauses.append(f"sunk_date <= '{end_date}'")
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    # Add GROUP BY and ORDER BY
    query += """
    GROUP BY sunk_month_year
    ORDER BY MIN(sunk_date)
    """
    
    # Execute query and return results as DataFrame
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    
    return df

if __name__ == "__main__":
    # Example usage
    print("\nExample 1: All-time monthly aggregation")
    print(aggregate_monthly_sinkings())
    
    print("\nExample 2: Monthly aggregation for 1942")
    print(aggregate_monthly_sinkings('1942-01-01', '1942-12-31'))
