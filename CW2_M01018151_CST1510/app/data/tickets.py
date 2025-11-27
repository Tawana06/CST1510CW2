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


def update_ticket_status(ticket_id, new_status):
    """Update ticket status."""
    conn = connect_database()
    cursor = conn.cursor()

    update_sql = "UPDATE it_tickets SET status = ? WHERE ticket_id = ?"
    cursor.execute(update_sql, (new_status, ticket_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected