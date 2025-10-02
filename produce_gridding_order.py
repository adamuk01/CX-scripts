#!/usr/bin/python3

# Output the gridding position. This is a complete dump, based on average position - but if this is null/zero, it uses final_position_last_year

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Update race average in DB file.")
parser.add_argument("input_file", help="Path to the input DB file")
args = parser.parse_args()

db_file = args.input_file

print("Creating CSV file for gridding",db_file,"with current values")

import sqlite3
import csv


def dump_to_csv(db_file, table_name,fields):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Execute SELECT query to fetch specific fields and sort the data
#    query = f"SELECT {', '.join(fields)}, firstname || ' ' || surname AS full_name, COALESCE(average_points, average_points_last_year) AS final_race_position FROM {table_name}     ORDER BY COALESCE(average_points, average_points_last_year) DESC NULLS LAST"
#    print ("Query:", query)
    query = f"""
SELECT {', '.join(fields)},
       firstname || ' ' || surname AS full_name,
       COALESCE(NULLIF(average_points, 0), average_points_last_year) AS final_points
FROM {table_name}
ORDER BY (final_points IS NULL) ASC, final_points DESC
"""
#    print ("Query:", query)

    cursor.execute(query)

    # Fetch the sorted data
    data = cursor.fetchall()

    # Write the data to a CSV file
    csv_file = f"{db_file}-gridding.csv"
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)

    # Write header row
        writer.writerow(['Pos','Full name','Race No.','Club', 'Cat','Gender','Av. Points','LY points'])
#        writer.writerow(['Position', *fields])
        
     # Write data rows with count at the start of each line
        for count, row in enumerate(data, start=1):
#            #writer.writerow([count] + list(row[2:]))
#            writer.writerow([count] + list(row[7:8]) + list(row[2:7]))
            writer.writerow([count] + list(row[8:9]) + list(row[2:8]))

    conn.close()

# Example usage:
table_name = 'riders'
#fields = ['full_name', 'race_number', 'club_name', 'race_category', 'gender', 'final_position_last_year', 'average_position']  # Specify the fields you want to select
fields = ['firstname', 'surname', 'race_number', 'club_name', 'race_category_current_year', 'gender', 'average_points', 'average_points_last_year' ]  # Specify the fields you want to select

dump_to_csv(db_file, table_name, fields)

# Can't add this line yet as we have non-league riders to add...
#csv_file = f"{db_file}-gridding.csv"
#f = open(csv_file, "a")
#print(",Any other rider not called.", file=f)
#f.close()
