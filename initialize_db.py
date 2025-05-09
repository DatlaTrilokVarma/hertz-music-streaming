"""Initialize MySQL database for MTunes."""
import os
import mysql.connector
from mysql.connector import Error

def setup_mysql():
    """Set up MySQL database."""
    # Get MySQL connection parameters from environment variables
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_database = os.environ.get('MYSQL_DB', 'mtunes')
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_database}")
            print(f"Database '{mysql_database}' created or already exists.")
            
            # Use the database
            cursor.execute(f"USE {mysql_database}")
            
            # Import schema and data from previously exported SQL file
            export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mysql_export')
            combined_sql_file = os.path.join(export_dir, 'mtunes_mysql_complete.sql')
            
            if os.path.exists(combined_sql_file):
                print(f"Importing schema and data from {combined_sql_file}...")
                
                # Read the SQL file
                with open(combined_sql_file, 'r') as f:
                    sql_script = f.read()
                
                # Split script into individual statements and execute them
                statements = sql_script.split(';')
                for statement in statements:
                    if statement.strip():
                        cursor.execute(statement)
                
                connection.commit()
                print("Schema and data imported successfully.")
            else:
                print(f"SQL file not found: {combined_sql_file}")
                print("Please run mysql_export.py first to generate the SQL file.")
            
            # Close the connection
            cursor.close()
            connection.close()
            print("MySQL connection closed.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # Make sure connection is closed
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    setup_mysql()