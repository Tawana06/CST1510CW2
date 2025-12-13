import pandas as pd
import os
from services.database_manager import DatabaseManager
from typing import Optional

# Get database path
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(current_dir), "intelligence_platform.db")


class ITTicket:
    """Represents an IT support ticket."""

    # Database manager as a class variable
    _db_manager = DatabaseManager(db_path)

    def __init__(self, ticket_id: int, title: str, priority: str, status: str, assigned_to: str,
                 description: str = None, created_at: str = None, resolution_time_hours: float = None):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__assigned_to = assigned_to
        self.__description = description
        self.__created_at = created_at
        self.__resolution_time_hours = resolution_time_hours

    def assign_to(self, staff: str) -> None:
        self.__assigned_to = staff

    def close_ticket(self) -> None:
        self.__status = "Closed"

    def get_status(self) -> str:
        return self.__status

    def get_id(self) -> int:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def get_priority(self) -> str:
        return self.__priority

    def get_assigned_to(self) -> str:
        return self.__assigned_to

    def get_description(self) -> Optional[str]:
        return self.__description

    def get_created_at(self) -> Optional[str]:
        return self.__created_at

    def get_resolution_time_hours(self) -> Optional[float]:
        return self.__resolution_time_hours

    def __str__(self) -> str:
        return (
            f"Ticket {self.__id}: {self.__title} "
            f"[{self.__priority}] – {self.__status} (assigned to: {self.__assigned_to})"
        )

    # Database operations as class methods using DatabaseManager
    @classmethod
    def get_all_tickets(cls) -> pd.DataFrame:
        """Get all IT tickets."""
        return cls._db_manager.fetch_dataframe("SELECT * FROM it_tickets")

    @classmethod
    def get_tickets_by_status(cls, status: str) -> pd.DataFrame:
        """Get tickets by status."""
        return cls._db_manager.fetch_dataframe(
            "SELECT * FROM it_tickets WHERE status = ?",
            (status,)
        )

    @classmethod
    def get_ticket_by_id(cls, ticket_id: int) -> Optional['ITTicket']:
        """Get a single ticket by ID."""
        ticket_data = cls._db_manager.fetch_one(
            "SELECT * FROM it_tickets WHERE ticket_id = ?",
            (ticket_id,)
        )

        if ticket_data:
            #using columns: ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
            title = ticket_data[2] if len(ticket_data) > 2 else "No Title"
            return cls(
                ticket_id=ticket_data[0],
                title=title,
                priority=ticket_data[1],
                status=ticket_data[3],
                assigned_to=ticket_data[4],
                description=ticket_data[2] if len(ticket_data) > 2 else None,
                created_at=ticket_data[5] if len(ticket_data) > 5 else None,
                resolution_time_hours=ticket_data[6] if len(ticket_data) > 6 else None
            )
        return None

    @classmethod
    def insert_ticket(cls, ticket_id: int, priority: str, description: str, status: str,
                      assigned_to: str, created_at: str, resolution_time_hours: float) -> int:
        """Insert new IT ticket."""
        cursor = cls._db_manager.execute_query("""
            INSERT INTO it_tickets
            (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))
        return ticket_id

    @classmethod
    def update_ticket_status(cls, ticket_id: int, new_status: str) -> int:
        """Update ticket status."""
        cursor = cls._db_manager.execute_query(
            "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
            (new_status, ticket_id)
        )
        return cursor.rowcount

    @classmethod
    def delete_ticket(cls, ticket_id: int) -> int:
        """Delete a ticket."""
        cursor = cls._db_manager.execute_query(
            "DELETE FROM it_tickets WHERE ticket_id = ?",
            (ticket_id,)
        )
        return cursor.rowcount

    @classmethod
    def get_ticket_summary(cls) -> tuple:
        """Get basic ticket summary."""
        result = cls._db_manager.fetch_one("""
        SELECT 
            COUNT(*) as total_tickets,
            AVG(resolution_time_hours) as avg_resolution_time,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open_tickets
        FROM it_tickets
        """)
        return result

    @classmethod
    def get_staff_performance(cls) -> pd.DataFrame:
        """Simple staff performance analysis."""
        return cls._db_manager.fetch_dataframe("""
        SELECT 
            assigned_to,
            COUNT(*) as ticket_count,
            AVG(resolution_time_hours) as avg_resolution_time
        FROM it_tickets 
        WHERE assigned_to IS NOT NULL
        GROUP BY assigned_to
        ORDER BY avg_resolution_time DESC
        """)