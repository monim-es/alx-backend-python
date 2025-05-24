# ALX Python Generators - Database Seeder

This project sets up a MySQL database `ALX_prodev` and a `user_data` table, then populates it with data from a CSV file. It demonstrates using a Python generator to stream rows from the database one by one, avoiding loading all data into memory at once.

## Features

- Connect to MySQL server and create database if it doesn't exist
- Create `user_data` table with appropriate schema and indexing
- Insert data from `user_data.csv` safely, avoiding duplicates
- Stream rows using a generator function for efficient memory usage

## Usage

1. Configure your MySQL connection parameters in `seed.py`
2. Run the provided script to set up the database and load data
3. Use the `stream_rows` generator to process database rows efficiently

## Requirements

- Python 3.x
- `mysql-connector-python` package
- MySQL server running locally or remotely

## Example

```python
import seed

conn = seed.connect_to_prodev()
for row in seed.stream_rows(conn):
    print(row)
