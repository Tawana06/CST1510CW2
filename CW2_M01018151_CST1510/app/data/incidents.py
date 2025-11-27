import pandas as pd
from app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def update_incident_status(incident_id, new_status):
    """Update incident status."""
    conn = connect_database()
    cursor = conn.cursor()

    update_sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    cursor.execute(update_sql, (new_status, incident_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected


def delete_incident(incident_id):
    """Delete an incident."""
    conn = connect_database()
    cursor = conn.cursor()

    delete_sql = "DELETE FROM cyber_incidents WHERE id = ?"
    cursor.execute(delete_sql, (incident_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected

# Analytical queries for incidents
def get_incidents_by_type_count():
    """Count incidents by type."""
    conn = connect_database()
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_high_severity_by_status():
    """Count high severity incidents by status."""
    conn = connect_database()
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df