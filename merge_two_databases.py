#!/usr/bin/env python3

import sqlite3
import argparse
import shutil
import os

def merge_riders_table(source_db, new_riders_db, output_db):
    # Copy source_db to output_db to avoid modifying originals
    shutil.copy2(source_db, output_db)

    # Connect to both databases
    dest_conn = sqlite3.connect(output_db)
    dest_cursor = dest_conn.cursor()

    new_conn = sqlite3.connect(new_riders_db)
    new_cursor = new_conn.cursor()

    # Read column names from riders table
    new_cursor.execute("PRAGMA table_info(riders);")
    columns = new_cursor.fetchall()
    all_columns = [col[1] for col in columns]

    # Exclude 'id' column
    insert_columns = [col for col in all_columns if col != 'id']
    columns_str = ', '.join(insert_columns)
    placeholders = ', '.join('?' for _ in insert_columns)

    # Fetch data from new riders, excluding 'id'
    new_cursor.execute(f"SELECT {columns_str} FROM riders;")
    rows = new_cursor.fetchall()

    # Count existing rows before merge
    dest_cursor.execute("SELECT COUNT(*) FROM riders;")
    before_count = dest_cursor.fetchone()[0]

    # Insert into destination DB
    inserted = 0
    for row in rows:
        try:
            dest_cursor.execute(f"INSERT INTO riders ({columns_str}) VALUES ({placeholders})", row)
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # Skip duplicate or conflicting rows

    # Count after merge
    dest_cursor.execute("SELECT COUNT(*) FROM riders;")
    after_count = dest_cursor.fetchone()[0]

    # Close connections
    dest_conn.commit()
    dest_conn.close()
    new_conn.close()

    # Print summary
    print("✅ Merge Complete: Output written to", output_db)
    print()
    print("📄 Source DB:", source_db)
    print(f"  - riders: {before_count} rows before merge")
    print("📄 New Riders DB:", new_riders_db)
    print(f"  - New rows inserted: {inserted}")
    print(f"📄 Final Total in Merged DB: {after_count} rows")

def main():
    parser = argparse.ArgumentParser(description="Merge new riders into existing SQLite DB")
    parser.add_argument("source_db", help="Path to original DB (e.g. main riders DB)")
    parser.add_argument("new_riders_db", help="Path to new riders DB to merge in")
    args = parser.parse_args()

    output_db = os.path.splitext(args.source_db)[0] + "-merged.db"
    merge_riders_table(args.source_db, args.new_riders_db, output_db)

if __name__ == "__main__":
    main()

