from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

def drop_table(table_name):
    # Load environment variables
    load_dotenv()
    
    # Create SQLAlchemy engine
    connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(connection_string)
    
    with engine.connect() as connection:
        # Drop the table
        drop_sql = f"DROP TABLE IF EXISTS {table_name}"
        connection.execute(text(drop_sql))
        connection.commit()
        print(f"Table {table_name} dropped successfully!")

if __name__ == "__main__":
    drop_table('japan_naval_sinkings')
