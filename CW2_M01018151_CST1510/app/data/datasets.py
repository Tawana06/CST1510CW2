import pandas as pd
from app.data.db import connect_database   #TF is kwarggs


def get_all_datasets():
    """Get all datasets metadata."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df


def get_datasets_by_uploaded_by(uploaded_by):
    """Get datasets by uploaded_by."""
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata WHERE uploaded_by = ?"
    df = pd.read_sql_query(query, conn, params=(uploaded_by,))
    conn.close()
    return df


def insert_dataset(dataset_id, name, rows, columns, uploaded_by, upload_date):
    """Insert new dataset metadata - SIMPLE VERSION."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_id, name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, rows, columns, uploaded_by, upload_date))
    conn.commit()
    conn.close()
    return dataset_id


def update_dataset(dataset_id, **kwargs):
    """Update dataset metadata - SIMPLE VERSION."""
    if not kwargs:
        return 0

    conn = connect_database()
    cursor = conn.cursor()

    # Build query dynamically
    set_clauses = []
    values = []
    for key, value in kwargs.items():
        if value is not None:
            set_clauses.append(f"{key} = ?")
            values.append(value)

    values.append(dataset_id)
    query = f"UPDATE datasets_metadata SET {', '.join(set_clauses)} WHERE dataset_id = ?"

    cursor.execute(query, values)
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected


def delete_dataset(dataset_id):
    """Delete a dataset."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE dataset_id = ?",
        (dataset_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected


# Simple analytical query
def get_dataset_summary():
    """Get basic dataset summary."""
    conn = connect_database()
    query = """
    SELECT 
        COUNT(*) as total_datasets,
        SUM(rows) as total_rows,
        AVG(columns) as avg_columns
    FROM datasets_metadata
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result