#!/usr/bin/python3

# This will merge ALL the seperate databases into a single database so they can all be counted for example


import sqlite3

def merge_databases(source_dbs, destination_db):
    # Connect to the destination database
    dest_conn = sqlite3.connect(destination_db)
    dest_cursor = dest_conn.cursor()

    # Iterate over source databases
    for source_db in source_dbs:
        # Connect to the source database
        source_conn = sqlite3.connect(source_db)
        source_cursor = source_conn.cursor()

        # Extract table names from source database
        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        # Iterate over tables in the source database
        for table in tables:
            table_name = table[0]
            # Extract schema information for the table
            source_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = source_cursor.fetchall()

            # Create corresponding table in the destination database
            dest_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join([f'{col[1]} {col[2]}' for col in columns])});")

            # Copy data from source table to destination table
            source_cursor.execute(f"SELECT * FROM {table_name};")
            rows = source_cursor.fetchall()
            dest_cursor.executemany(f"INSERT INTO {table_name} VALUES ({','.join(['?' for _ in range(len(columns))])});", rows)

        # Commit changes and close connections for the source database
        source_conn.commit()
        source_conn.close()

    # Commit changes and close connections for the destination database
    dest_conn.commit()
    dest_conn.close()

if __name__ == "__main__":
    # Provide paths to the source databases and the destination database
    source_databases = ["U8.db", "U10.db", "Women.db", "U12.db", "Senior.db", "Vet50.db", "Youth.db"]
    destination_database = "AllRidersMerged.db"

    merge_databases(source_databases, destination_database)

