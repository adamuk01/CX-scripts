#!/usr/bin/python3

# This really is a work in progress, depends what I get from RiderHQ - at the moment this take the race results...
# REMEMBER to remove the first header line.... the head is junk and not needed!

import csv
import sqlite3
import argparse

from datetime import datetime


def get_year(date_str):
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_str, '%m/%d/%y')
        original_year = date_obj.year % 100  # Extract the two-digit year
        current_year = datetime.now().year
        current_century = current_year // 100 * 100

        # Determine the correct century
        if original_year <= current_year % 100:
            adjusted_year = original_year + current_century
        else:
            adjusted_year = original_year + current_century - 100

        # Print debug information
        print(f"Original Year (2-digit): {original_year}, Adjusted Year: {adjusted_year}")

        return str(adjusted_year)
    except ValueError as e:
        # Print the error and the input string
        print(f"Error: {e}. Input date: {date_str}")
        return None

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
        
        # Extract data from the row - This needs updating, based on the fields from RiderHQ - rememeber starts from zero.
        BC_number = row[9]
        race_number = row[1]
        firstname = row[2]
        surname = row[3]
        gender = row[7]
        club_name = row[4]
        race_category_current_year = row[6]
        IBX = row[18]
        DOB = row[10]
        YOB = (get_year(row[10]))

        # Insert data into the database table, specifying the columns explicitly
        c.execute('''INSERT INTO riders ( BC_number, race_number, firstname, surname, gender, club_name, race_category_current_year, DOB, YOB,
                                          IBX)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ( BC_number, race_number, firstname, surname, gender, club_name, race_category_current_year, DOB, YOB,
                                          IBX))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data imported successfully!")

