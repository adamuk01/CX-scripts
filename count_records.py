#!/usr/bin/python3

# This will Count the records in a datbase file

import sqlite3
import sys

def count_entries(database_file):
    # Connect to the SQLite database
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Execute the query to count the number of entries in the 'riders' table
        cursor.execute("SELECT COUNT(*) FROM riders")
        count = cursor.fetchone()[0]

        # Print the result
        print(f"Number of entries in 'riders' table: {count}")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_records.py <database_file>")
    else:
        database_file = sys.argv[1]
        count_entries(database_file)

