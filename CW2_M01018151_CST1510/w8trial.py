import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

# Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")

from pathlib import Path

Path("app/__init__.py").touch()
Path("app/data/__init__.py").touch()
Path("app/services/__init__.py").touch()