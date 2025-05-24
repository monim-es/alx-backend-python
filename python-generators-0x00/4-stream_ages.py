#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()

def average_user_age():
    """Calculates and prints the average age using the age generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count > 0:
        avg = total_age / count
        print(f"Average age of users: {avg}")
    else:
        print("No users found.")

if __name__ == "__main__":
    average_user_age()
