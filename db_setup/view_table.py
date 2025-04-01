import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

def view_table_info(table_name):
    # Load environment variables
    load_dotenv()
    
    # Create SQLAlchemy engine
    connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(connection_string)
    
    with engine.connect() as connection:
        # Get table structure
        print("\nTable Structure:")
        result = connection.execute(text(f"DESCRIBE {table_name}"))
        for row in result:
            print(f"{row[0]}: {row[1]}")
        
        # Get sample data
        print("\nSample Data (First 5 rows):")
        df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", connection)
        print(df.to_string())
        
        # Get row count
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        print(f"\nTotal number of rows: {count}")

if __name__ == "__main__":
    view_table_info('japan_naval_sinkings')
