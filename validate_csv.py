#!/usr/bin/python3

# Check the CSV file for any missing fields. Then report them.
# Also check for duplicate lines AND duplicate names (if they entered twice)
# Membership ID is the BC number
# Membership number is their WMCCL race number & we must have one for members

import csv

def validate_csv(csv_file):
    issues = []
    seen_rows = set()
    seen_names = set()

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)

        for line_num, row in enumerate(reader, start=2):  # Start from line 2
            row_tuple = tuple(row.items())

            # Check for duplicate rows
            if row_tuple in seen_rows:
                issues.append(f"Line {line_num}: Duplicate row found.")
            else:
                seen_rows.add(row_tuple)

            # Extract fields from CSV
            for key, value in row.items():
                value = value.strip()  # Remove leading/trailing spaces
                if not value:
                    issues.append(f"Line {line_num}: '{key}' is blank.")

            # Extract specific fields for additional checks
            first_name = row.get("First name", "").strip()
            last_name = row.get("Last name", "").strip()
            has_membership = row.get("Are you a member of British Cycling?", "").strip().upper()
            membership_number = row.get("Membership number", "").strip()

            # Check for blank fields
            if not first_name:
                issues.append(f"Line {line_num}: 'First name' is blank.")
            if not last_name:
                issues.append(f"Line {line_num}: 'Last name' is blank.")
            if has_membership == "TRUE" and not membership_number:
                issues.append(f"Line {line_num}: 'Has membership' is TRUE but 'Membership number' is blank.")

            # Check for duplicate first name and last name
            name = (first_name, last_name)
            if name in seen_names:
                issues.append(f"Line {line_num}: Duplicate 'First name' and 'Last name' combination found.")
            else:
                seen_names.add(name)

    return issues

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate CSV file and report issues")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    issues = validate_csv(args.csv_file)

    if issues:
        print("Validation failed. Issues found:")
        for issue in issues:
            print(issue)
    else:
        print("CSV file is valid. No issues found.")

