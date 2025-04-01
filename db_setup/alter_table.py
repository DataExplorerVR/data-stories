from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

def alter_table():
    # Load environment variables
    load_dotenv()
    
    # Create SQLAlchemy engine
    connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(connection_string)
    
    with engine.connect() as connection:
        # Rename the column
        alter_sql = "ALTER TABLE japan_naval_sinkings CHANGE COLUMN sunk_type sunk_type_vessel TEXT"
        connection.execute(text(alter_sql))
        connection.commit()
        print("Column renamed successfully!")

if __name__ == "__main__":
    alter_table()
