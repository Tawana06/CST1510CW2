# init_database.py
import sqlite3
import os
import bcrypt
import pandas as pd


def create_database():
    """Create the SQLite database with all required tables and import CSV data."""

    # Database path
    db_path = r"C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\multi_domain_platform\intelligence_platform.db"

    # OOP DATA folder path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, "OOP DATA")

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"Creating database at: {db_path}")
    print(f"Looking for CSV files in: {data_folder}")

    # Connect to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create security_incidents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        category TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT DEFAULT 'Open',
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create datasets_metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        size_bytes INTEGER DEFAULT 0,
        rows INTEGER NOT NULL,
        columns INTEGER NOT NULL,
        source TEXT DEFAULT 'Unknown',
        uploaded_by TEXT,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create it_tickets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        priority TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Open',
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolution_time_hours REAL
    )
    """)

    # Create test users with bcrypt hashing
    test_users = [
        ('alice', 'SecurePass123!', 'analyst'),
        ('bob', 'password123', 'user'),
        ('admin', 'AdminPass123!', 'admin')
    ]

    for username, password, role in test_users:
        # Hash password with bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed_password.decode('utf-8'), role)
        )

    # Import data from CSV files if they exist
    print("\nImporting data from CSV files...")

    # 1. Import security incidents CSV
    incidents_csv = os.path.join(data_folder, "cyber_incidents.csv")
    if os.path.exists(incidents_csv):
        try:
            incidents_df = pd.read_csv(incidents_csv)
            print(f"   Found {len(incidents_df)} incidents in CSV")

            # Reorder columns to match database schema
            incidents_df = incidents_df[['incident_id', 'timestamp', 'severity', 'category', 'status', 'description']]

            # Clear existing data and import
            cursor.execute("DELETE FROM cyber_incidents")
            incidents_df.to_sql('cyber_incidents', conn, if_exists='append', index=False)
            print(f"   Imported {len(incidents_df)} incidents to database")
        except Exception as e:
            print(f"   Error importing incidents: {e}")
    else:
        print(f"   cybersecurity_incidents.csv not found, using test data")
        # Add test incidents if CSV doesn't exist
        test_incidents = [
            ('Malware', 'High', 'Open', 'Malware detected on server'),
            ('Phishing', 'Medium', 'Resolved', 'Phishing email campaign'),
            ('DDoS', 'Critical', 'Open', 'DDoS attack on web server'),
            ('Data Breach', 'High', 'Open', 'Suspected data breach'),
            ('Unauthorized Access', 'Low', 'Closed', 'Failed login attempts')
        ]

        for category, severity, status, description in test_incidents:
            cursor.execute(
                "INSERT OR IGNORE INTO cyber_incidents (category, severity, status, description) VALUES (?, ?, ?, ?)",
                (category, severity, status, description)
            )

    # 2. Import datasets CSV
    datasets_csv = os.path.join(data_folder, "datasets_metadata.csv")
    if os.path.exists(datasets_csv):
        try:
            datasets_df = pd.read_csv(datasets_csv)
            print(f"   Found {len(datasets_df)} datasets in CSV")

            # Add missing columns with default values
            datasets_df['size_bytes'] = datasets_df['rows'] * datasets_df['columns'] * 100
            datasets_df['source'] = 'CSV Import'

            # Reorder columns to match database schema
            datasets_df = datasets_df[
                ['dataset_id', 'name', 'size_bytes', 'rows', 'columns', 'source', 'uploaded_by', 'upload_date']]

            # Clear existing data and import
            cursor.execute("DELETE FROM datasets_metadata")
            datasets_df.to_sql('datasets_metadata', conn, if_exists='append', index=False)
            print(f"   Imported {len(datasets_df)} datasets to database")
        except Exception as e:
            print(f"   Error importing datasets: {e}")
    else:
        print(f"   datasets.csv not found, using test data")
        # Add test datasets if CSV doesn't exist
        test_datasets = [
            ('Sales Data', 104857600, 100000, 50, 'CRM System', 'alice'),
            ('Customer Analytics', 52428800, 50000, 30, 'Analytics Platform', 'bob'),
            ('Server Logs', 209715200, 200000, 20, 'Production Servers', 'charlie'),
            ('Financial Records', 157286400, 75000, 40, 'Accounting System', 'alice')
        ]

        for name, size_bytes, rows, columns, source, uploaded_by in test_datasets:
            cursor.execute(
                "INSERT OR IGNORE INTO datasets_metadata (name, size_bytes, rows, columns, source, uploaded_by) VALUES (?, ?, ?, ?, ?, ?)",
                (name, size_bytes, rows, columns, source, uploaded_by)
            )

    # 3. Import tickets CSV
    tickets_csv = os.path.join(data_folder, "it_tickets.csv")
    if os.path.exists(tickets_csv):
        try:
            tickets_df = pd.read_csv(tickets_csv)
            print(f"   Found {len(tickets_df)} tickets in CSV")

            # Clear existing data and import
            cursor.execute("DELETE FROM it_tickets")
            tickets_df.to_sql('it_tickets', conn, if_exists='append', index=False)
            print(f"   Imported {len(tickets_df)} tickets to database")
        except Exception as e:
            print(f"   Error importing tickets: {e}")
    else:
        print(f"   it_tickets.csv not found, using test data")
        # Add test tickets if CSV doesn't exist
        test_tickets = [
            ('High', 'Server outage affecting all users', 'Open', 'John', 0),
            ('Medium', 'Email configuration issue', 'In Progress', 'Sarah', 2.5),
            ('Low', 'Monitor replacement request', 'Resolved', 'Mike', 8.0),
            ('Critical', 'Database connection failure', 'Open', 'John', 0),
            ('Medium', 'Software license renewal', 'Waiting for User', 'Sarah', 0)
        ]

        for priority, description, status, assigned_to, resolution_time in test_tickets:
            cursor.execute(
                "INSERT OR IGNORE INTO it_tickets (priority, description, status, assigned_to, resolution_time_hours) VALUES (?, ?, ?, ?, ?)",
                (priority, description, status, assigned_to, resolution_time)
            )

    # Commit changes
    conn.commit()

    # Verify tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print("\nDatabase created successfully!")
    print("Tables created:")
    for table in tables:
        print(f"   - {table[0]}")

    # Count records in each table
    tables_to_count = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    for table in tables_to_count:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table}: {count} records")

    conn.close()

    print(f"\nDatabase is ready at: {db_path}")
    print("You can now run your Streamlit application!")


if __name__ == "__main__":
    create_database()