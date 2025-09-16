#!/usr/bin/python3

# This will calculate the points for each round for the riders. It bases it on category position
# WOMEN ONLY! THey have different cagegory/field

import csv
import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Load result data into race database")
parser.add_argument("db_input_file", help="Path to the DB file")
parser.add_argument("round", type=int, help="Week or Round number")
args = parser.parse_args()

database_file = args.db_input_file
round = args.round

field1 = "r" + str(round) + "_overall_position"
#field1 = "r" + str(round) + "_cat_position"
field2 = "r" + str(round) + "_points"

print("Updating database:",database_file,"for round",round)

def calculate_points(position):
    # Check if position is null
    if position is None:
        return 0  # or any other value you want to return for null positions

    # Calculate points based on finishing position
    return max(0, 100 - position + 1)

def record_points(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch riders' positions from the database
#    cursor.execute("SELECT race_number, position FROM riders")
    query = f"SELECT race_number, {field1} FROM riders "
#    print (query)
    cursor.execute(query)
    rows = cursor.fetchall()
#    print (rows)

    # Update points for each rider based on their position
    for row in rows:
        race_number, position = row
        points = calculate_points(position)
        cursor.execute(f"UPDATE riders SET {field2} = ? WHERE race_number = ?", (points, race_number))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

record_points(database_file)

print("Womens New points calculated successfully!")
