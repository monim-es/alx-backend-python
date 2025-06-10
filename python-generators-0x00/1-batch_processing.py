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

def stream_users_in_batches(batch_size):
    """Generator that fetches user_data rows in batches of batch_size."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size
    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """Process batches and yield users with age > 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
