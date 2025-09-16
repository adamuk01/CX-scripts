#!/usr/bin/python3

# This will look at the race file & check their race number - if > 900 they are not a member so field 4 should be FALSE. If however < 879 - they are a member so should be TRUE
import csv
import sys

# Function to process each row
def process_row(row, line_number):
    try:
        # Convert field 14 to integer
        value = int(row[13])
        # Check if value is greater than 900
        if value > 899:
            row[4] = 'FALSE'
        else:
            row[4] = 'TRUE'
    except ValueError:
        print(f"Error: Invalid data in field 14 on line {line_number}: {row}")
    return row

# Read the input CSV and process it
def update_csv(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        rows = []
        header = next(reader)  # Skip the header
        rows.append(header)    # Keep the header in the output file

        for i, row in enumerate(reader, start=2):  # Start from line 2 to account for the header
            processed_row = process_row(row, i)
            rows.append(processed_row)

    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

    print(f"CSV processing complete. Updated file saved as {output_file}")

# Main function to handle command line arguments
def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_csv> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        update_csv(input_file, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

