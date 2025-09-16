#!/usr/bin/python3
import sqlite3
import csv
import argparse

# Load data from the SQLite database
def load_db_data(db_path):
    """
    Loads rider data from an SQLite database.
    
    Args:
    - db_path: Path to the SQLite database file.
    
    Returns:
    - A dictionary where the keys are (firstname, surname) tuples and the values are tuples of race numbers, race categories, and gender.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT race_number, firstname, surname, race_category_current_year, gender FROM riders"
    cursor.execute(query)
    db_data = cursor.fetchall()  # Fetch all data from the query
    conn.close()
    
    # Normalize database data (convert to lowercase, strip spaces)
    normalized_db_data = {
        (first_name.strip().lower(), surname.strip().lower()): (str(race_number).strip(), race_category.strip(), gender.strip().upper())
        for race_number, first_name, surname, race_category, gender in db_data
    }
    
    return normalized_db_data

# Load data from the CSV file with field presence checks
def load_csv_data(csv_path):
    """
    Loads rider data from a CSV file, ensuring that required fields are present.
    
    Args:
    - csv_path: Path to the CSV file.
    
    Returns:
    - A dictionary where the keys are (firstname, surname) tuples and the values are tuples of bib numbers (membership numbers), age categories, and sex.
    """
    required_fields = ['Membership number', 'First name', 'Last name', 'Age Category', 'sex']
    csv_data = {}
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in reader.fieldnames]
        if missing_fields:
            print(f"Warning: The following required fields are missing in the CSV file: {', '.join(missing_fields)}")

        for row in reader:
            # Only attempt to access fields that exist
            bib_number = row["Membership number"].strip() if "Membership number" in row else None
            first_name = row["First name"].strip().lower() if "First name" in row else None
            last_name = row["Last name"].strip().lower() if "Last name" in row else None
            age_category = row["Age Category"].strip() if "Age Category" in row else None
            sex = row["sex"].strip().upper() if "sex" in row else None

            if first_name and last_name:
                csv_data[(first_name, last_name)] = (bib_number, age_category, sex)
                
    return csv_data

# Helper function to extract base category (e.g., U8 from U8M, U8F)
def extract_base_category(category):
    """
    Extracts the base age category by removing gender suffixes (e.g., M or F).
    
    Args:
    - category: The race category (e.g., U8M, U8F).
    
    Returns:
    - The base category without any suffix (e.g., U8).
    """
    return category[:-1] if category and category[-1] in ['M', 'F'] else category

# Compare data between database and CSV
def compare_data(db_data, csv_data):
    """
    Compares the race numbers, race categories, and gender/sex between the SQLite database and CSV file.
    
    Args:
    - db_data: Dictionary with data from the SQLite database.
    - csv_data: Dictionary with data from the CSV file.
    
    Returns:
    - A list of mismatches where race numbers, age categories, or gender/sex differ.
    - The total number of entries compared.
    """
    mismatches = []
    total_comparisons = 0
    
    # Compare database entries to CSV
    for name_key in db_data:
        total_comparisons += 1
        db_bib_number, db_race_category, db_gender = db_data[name_key]
        csv_bib_number, csv_age_category, csv_sex = csv_data.get(name_key, (None, None, None))
        
        # Compare race numbers if present
        if csv_bib_number and db_bib_number != csv_bib_number:
            mismatches.append({
                "first_name": name_key[0],
                "surname": name_key[1],
                "db_bib_number": db_bib_number,
                "csv_bib_number": csv_bib_number
            })
        
        # Compare race categories (base categories only)
        if csv_age_category:
            db_base_category = extract_base_category(db_race_category)
            if db_base_category != csv_age_category:
                mismatches.append({
                    "first_name": name_key[0],
                    "surname": name_key[1],
                    "db_race_category": db_race_category,
                    "csv_age_category": csv_age_category
                })

        # Compare gender and sex if present
        if csv_sex and db_gender != csv_sex:
            mismatches.append({
                "first_name": name_key[0],
                "surname": name_key[1],
                "db_gender": db_gender,
                "csv_sex": csv_sex
            })
    
    return mismatches, total_comparisons

# Main function to handle arguments and run the comparison
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Compare SQLite database and CSV file for matching entries.")
    parser.add_argument("db_path", help="Path to the SQLite database file.")
    parser.add_argument("csv_path", help="Path to the CSV file.")
    args = parser.parse_args()

    # Load data from the database and the CSV file
    db_data = load_db_data(args.db_path)
    csv_data = load_csv_data(args.csv_path)

    # Compare the data
    mismatches, total_comparisons = compare_data(db_data, csv_data)

    # Display mismatches
    if mismatches:
        print("Rows where race number, race category, or gender/sex do not match between database and CSV:")
        for mismatch in mismatches:
            print(f"First Name: {mismatch['first_name']}, Surname: {mismatch['surname']}")
            if "db_bib_number" in mismatch:
                print(f"  - Database Race Number: {mismatch['db_bib_number']}")
                print(f"  - CSV Bib Number: {mismatch['csv_bib_number']}")
            if "db_race_category" in mismatch:
                print(f"  - Database Race Category: {mismatch['db_race_category']}")
                print(f"  - CSV Age Category: {mismatch['csv_age_category']}")
            if "db_gender" in mismatch:
                print(f"  - Database Gender: {mismatch['db_gender']}")
                print(f"  - CSV sex: {mismatch['csv_sex']}")
    else:
        print("No mismatches found.")

    # Summary of the operation
    print("\nSummary:")
    print(f"Total comparisons made: {total_comparisons}")
    print(f"Mismatches found: {len(mismatches)}")

if __name__ == "__main__":
    main()

