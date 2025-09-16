#!/usr/bin/python3
"""
validate_category_by_race_number.py

This script checks a race CSV file to ensure each rider's "Entry type"
matches the expected type for their "Membership number" range.

- Reports mismatches (wrong category for number range).
- Reports invalid rows (missing or non-numeric membership numbers).
- Prints a summary at the end.
"""

import csv
import sys

# Define the ranges and corresponding entry types
criteria = {
    (1, 69): "Under 8",
    (70, 129): "Under 10",
    (130, 199): "Under 12",
    (200, 249): "Youth (U-14 & U-16)",
    (250, 299): "Youth (U-14 & U-16)",
    (300, 459): "Masters 50+ Open",
    (460, 559): "Masters 50+ Open",
    (560, 569): "Junior Female",
    (580, 591): "Senior/Masters Female",
    (610, 634): "Senior/Masters Female",
    (690, 706): "Junior Open",
    (720, 799): "Senior Open",
    (800, 879): "Masters 40-49 Open"
    # Add more ranges as needed
}

def check_entry_type(file_path):
    mismatches = []
    invalid_rows = []
    total_rows = 0

    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                total_rows += 1
                raw_number = row['Membership number'].strip()
                entry_type = row['Entry type']

                # Handle invalid membership numbers
                if not raw_number.isdigit():
                    invalid_rows.append(row)
                    print(f"Invalid row: Membership number='{raw_number}', Entry type='{entry_type}'")
                    continue

                race_number = int(raw_number)

                # Check against criteria
                for race_range, expected_entry_type in criteria.items():
                    if race_range[0] <= race_number <= race_range[1]:
                        if entry_type != expected_entry_type:
                            mismatches.append((race_number, entry_type, expected_entry_type))
                            print(
                                f"Mismatch found: Race Number {race_number} "
                                f"has Entry Type '{entry_type}' but expected '{expected_entry_type}'"
                            )
                        break  # Stop once the range is matched

        # --- Summary ---
        print("\n--- Summary ---")
        print(f"Total rows checked: {total_rows}")
        print(f"Mismatches: {len(mismatches)}")
        print(f"Invalid rows: {len(invalid_rows)}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_category_by_race_number.py <csv_file>")
    else:
        file_path = sys.argv[1]
        check_entry_type(file_path)

