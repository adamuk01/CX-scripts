#!/usr/bin/python3


import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Update race average in DB file.")
parser.add_argument("input_file", help="Path to the input DB file")
args = parser.parse_args()

db_file = args.input_file

def update_average(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, total_points_last_year, races_finished_last_year FROM riders")
    rows = cursor.fetchall()

    for id, total_points_str, races_finished_str in rows:
        # Convert string values to integers, handling null values
        total_points = int(total_points_str) if total_points_str is not None else 0
        races_finished = int(races_finished_str) if races_finished_str is not None else 0
        
        if races_finished != 0:  # Avoid division by zero
            average = int(total_points / races_finished)
            cursor.execute("UPDATE riders SET average_points_last_year = ? WHERE total_points_last_year = ? AND races_finished_last_year = ? AND id = ?", (average, total_points, races_finished, id))

    conn.commit()


# Update the average position
def update_average_position_last_year(database_file):
    # Connect to the SQLite database
    cursor = conn.cursor()

    # Execute the SQL UPDATE query to update average_position_last_year based on average_points_last_year
    cursor.execute("""
        UPDATE riders
        SET average_position_last_year = CASE
            WHEN average_points_last_year IS NULL THEN 100
            ELSE (
                SELECT COUNT(DISTINCT average_points_last_year) + 1
                FROM riders AS t2
                WHERE t2.average_points_last_year > riders.average_points_last_year
            )
        END
    """)


    # Commit the transaction and close the database connection
    conn.commit()
    conn.close()


# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Call the function to update the average field
update_average(conn)

# Call the function to update the average position
update_average_position_last_year(conn)

# Close the database connection
conn.close()

