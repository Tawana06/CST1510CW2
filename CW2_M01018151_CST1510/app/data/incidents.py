import pandas as pd
from app.data.db import connect_database

def insert_incident(incident_id, timestamp, category, severity, status, description):
    """Insert new incident - FIXED PARAMETER ORDER."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (incident_id, timestamp, category, severity, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (incident_id, timestamp, category, severity, status, description))
    conn.commit()
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn
    )
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    """Update incident status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def delete_incident(incident_id):
    """Delete an incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE incident_id = ?",
        (incident_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def get_incidents_by_type_count():
    """Count incidents by type ."""
    conn = connect_database()
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_high_severity_by_status():
    """Count high severity incidents by status """
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