#!/usr/bin/python3

# Output the League tables for a single category. 

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Dump the league tables from the DB file.")
parser.add_argument("input_file", help="Path to the input DB file")
parser.add_argument("category", help="Race Category, e.g Under 8 or Under 6 or Vet 50-59 - must be full category in quotes")
args = parser.parse_args()

db_file = args.input_file
category = args.category

print("Creating CSV file for League tables from ",db_file,"with current values for",category)

import sqlite3
import csv


def dump_to_csv(db_file, table_name,fields, category):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Execute SELECT query to fetch specific fields and sort the data - Female first:
    query = f"SELECT firstname || ' ' || surname AS full_name, {', '.join(fields)} FROM {table_name} WHERE race_category_current_year LIKE '%{category}%' ORDER by best_X_points DESC"
    cursor.execute(query)

    # Fetch the sorted data
    data = cursor.fetchall()

    # Write the data to a CSV file
    csv_file = f"{category}-leaguetable.csv"
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)

    # Write header row
        writer.writerow(['Position','Fullname', *fields])
        
     # Write data rows with count at the start of each line
        for count, row in enumerate(data, start=1):
            writer.writerow([count] + list(row))

    conn.close()

# Example usage:
table_name = 'riders'
#fields = ['full_name', 'race_number', 'club_name', 'race_category', 'gender', 'final_position_last_year', 'average_position', 'races_finished']  # Specify the fields you want to select
#fields = ['firstname', 'surname', 'race_number', 'race_category_current_year', 'gender', 'club_name', 'IBX', 'best_X_points', 'r1_points', 'r2_points', 'r3_points', 'r4_points', 'r5_points', 'r6_points', 'r7_points', 'r8_points', 'r9_points', 'r10_points', 'r11_points', 'r12_points']
fields = ['race_number', 'race_category_current_year', 'club_name', 'IBX', 'best_X_points', 'average_points', 'r1_points', 'r2_points', 'r3_points', 'r4_points', 'r5_points', 'r6_points', 'r7_points', 'r8_points', 'r9_points', 'r10_points', 'r11_points', 'r12_points']

dump_to_csv(db_file, table_name, fields, category)

