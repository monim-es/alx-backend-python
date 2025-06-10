import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to MySQL server (no database)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # set your root password if any
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # set your root password if any
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists."""
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX idx_user_id(user_id)
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table if user_id doesn't exist."""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if user_id exists
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (row['user_id'],))
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (row['user_id'], row['name'], row['email'], row['age'])
                    )
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")

def stream_rows(connection):
    """Generator that yields rows one by one from user_data."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        row = cursor.fetchone()
        while row:
            yield row
            row = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(f"Error streaming rows: {e}")
