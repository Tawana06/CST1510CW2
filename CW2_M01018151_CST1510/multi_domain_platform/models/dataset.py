import pandas as pd
import os
from services.database_manager import DatabaseManager
from typing import Optional

# Get database path
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(current_dir), "intelligence_platform.db")


class Dataset:
    """Represents a data science dataset in the platform."""

    # Database manager as a class variable
    _db_manager = DatabaseManager(db_path)

    def __init__(self, dataset_id: int, name: str, rows: int, columns: int, source: str,
                 uploaded_by: str = None, upload_date: str = None):
        self.__id = dataset_id
        self.__name = name
        self.__rows = rows
        self.__columns = columns
        self.__source = source
        self.__uploaded_by = uploaded_by
        self.__upload_date = upload_date

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_rows(self) -> int:
        return self.__rows

    def get_columns(self) -> int:
        return self.__columns

    def calculate_size_mb(self) -> float:
        # Calculate fake size based on rows and columns
        estimated_size_bytes = self.__rows * self.__columns * 100  # Rough estimate
        return estimated_size_bytes / (1024 * 1024)

    def get_source(self) -> str:
        return self.__source

    def get_uploaded_by(self) -> Optional[str]:
        return self.__uploaded_by

    def get_upload_date(self) -> Optional[str]:
        return self.__upload_date

    def __str__(self) -> str:
        size_mb = self.calculate_size_mb()
        return f"Dataset {self.__id}: {self.__name} ({size_mb:.2f} MB, {self.__rows} rows, {self.__columns} cols)"

    # Database operations as class methods using DatabaseManager
    @classmethod
    def get_all_datasets(cls) -> pd.DataFrame:
        """Get all datasets metadata."""
        return cls._db_manager.fetch_dataframe("SELECT * FROM datasets_metadata")

    @classmethod
    def get_datasets_by_uploaded_by(cls, uploaded_by: str) -> pd.DataFrame:
        """Get datasets by uploaded_by."""
        return cls._db_manager.fetch_dataframe(
            "SELECT * FROM datasets_metadata WHERE uploaded_by = ?",
            (uploaded_by,)
        )

    @classmethod
    def get_dataset_by_id(cls, dataset_id: int) -> Optional['Dataset']:
        """Get a single dataset by ID."""
        dataset_data = cls._db_manager.fetch_one(
            "SELECT * FROM datasets_metadata WHERE dataset_id = ?",
            (dataset_id,)
        )

        if dataset_data:
            # using columns: dataset_id, name, rows, columns, uploaded_by, upload_date
            return cls(
                dataset_id=dataset_data[0],
                name=dataset_data[1],
                rows=dataset_data[2],
                columns=dataset_data[3],
                source='Unknown',  # Default since we removed this column
                uploaded_by=dataset_data[4] if len(dataset_data) > 4 else None,
                upload_date=dataset_data[5] if len(dataset_data) > 5 else None
            )
        return None

    @classmethod
    def insert_dataset(cls, dataset_id: int, name: str, rows: int, columns: int, uploaded_by: str,
                       upload_date: str) -> int:
        """Insert new dataset metadata."""
        cursor = cls._db_manager.execute_query("""
            INSERT INTO datasets_metadata
            (dataset_id, name, rows, columns, uploaded_by, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (dataset_id, name, rows, columns, uploaded_by, upload_date))
        return dataset_id

    @classmethod
    def update_dataset(cls, dataset_id: int, **kwargs) -> int:
        """Update dataset metadata."""
        if not kwargs:
            return 0

        # Build query dynamically
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                set_clauses.append(f"{key} = ?")
                values.append(value)

        values.append(dataset_id)
        query = f"UPDATE datasets_metadata SET {', '.join(set_clauses)} WHERE dataset_id = ?"

        cursor = cls._db_manager.execute_query(query, values)
        return cursor.rowcount

    @classmethod
    def delete_dataset(cls, dataset_id: int) -> int:
        """Delete a dataset."""
        cursor = cls._db_manager.execute_query(
            "DELETE FROM datasets_metadata WHERE dataset_id = ?",
            (dataset_id,)
        )
        return cursor.rowcount

    @classmethod
    def get_dataset_summary(cls) -> tuple:
        """Get basic dataset summary."""
        result = cls._db_manager.fetch_one("""
        SELECT 
            COUNT(*) as total_datasets,
            SUM(rows) as total_rows,
            AVG(columns) as avg_columns
        FROM datasets_metadata
        """)
        return result