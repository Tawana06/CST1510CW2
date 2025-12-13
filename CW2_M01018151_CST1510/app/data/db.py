import sqlite3
import os


def connect_database():
    """ fixed path connection"""
    # Use absolute Windows path
    db_path = r"C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\DATA\intelligence_platform.db"

    print(f"🔗 Connecting to: {db_path}")

    # Create directory if needed
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect
    conn = sqlite3.connect(db_path)
    print("✅ Connected!")
    return conn