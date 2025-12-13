
import bcrypt
import pandas as pd
from pathlib import Path
import sqlite3
import os


def connect_database():
    """Connect to SQLite database."""
    db_path = r"C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\multi_domain_platform\intelligence_platform.db"
    return sqlite3.connect(db_path)


def load_csv_to_table(csv_path, table_name):
    """Load CSV data into database table"""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f" CSV file not found: {csv_path}")
        return 0

    conn = connect_database()

    try:
        # Check if table has data
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"  Skipping {table_name} - already has {count} rows")
            return 0

        df = pd.read_csv(csv_path)
        rows_loaded = df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
        print(f" Loaded {rows_loaded} rows into {table_name} table")
        return rows_loaded
    except Exception as e:
        print(f"Error loading {csv_path}: {e}")
        return 0
    finally:
        conn.close()


def load_all_csv_data():
    """Load all CSV files into database"""
    # Update paths to  OOP DATA folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, "OOP DATA")

    csv_files = {
        'cyber_incidents': os.path.join(data_folder, 'cyber_incidents.csv'),
        'datasets_metadata': os.path.join(data_folder, 'datasets_metadata.csv'),
        'it_tickets': os.path.join(data_folder, 'it_tickets.csv')
    }

    total_rows = 0
    for table_name, csv_path in csv_files.items():
        rows_loaded = load_csv_to_table(csv_path, table_name)
        total_rows += rows_loaded

    print(f"\nTotal rows loaded: {total_rows}")
    return total_rows


if __name__ == "__main__":
    load_all_csv_data()