from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents


def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    migrate_users_from_file()

    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    total_rows = load_all_csv_data()

    # 4. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

    type_counts = get_incidents_by_type_count()
    print(f"   Incident types: {len(type_counts)}")

    users = get_all_users()
    print(f"   Total users: {len(users)}")

    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("=" * 60)
    print("\n📊 Database Summary:")
    print(f"   - Users: {len(users)}")
    print(f"   - Incidents: {len(incidents_df)}")
    print(f"   - Incident types: {len(type_counts)}")


if __name__ == "__main__":
    main()