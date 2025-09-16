#!/usr/bin/python3

# This will chop the last field of the CSV file. Only use this after week 3 or so  the field - "last years average" is removed.

import csv
import sys
import os

def chop_last_field(filename):
    # Create a temporary output file
    temp_file = filename + '.tmp'

    with open(filename, 'r', newline='') as infile, open(temp_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Remove the last field from each row
            new_row = row[:-1]
            # Write the updated row to the temp file
            writer.writerow(new_row)

    # Replace the original file with the modified temp file
    os.replace(temp_file, filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chop-last-field-csv.py <filename>")
    else:
        filename = sys.argv[1]
        chop_last_field(filename)


