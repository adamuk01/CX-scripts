#!/usr/bin/python3

import csv
import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Load result data into race database")
parser.add_argument("db_input_file", help="Path to the DB file")
parser.add_argument("csv_input_file", help="Path to CSV file")
parser.add_argument("round", type=int, help="Week or Round number")
args = parser.parse_args()

database_file = args.db_input_file
csv_file = args.csv_input_file
round = args.round

field1 = "r" + str(round) + "_overall_position"
field2 = "r" + str(round) + "_cat_position"

print("Updating database:",database_file,"with",csv_file,"for round",round)

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
c = conn.cursor()

# Open the CSV file and create a CSV reader object
with open(csv_file, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)

    # Iterate over each row in the CSV file
    for row in csvreader:
        # Extract data from the row
        rider_number = row[1]  # Rider number is second field of CSV file
        updated_field1 = row[0]  # Overall position is first column of CSV file
        updated_field2 = row[6]  # Category position is 7th field of CSV file

#        print ("rider_number",rider_number," Overall position",updated_field1," Cat position",updated_field2)
        # Execute SQL UPDATE statement to modify specific fields based on rider number
        c.execute(f'''UPDATE riders
                     SET {field1} = ?, {field2} = ?
                     WHERE race_number = ?''', (updated_field1, updated_field2, rider_number))
        if c.rowcount > 0:
            conn.commit()
#            print("Update successful with rider_number", rider_number)
        else:
            print("Exception: No rows were updated with rider_number", rider_number)


# Commit changes and close connection
conn.commit()
conn.close()

print("Fields updated successfully!")
