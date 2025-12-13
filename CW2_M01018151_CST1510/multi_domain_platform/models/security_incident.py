import pandas as pd
import os
from services.database_manager import DatabaseManager
from typing import Optional

# Get database path
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(current_dir), "intelligence_platform.db")


class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    # Database manager as a class variable
    _db_manager = DatabaseManager(db_path)

    def __init__(self, incident_id: int, incident_type: str, severity: str, status: str, description: str,
                 timestamp: str = None):
        self.__id = incident_id
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__timestamp = timestamp

    def get_id(self) -> int:
        return self.__id

    def get_incident_type(self) -> str:
        return self.__incident_type

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description

    def get_timestamp(self) -> Optional[str]:
        return self.__timestamp

    def update_status(self, new_status: str) -> None:
        self.__status = new_status

    def get_severity_level(self) -> int:
        """Return an integer severity level (simple example)."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)

    def __str__(self) -> str:
        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__incident_type} - {self.__status}"

    # Database operations as class methods using DatabaseManager
    @classmethod
    def insert_incident(cls, incident_id: int, timestamp: str, category: str, severity: str, status: str,
                        description: str) -> int:
        """Insert new incident."""
        cursor = cls._db_manager.execute_query("""
            INSERT INTO cyber_incidents
            (incident_id, timestamp, category, severity, status, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (incident_id, timestamp, category, severity, status, description))
        return incident_id

    @classmethod
    def get_all_incidents(cls) -> pd.DataFrame:
        """Get all incidents as DataFrame."""
        return cls._db_manager.fetch_dataframe(
            "SELECT * FROM cyber_incidents ORDER BY incident_id DESC"
        )

    @classmethod
    def get_incident_by_id(cls, incident_id: int) -> Optional['SecurityIncident']:
        """Get a single incident by ID."""
        incident_data = cls._db_manager.fetch_one(
            "SELECT * FROM cyber_incidents WHERE incident_id = ?",
            (incident_id,)
        )

        if incident_data:

            # CSV columns: incident_id,timestamp,severity,category,status,description
            # Database columns after import: incident_id,timestamp,category,severity,status,description
            return cls(
                incident_id=incident_data[0],        # incident_id
                incident_type=incident_data[3],      # severity (from CSV category)
                severity=incident_data[2],           # category (from CSV severity)
                status=incident_data[4],             # status
                description=incident_data[5],        # description
                timestamp=incident_data[1]           # timestamp
            )
        return None

    @classmethod
    def update_incident_status(cls, incident_id: int, new_status: str) -> int:
        """Update incident status."""
        cursor = cls._db_manager.execute_query(
            "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
            (new_status, incident_id)
        )
        return cursor.rowcount

    @classmethod
    def delete_incident(cls, incident_id: int) -> int:
        """Delete an incident."""
        cursor = cls._db_manager.execute_query(
            "DELETE FROM cyber_incidents WHERE incident_id = ?",
            (incident_id,)
        )
        return cursor.rowcount

    @classmethod
    def get_incidents_by_type_count(cls) -> pd.DataFrame:
        """Count incidents by type."""
        query = """
        SELECT category, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY category
        ORDER BY count DESC
        """
        return cls._db_manager.fetch_dataframe(query)

    @classmethod
    def get_high_severity_by_status(cls) -> pd.DataFrame:
        """Count high severity incidents by status."""
        query = """
        SELECT status, COUNT(*) as count
        FROM cyber_incidents
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
        """
        return cls._db_manager.fetch_dataframe(query)