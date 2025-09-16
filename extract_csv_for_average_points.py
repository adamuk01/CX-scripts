#!/usr/bin/python3

# This output certain file from the allrider.csv file for Run and Ride.

import csv
import argparse

# Specify the desired columns and their order
DESIRED_COLUMNS = ["Entry type", "Last name", "First name", "Membership number"]

def filter_csv(input_file, output_file):
    """Filter and write specific columns from the input CSV to the output CSV."""
    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        # Verify if all desired columns exist in the input file
        missing_columns = [col for col in DESIRED_COLUMNS if col not in reader.fieldnames]
        if missing_columns:
            raise ValueError(f"Missing columns in input file: {', '.join(missing_columns)}")

        # Open the output file for writing
        with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=DESIRED_COLUMNS)

            # Write the header row
            writer.writeheader()

            # Write filtered rows
            for row in reader:
                filtered_row = {col: row[col] for col in DESIRED_COLUMNS}
                writer.writerow(filtered_row)

    print(f"Filtered data written to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Filter specific columns from a CSV file.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("output_file", type=str, help="Path to the output CSV file.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to filter the CSV
    filter_csv(args.input_file, args.output_file)

if __name__ == "__main__":
    main()





