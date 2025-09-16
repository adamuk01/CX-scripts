#!/usr/bin/python3

# This takes the CSV input file and changes the Position toa sequential nmumber
import argparse
import csv

def update_csv(csv_file):
    # Read the CSV file
    data = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header line
        for row in reader:
            data.append(row)

    # Update the values in the first column ("position")
    for i, row in enumerate(data, start=1):
        row[0] = str(i)  # Update the value in the first column to the sequential number

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write back the header line
        writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update CSV file by changing the values in the first column to sequential numbers")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    update_csv(args.csv_file)

