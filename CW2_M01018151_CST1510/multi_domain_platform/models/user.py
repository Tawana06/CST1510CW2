
from typing import Optional
import os

from services.database_manager import DatabaseManager

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(current_dir), "intelligence_platform.db")

print(f"User class database path: {db_path}")  # For debugging


class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""

    # Database manager as a class variable
    _db_manager = DatabaseManager(db_path)

    def __init__(self, username: str, password_hash: str, role: str, user_id: int = None):
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role
        self.__id = user_id

    def get_username(self) -> str:
        return self.__username

    def get_role(self) -> str:
        return self.__role

    def verify_password(self, plain_password: str, hasher) -> bool:
        """Check if a plain-text password matches this user's hash."""
        return hasher.check_password(plain_password, self.__password_hash)

    @classmethod
    def get_user_by_username(cls, username: str) -> Optional['User']:
        """Retrieve user by username."""
        result = cls._db_manager.fetch_one(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if result:
            user_id, username_db, password_hash_db, role_db = result
            user = cls(username_db, password_hash_db, role_db)
            user.__id = user_id
            return user
        return None

    @classmethod
    def insert_user(cls, username: str, password_hash: str, role: str = 'user') -> int:
        """Insert new user."""
        cursor = cls._db_manager.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        return cursor.lastrowid

    def __str__(self) -> str:
        return f"User({self.__username}, role={self.__role})"