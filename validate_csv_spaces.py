#!/bin/python3
# Check the CSV file for space in a field before the comma


import csv
import sys

def check_and_fix_csv(csv_file):
    lines_with_space = []

    # Check for lines with space at the end of a field and store them
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for line_number, line in enumerate(csv_reader, start=1):
            has_space = False
            for field_number, field in enumerate(line, start=1):
                if field.endswith(' '):
                    has_space = True
                    break
            if has_space:
                lines_with_space.append((line_number, line))

    if lines_with_space:
        print("Lines with space at the end of a field:")
        for line_number, line in lines_with_space:
            print(f"Line {line_number}: {','.join(line)}")  # Output the line with the space

        # Rewrite the file without the space for lines with spaces
        with open(csv_file, 'r', newline='') as file:
            with open('corrected_' + csv_file, 'w', newline='') as corrected_file:
                csv_reader = csv.reader(file)
                csv_writer = csv.writer(corrected_file)
                for line_number, line in enumerate(csv_reader, start=1):
                    if (line_number, line) in lines_with_space:
                        # Remove space at the end of each field
                        line = [field.rstrip() for field in line]
                    csv_writer.writerow(line)
        print(f"File '{csv_file}' has been corrected and saved as 'corrected_{csv_file}'.")
    else:
        print("No lines found with space at the end of a field.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
    else:
        csv_file = sys.argv[1]
        check_and_fix_csv(csv_file)

