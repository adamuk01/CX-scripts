#!/usr/bin/bash

# Validate the race number in the CSV file matches the race number in the datbase!
# Filtered RiderHQ file - called "allRiders.csv" should be present

# Set PATH to include binary
PATH=$PATH:../bin
riderHQfilecat=allRiders+cat.csv

for db in *.db
do
	echo "Checking database: $db"
	validate_csv_against_db.py $db $riderHQfilecat
done

