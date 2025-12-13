# services/auth_manager.py
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager
import bcrypt
import re


class BcryptHasher:
    """Secure password hashing using bcrypt."""

    @staticmethod
    def hash_password(plain: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        """Check if a plain password matches the bcrypt hash."""
        try:
            return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
        except (ValueError, TypeError):
            return False


class AuthManager:
    """Handles user authentication and registration using DatabaseManager."""

    def __init__(self, db: DatabaseManager):
        self._db = db

    def validate_username(self, username: str):
        """Validate username format."""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long."
        if " " in username:
            return False, "Username cannot contain spaces."
        if not re.match(r"^[A-Za-z0-9_]+$", username):
            return False, "Username can only contain letters, numbers, and underscores."

        # Check if username exists in database
        if self.user_exists(username):
            return False, f"Username '{username}' already exists."

        return True, ""

    def validate_password(self, password: str):
        """Validate password strength."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number."
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\",.<>/?]", password):
            return False, "Password must contain at least one special character."
        return True, ""

    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the database."""
        row = self._db.fetch_one(
            "SELECT username FROM users WHERE username = ?",
            (username,)
        )
        return row is not None

    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """Register a new user in the database."""
        # Check if username already exists
        if self.user_exists(username):
            return False

        # Hash password with bcrypt and insert user
        password_hash = BcryptHasher.hash_password(password)

        try:
            cursor = self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Registration error: {e}")
            return False

    def login_user(self, username: str, password: str) -> Optional[User]:
        """Login a user and return User object if successful."""
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if row is None:
            return None

        username_db, password_hash_db, role_db = row

        if BcryptHasher.check_password(password, password_hash_db):
            return User(username_db, password_hash_db, role_db)
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username without password verification."""
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if row is None:
            return None

        username_db, password_hash_db, role_db = row
        return User(username_db, password_hash_db, role_db)

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password."""
        # First verify old password
        user = self.login_user(username, old_password)
        if not user:
            return False

        # Hash new password with bcrypt and update
        new_password_hash = BcryptHasher.hash_password(new_password)

        try:
            cursor = self._db.execute_query(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_password_hash, username)
            )
            return cursor.rowcount > 0
        except Exception:
            return False

    def get_all_users(self):
        """Get all users (admin only)."""
        rows = self._db.fetch_all(
            "SELECT username, role FROM users ORDER BY username"
        )
        return rows