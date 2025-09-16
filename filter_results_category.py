#!/usr/bin/python3

# This will take the CSV file from D3tech and filter out the non-legue riders and then shuffle the number up for the league riders
# It only adjusts their category position. Not their position in the race!
# I assume a rider with a race number > 899 is a non-league member
# WE DO NOT NEED TO DO THIS TO THE WOMEN! 

import csv
import argparse

def filter_and_reorder(csv_file):
    # Read CSV file into a list of dictionaries
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Remove lines where the value in the second field is greater than 900
    filtered_data = [row for row in data if int(row['Race No']) <= 900]

    # Reorder remaining lines based on rankings
    filtered_data.sort(key=lambda x: int(x['Cat Pos']))

    # Update rankings
    for i, row in enumerate(filtered_data, start=1):
        row['Cat Pos'] = str(i)

    # Write modified data back to CSV file
    with open('modified_' + csv_file, 'w', newline='') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter lines based on the second field being greater than 900 and reorder rankings in a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    csv_file = args.csv_file
    filter_and_reorder(csv_file)

