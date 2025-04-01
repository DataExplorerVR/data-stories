import mysql.connector
from dotenv import load_dotenv
import os

def init_database():
    # Load environment variables
    load_dotenv()
    
    # Get database configuration
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', '3306')
    }
    
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        db_name = os.getenv('DB_NAME', 'data_stories')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        
        # Switch to the database
        cursor.execute(f"USE {db_name}")
        
        # Here you can add your table creation statements
        # Example:
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS your_table (
        #         id INT AUTO_INCREMENT PRIMARY KEY,
        #         name VARCHAR(255),
        #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #     )
        # """)
        
        conn.commit()
        print("Database initialization completed successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    init_database()
