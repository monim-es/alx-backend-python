#!/usr/bin/python3
import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )

def stream_users():
    """Generator that yields rows from user_data table one by one."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    conn.close()
