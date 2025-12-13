
import sqlite3
import os
from typing import Any, Iterable, Optional, List, Tuple


class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection = None  # Single connection instance
        self._initialize_database()  # Create tables on initialization

    def _initialize_database(self):
        """Create necessary tables if they don't exist."""
        # Use a fresh connection for initialization to avoid any issues
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()

            # First check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table_exists = cursor.fetchone() is not None

            if not table_exists:
                print(f"⚠ Creating database tables for the first time...")
                print(f"   Database location: {os.path.abspath(self._db_path)}")

                # Create users table
                cursor.execute('''
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL,
                        email TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                print("   ✓ Created 'users' table")

                # Create other tables as needed for your application
                cursor.execute('''
                    CREATE TABLE sessions (
                        session_id TEXT PRIMARY KEY,
                        username TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        FOREIGN KEY (username) REFERENCES users(username)
                    )
                ''')
                print("   ✓ Created 'sessions' table")

                # Add more tables based on your needs
                cursor.execute('''
                    CREATE TABLE articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT,
                        author TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (author) REFERENCES users(username)
                    )
                ''')
                print("   ✓ Created 'articles' table")

                conn.commit()
                print(f"Database initialization complete!")
            else:
                print(f"Database tables already exist in: {self._db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create a database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path, check_same_thread=False)
            # Enable foreign keys
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    def connect(self) -> None:
        """Ensure connection exists (called automatically)."""
        self._get_connection()

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute_query(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        """Execute a write query (INSERT, UPDATE, DELETE)."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        conn.commit()
        return cur

    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[Tuple]:
        """Fetch a single row from the database."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> List[Tuple]:
        """Fetch all rows from the database."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()

    def fetch_dataframe(self, sql: str, params: Iterable[Any] = ()):
        """Fetch data as pandas DataFrame."""
        import pandas as pd
        conn = self._get_connection()
        return pd.read_sql_query(sql, conn, params=tuple(params))

    # HELPER METHODS

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(sql, (table_name,))
        return result is not None

    def get_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        results = self.fetch_all(sql)
        return [row[0] for row in results]

    def add_default_user(self, username: str, password_hash: str, role: str = "user", email: str = None) -> bool:
        """Add a default user to the database (for initialization)."""
        try:
            self.execute_query(
                "INSERT OR IGNORE INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, email)
            )
            print(f"✓ Added default user: {username}")
            return True
        except Exception as e:
            print(f"✗ Failed to add user {username}: {e}")
            return False