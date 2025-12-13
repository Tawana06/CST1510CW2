#update using code from the non OOP db file
import sqlite3
import os
from services.database_manager import DatabaseManager


def connect_database():
    """Fixed path connection - updated to use DatabaseManager."""
    # Use absolute Windows path
    db_path = r"C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\multi_domain_platform\intelligence_platform.db"

    print(f"Connecting to: {db_path}")

    # Create directory if needed
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Create DatabaseManager instance
    db_manager = DatabaseManager(db_path)
    db_manager.connect()

    print(" Connected via DatabaseManager!")
    return db_manager._connection