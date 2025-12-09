import pandas as pd
from app.data.db import connect_database

def get_all_tickets():
    """Get all IT tickets."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df

def get_tickets_by_status(status):
    """Get tickets by status."""
    conn = connect_database()
    query = "SELECT * FROM it_tickets WHERE status = ?"
    df = pd.read_sql_query(query, conn, params=(status,))
    conn.close()
    return df

def insert_ticket(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """Insert new IT ticket - SIMPLE VERSION."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit()
    conn.close()
    return ticket_id

def update_ticket_status(ticket_id, new_status):
    """Update ticket status."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def delete_ticket(ticket_id):
    """Delete a ticket."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

# Simple analytical queries
def get_ticket_summary():
    """Get basic ticket summary."""
    conn = connect_database()
    query = """
    SELECT 
        COUNT(*) as total_tickets,
        AVG(resolution_time_hours) as avg_resolution_time,
        SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open_tickets
    FROM it_tickets
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def get_staff_performance():
    """Simple staff performance analysis."""
    conn = connect_database()
    query = """
    SELECT 
        assigned_to,
        COUNT(*) as ticket_count,
        AVG(resolution_time_hours) as avg_resolution_time
    FROM it_tickets 
    WHERE assigned_to IS NOT NULL
    GROUP BY assigned_to
    ORDER BY avg_resolution_time DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df