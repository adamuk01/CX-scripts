#!/usr/bin/python3

# This sets the first character of a specific field to be uppercase!
# Edit the fields below - like firstname or surname etc..

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Import initial rider data into race database")
parser.add_argument("input_file", help="Path to the DB file")

args = parser.parse_args()
database_file = args.input_file

print ("Checking database for capitals database:",database_file)

def capitalize_text_field(conn, table_name, text_field_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT rowid, {text_field_name} FROM {table_name}")
    rows = cursor.fetchall()

    for rowid, text_field_value in rows:
        if text_field_value:
            fixed_value = text_field_value.title()
            if fixed_value != text_field_value:
                print(f"Fixing: {text_field_value} → {fixed_value}")
                cursor.execute(
                    f"UPDATE {table_name} SET {text_field_name} = ? WHERE rowid = ?",
                    (fixed_value, rowid)
                )

    conn.commit()

# Connect to the SQLite database
conn = sqlite3.connect(database_file)

# Specify the table name and the text field name to be processed
table_name = 'riders'

text_field_name = 'firstname'
# Call the function to capitalize the text field
capitalize_text_field(conn, table_name, text_field_name)

text_field_name = 'surname'
# Call the function to capitalize the text field
capitalize_text_field(conn, table_name, text_field_name)

# Close the database connection
conn.close()
