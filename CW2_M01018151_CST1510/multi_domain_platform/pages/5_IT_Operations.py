import streamlit as st
import pandas as pd
from models.it_ticket import ITTicket


# Page configuration first
st.set_page_config(
    page_title="IT Operations Dashboard",
    page_icon="🖥️",
    layout="wide"
)

# Check login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#  if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Go to Login Page"):
            st.switch_page("OOP_home.py")
    with col2:
        if st.button("📝 Register New Account"):
            st.switch_page("OOP_home.py")

    st.stop()

# domain
st.title("🖥️ IT Operations Dashboard")

# side bar
with st.sidebar:
    st.header("Ticket Filters")
    status_filter = st.multiselect(
        "Ticket Status",
        ["Open", "In Progress", "Resolved", "Closed", "Waiting for User"],
        default=["Open", "In Progress"]
    )
    priority_filter = st.selectbox(
        "Priority Level",
        ["All", "Low", "Medium", "High", "Critical"]
    )

# main
st.header("Service Desk Performance")

# Get data using OOP
try:
    # Get all tickets as DataFrame using ITTicket class method
    tickets_df = ITTicket.get_all_tickets()

    # Get summary using ITTicket class method
    summary = ITTicket.get_ticket_summary()

    # Get staff performance using ITTicket class method
    staff_perf_df = ITTicket.get_staff_performance()

    # Create ITTicket objects from the data
    tickets_list = []
    for _, row in tickets_df.iterrows():
        ticket = ITTicket(
            ticket_id=row['ticket_id'],
            title=row.get('description', 'No Title'),  # Using description as title
            priority=row['priority'],
            status=row['status'],
            assigned_to=row['assigned_to'],
            description=row.get('description'),
            created_at=row.get('created_at'),
            resolution_time_hours=row.get('resolution_time_hours')
        )
        tickets_list.append(ticket)

except Exception as e:
    st.error(f"Error loading data: {e}")
    tickets_df = pd.DataFrame()
    summary = (0, 0.0, 0)
    staff_perf_df = pd.DataFrame()
    tickets_list = []

# Metrics
if summary:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", summary[0])
    col2.metric("Avg Resolution", f"{summary[1]:.1f} hours")
    col3.metric("Open Tickets", summary[2])

# Apply filters
filtered_tickets = tickets_df.copy()
if status_filter:
    filtered_tickets = filtered_tickets[filtered_tickets['status'].isin(status_filter)]
if priority_filter != "All":
    filtered_tickets = filtered_tickets[filtered_tickets['priority'] == priority_filter]

# Display
st.subheader("Ticket Overview")
st.dataframe(filtered_tickets)

# Staff performance
st.subheader("Staff Performance")
if len(staff_perf_df) > 0:
    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(staff_perf_df.set_index('assigned_to')['avg_resolution_time'])

    with col2:
        st.write("Performance Details:")
        st.dataframe(staff_perf_df)