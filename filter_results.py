#!/usr/bin/python3

# This will take the CSV file, remove any race number > 900 and shuffle up the ranking. It only adjusts the Position - not the category ranking (done by another script)
# Idea is to remove the non league riders from the CSV results file first

import csv
import argparse

def remove_null_first_column(input_file, output_file):
    with open(csv_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        header = next(reader)
        writer.writerow(header)

        # Write rows with non-null first column
        for row in reader:
            if row and row[0].strip() != "":
                writer.writerow(row)



def filter_and_reorder(csv_file, csv_output_file):
    # Read CSV file into a list of dictionaries
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Remove lines where the value in the second field is greater than 900
    filtered_data = [row for row in data if int(row['Race No']) < 900]
#        for row in data:
#          try:
#            # Attempt to convert the 'Race No' field to an integer
#            race_no = int(row['Race No'])
#            if race_no < 900:
#                print(f"Valid Race No: {race_no}")
#          except ValueError as e:
#            # Handle cases where conversion fails
#            print(f"Invalid value for 'Race No': {row['Race No']}, Error: {e}")


    # Reorder remaining lines based on rankings
    filtered_data.sort(key=lambda x: int(x['Pos']))

    # Update rankings
    for i, row in enumerate(filtered_data, start=1):
        row['Pos'] = str(i)

    # Write modified data back to CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter lines based on the second field being greater than 900 and reorder rankings in a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    csv_file = args.csv_file
    csv_output_file = 'modified' + csv_file
    remove_null_first_column(csv_file, csv_output_file)
    filter_and_reorder(csv_output_file, csv_file)



