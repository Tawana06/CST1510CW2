from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file, load_all_csv_data
from app.data.incidents import insert_incident, get_all_incidents, get_incidents_by_type_count
from app.data.datasets import get_all_datasets, get_dataset_summary
from app.data.tickets import get_all_tickets, get_ticket_summary
from app.data.users import get_all_users


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
    print("\n🔐 Testing authentication...")
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(f"  {msg}")

    success, msg = login_user("alice", "SecurePass123!")
    print(f"  {msg}")

    # 4. Load CSV data
    print("\n📂 Loading CSV data...")
    total_rows = load_all_csv_data()
    print(f"  Loaded {total_rows} total rows")

    # 5. Test CRUD - Note: Use high incident_id to avoid conflicts
    print("\n🔧 Testing CRUD operations...")
    incident_id = insert_incident(
        9999,  # High number to avoid conflict
        "2024-11-05 10:30:00",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected"
    )
    print(f"  Created incident #{incident_id}")

    # 6. Query data
    print("\n📊 Querying data...")

    incidents = get_all_incidents()
    print(f"  Total incidents: {len(incidents)}")

    type_counts = get_incidents_by_type_count()
    print(f"  Incident types: {len(type_counts)}")

    datasets = get_all_datasets()
    print(f"  Total datasets: {len(datasets)}")

    tickets = get_all_tickets()
    print(f"  Total tickets: {len(tickets)}")

    users = get_all_users()
    print(f"  Total users: {len(users)}")

    # 7. Simple analysis
    print("\n📈 Simple analysis...")
    dataset_summary = get_dataset_summary()
    if dataset_summary:
        print(f"  Dataset summary: {dataset_summary[0]} datasets, {dataset_summary[1]:,} total rows")

    ticket_summary = get_ticket_summary()
    if ticket_summary:
        print(f"  Ticket summary: {ticket_summary[0]} tickets, {ticket_summary[2]} open")

    print("\n" + "=" * 60)
    print("🎉 Demo completed successfully!")
    print("=" * 60)

    print("\n📁 Database Summary:")
    print(f"  • Users: {len(users)}")
    print(f"  • Incidents: {len(incidents)}")
    print(f"  • Datasets: {len(datasets)}")
    print(f"  • Tickets: {len(tickets)}")


if __name__ == "__main__":
    main()