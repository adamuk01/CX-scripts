#!/usr/bin/python3

# REMEMBER to remove the first line.... the head is junk and not needed!
#Fields are:

# Event,Unique ID,Race Number,First name,Last name,,Membership type,Membership ID,gender,Date of birth,One Bike?,Club Name,YOB,Age,Category,,Secondary Category,League Category,,



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
        riderHQ_id = row[1]
        race_number = row[2]
        firstname = row[3]
        surname = row[4]
        BC_number = row[7]
        gender = row[8]
        DOB = row[9]
        IBX = row[10]
        club_name = row[11]
        YOB = row[12]
        race_category_previous_year = row[17]
        
        # Insert data into the database table, specifying the columns explicitly
        c.execute('''INSERT INTO riders (riderHQ_id, race_number, firstname, surname, BC_number, gender, DOB, IBX, club_name, YOB, race_category_previous_year) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (riderHQ_id, race_number, firstname, surname, BC_number, gender, DOB, IBX, club_name, YOB, race_category_previous_year))

# Commit changes and close connection
conn.commit()
conn.close()

print("Data imported successfully!")

