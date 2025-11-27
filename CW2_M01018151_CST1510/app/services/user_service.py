import bcrypt
import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table


def register_user(username, password, role="user"):
    """Register a new user."""
    conn = connect_database()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    """Authenticate a user."""
    user = get_user_by_username(username)
    if not user:
        return False, "Username not found."

    # Verify password (user[2] is password_hash column)
    stored_hash = user[2]
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."


def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"⚠️ File not found: {filepath}")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")
    return migrated_count


def load_csv_to_table(csv_path, table_name):
    """Load CSV data into database table."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return 0

    conn = connect_database()

    try:
        df = pd.read_csv(csv_path)
        rows_loaded = df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
        print(f"✅ Loaded {rows_loaded} rows into {table_name} table")
        return rows_loaded
    except Exception as e:
        print(f"❌ Error loading {csv_path}: {e}")
        return 0
    finally:
        conn.close()


def load_all_csv_data():
    """Load all CSV files into database."""
    csv_files = {
        'cyber_incidents': 'DATA/cyber_incidents.csv',
        'datasets_metadata': 'DATA/datasets_metadata.csv',
        'it_tickets': 'DATA/it_tickets.csv'
    }

    total_rows = 0
    for table_name, csv_path in csv_files.items():
        rows_loaded = load_csv_to_table(csv_path, table_name)
        total_rows += rows_loaded

    return total_rows