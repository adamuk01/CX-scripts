#!/usr/bin/python3

# REMEMBER to remove the first line.... the head is junk and not needed!
#Fields are:

# Race Number,First name,Surname,Gender,Category,Club,Total Score,Races entered,R1,R2,r£,R4,R5,R6,R7,R8,R9,R10,R11,R12

import csv
import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Import initial rider data into race database")
parser.add_argument("input_file", help="Path to the DB file")
parser.add_argument("csv_input_file", help="Path to CSV file")
args = parser.parse_args()

database_file = args.input_file
csv_file = args.csv_input_file

print ("Loading data from",csv_file,"into database",database_file)

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
c = conn.cursor()

# Open the CSV file and create a CSV reader object
with open(csv_file, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Iterate over each row in the CSV file
    for row in csvreader:
        # Assuming the first 7 columns of the CSV file correspond to the first 7 columns of the database table
        # You can adjust the indices according to the structure of your CSV file and database table
        
        # Extract data from the row
        race_number = row[0]
        firstname = row[1]
        surname = row[2]
        gender = row[3]
        race_category = row[4]
        club_name = row[5]
        total_points_last_year = row[6]
        races_finished_last_year = row[7]
        r1_points = row[8]
        r2_points = row[9]
        r3_points = row[10]
        r4_points = row[11]
        r5_points = row[12]
        r6_points = row[13]
        r7_points = row[14]
        r8_points = row[15]
        r9_points = row[16]
        r10_points = row[17]
        r11_points = row[18]
        r12_points = row[19]

        print (surname)
        
        # Insert data into the database table, specifying the columns explicitly
        c.execute('''INSERT INTO riders (race_number, firstname, surname, gender, race_category, club_name, total_points_last_year, races_finished_last_year, r1_points, r2_points, r3_points, r4_points, r5_points, r6_points, r7_points, r8_points, r9_points, r10_points, r11_points, r12_points  ) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (race_number, firstname, surname, gender, race_category, club_name, total_points_last_year, races_finished_last_year, r1_points, r2_points, r3_points, r4_points, r5_points, r6_points, r7_points, r8_points, r9_points, r10_points, r11_points, r12_points ))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data imported successfully!")

