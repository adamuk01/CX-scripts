#!/usr/bin/python3

# Do not use! Just for reference

# This will take the CSV file, you give it the lines to exclude and it will remove those lines and shuffle up the ranking.
# Idea is to remove the non league riders from the CSV results file first
# e.g  ./filter_results.py VetsRound11.csv 5 14 18 22 32 37 41 46 48 76 89 95

import csv
import argparse

def remove_and_reorder(csv_file, lines_to_remove):
    # Read CSV file into a list of dictionaries
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Remove lines to be excluded and update rankings
    updated_data = []
    removed_ranks = set(lines_to_remove)
    for row in data:
        if int(row['Pos']) not in removed_ranks:
            updated_data.append(row)

    # Reorder remaining lines based on rankings
    updated_data.sort(key=lambda x: int(x['Pos']))

    # Update rank values
    for i, row in enumerate(updated_data, start=1):
        row['Pos'] = str(i)

    # Write modified data back to CSV file
    with open('nonleague-filtered_' + csv_file, 'w', newline='') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove and reorder lines in a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("lines_to_remove", nargs="+", type=int, help="Lines to remove (rankings)")
    args = parser.parse_args()

    input_file = args.input_file
    lines_to_remove = args.lines_to_remove

    remove_and_reorder(input_file, lines_to_remove)

