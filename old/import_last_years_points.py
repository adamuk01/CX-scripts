#!/usr/bin/python3

# This will load last years averge points into the database.

import csv
import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Load result data into race database")
parser.add_argument("db_input_file", help="Path to the DB file")
parser.add_argument("csv_input_file", help="Path to CSV file")
args = parser.parse_args()

database_file = args.db_input_file
csv_file = args.csv_input_file

print("Updating database:",database_file,"with",csv_file)

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
c = conn.cursor()

# Open the CSV file and create a CSV reader object
with open(csv_file, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)

    # Iterate over each row in the CSV file
    for row in csvreader:
        # Extract data from the row
        rider_number = row[1]  # Assuming rider number is in the first column
        updated_field1 = row[6]  # Total Average points
        updated_field2 = row[7]  # Races completed

        # Remove the comma from the string representation of the number
        number_without_comma = updated_field1.replace(",", "")

        # Convert the string to a float and then to an integer
        true_integer = int(float(number_without_comma))

        # Execute SQL UPDATE statement to modify specific fields based on rider number
        c.execute(f'''UPDATE riders
                     SET total_points_last_year = ?, races_finished_last_year = ?
                     WHERE race_number = ?''', (true_integer, updated_field2, rider_number))
        if c.rowcount > 0:
            conn.commit()
#            print("Update successful with rider_number", rider_number)
        else:
            print("Exception: No rows were updated with rider_number", rider_number)


# Commit changes and close connection
conn.commit()
conn.close()

print("Fields updated successfully!")
