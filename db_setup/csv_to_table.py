import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import numpy as np

def get_sql_type(dtype):
    """Map pandas dtypes to SQL types"""
    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATETIME'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    else:
        return 'TEXT'

def create_table_from_csv(csv_path, table_name):
    """Create a MySQL table from a CSV file"""
    # Load environment variables
    load_dotenv()
    
    # Read CSV file
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Create SQLAlchemy engine
    connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(connection_string)
    
    # Generate CREATE TABLE statement
    columns = []
    for column, dtype in df.dtypes.items():
        sql_type = get_sql_type(dtype)
        # Clean column name (remove special characters and spaces)
        clean_column = column.replace(' ', '_').replace('-', '_').lower()
        columns.append(f"`{clean_column}` {sql_type}")
    
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {', '.join(columns)}
    )
    """
    
    # Create table and load data
    with engine.connect() as connection:
        print(f"Creating table: {table_name}")
        connection.execute(text(create_table_sql))
        connection.commit()
        
        print("Loading data into table...")
        # Clean column names in DataFrame to match table
        df.columns = [col.replace(' ', '_').replace('-', '_').lower() for col in df.columns]
        # Replace NaN values with None for proper SQL NULL handling
        df = df.replace({np.nan: None})
        
        # Load data in chunks to handle large files
        chunk_size = 1000
        for i in range(0, len(df), chunk_size):
            chunk = df[i:i + chunk_size]
            chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Loaded {min(i + chunk_size, len(df))} of {len(df)} rows")
    
    print("Table creation and data loading completed successfully!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python csv_to_table.py <csv_file_path> <table_name>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    table_name = sys.argv[2]
    create_table_from_csv(csv_path, table_name)
