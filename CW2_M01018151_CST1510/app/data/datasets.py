import pandas as pd
from app.data.db import connect_database


def get_all_datasets():
    """Get all datasets metadata."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df


def get_datasets_by_category(category):
    """Get datasets by category."""
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata WHERE category = ?"
    df = pd.read_sql_query(query, conn, params=(category,))
    conn.close()
    return df


def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert new dataset metadata."""
    conn = connect_database()
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO datasets_metadata 
    (dataset_name, category, source, last_updated, record_count, file_size_mb)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_sql, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id