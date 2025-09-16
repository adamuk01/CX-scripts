#!/usr/bin/env python3
#!/usr/bin/env python3

import sqlite3
import argparse

def fetch_table_as_dict(db_path, table, key_field):
    """
    Fetches all rows from the specified table in a database and returns them
    as a dictionary keyed by the unique field (e.g., race_number or id).

    Args:
        db_path (str): Path to the SQLite database.
        table (str): Table name to fetch from.
        key_field (str): The field to use as the dictionary key.

    Returns:
        dict: {key_field_value: {column_name: value, ...}}
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()

    return {row[key_field]: dict(row) for row in rows}

def diff_databases(db1_path, db2_path, table="riders", key_field="race_number"):
    """
    Compares the contents of a table in two SQLite databases.

    Args:
        db1_path (str): Path to the first (original) database.
        db2_path (str): Path to the second (new) database.
        table (str): Table name to compare.
        key_field (str): Unique identifier field to use for comparison.

    Prints:
        Lists of added, removed, and changed rows.
    """
    db1_data = fetch_table_as_dict(db1_path, table, key_field)
    db2_data = fetch_table_as_dict(db2_path, table, key_field)

    all_keys = set(db1_data.keys()).union(db2_data.keys())

    added = []
    removed = []
    changed = []

    for key in sorted(all_keys):
        row1 = db1_data.get(key)
        row2 = db2_data.get(key)

        if row1 and not row2:
            removed.append(key)
        elif row2 and not row1:
            added.append(key)
        elif row1 != row2:
            changed.append((key, row1, row2))

    print(f"🔍 Comparing table '{table}' by key '{key_field}'")
    print(f"📂 DB1: {db1_path}")
    print(f"📂 DB2: {db2_path}\n")

    print("📥 Added records:")
    if added:
        for key in added:
            print(f"  + {key}")
    else:
        print("  (none)")

    print("\n🗑️ Removed records:")
    if removed:
        for key in removed:
            print(f"  - {key}")
    else:
        print("  (none)")

    print("\n✏️ Changed records:")
    if changed:
        for key, r1, r2 in changed:
            print(f"  ~ {key}")
            for field in r1:
                if r1[field] != r2[field]:
                    print(f"     {field}: '{r1[field]}' → '{r2[field]}'")
    else:
        print("  (none)")

    print("\n✅ Done.")

def main():
    parser = argparse.ArgumentParser(description="Diff two SQLite databases with identical schemas.")
    parser.add_argument("db1", help="Path to the first (original) SQLite database")
    parser.add_argument("db2", help="Path to the second (new/modified) SQLite database")
    parser.add_argument("--table", default="riders", help="Name of the table to compare (default: riders)")
    parser.add_argument("--key", default="id", help="Primary key field for diff (default: id)")
    args = parser.parse_args()

    diff_databases(args.db1, args.db2, table=args.table, key_field=args.key)

if __name__ == "__main__":
    main()

