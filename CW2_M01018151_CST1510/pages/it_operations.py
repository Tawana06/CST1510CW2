import streamlit as st
import pandas as pd
from app.data.tickets import get_all_tickets, get_ticket_summary, get_staff_performance

import streamlit as st

# ---------- LOGIN CHECK (add to top of each domain page) ----------
# Page configuration first
st.set_page_config(
    page_title="Cybersecurity Dashboard",  # Change per page
    page_icon="🔒",  # Change per page
    layout="wide"
)

# Check login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("⛔ You must be logged in to access this dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Go to Login Page"):
            st.switch_page("app.py")
    with col2:
        if st.button("📝 Register New Account"):
            st.switch_page("app.py")

    st.stop()

# Optional: Role-based access control
# if st.session_state.user_role == "user":
#     st.error("⛔ Access denied. Analyst or admin role required.")
#     st.stop()

# ---------- REST OF YOUR DOMAIN PAGE CODE HERE ----------
# (Your existing dashboard code from earlier)
st.set_page_config(page_title="IT Operations Dashboard", layout="wide")
st.title("🖥️ IT Operations Dashboard")

# ---- SIDEBAR ----
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

# ---- MAIN CONTENT ----
st.header("Service Desk Performance")

# Get data
tickets = get_all_tickets()
summary = get_ticket_summary()
staff_perf = get_staff_performance()

# Metrics
if summary:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", summary[0])
    col2.metric("Avg Resolution", f"{summary[1]:.1f} hours")
    col3.metric("Open Tickets", summary[2])

# Apply filters
filtered_tickets = tickets.copy()
if status_filter:
    filtered_tickets = filtered_tickets[filtered_tickets['status'].isin(status_filter)]
if priority_filter != "All":
    filtered_tickets = filtered_tickets[filtered_tickets['priority'] == priority_filter]

# Display
st.subheader("Ticket Overview")
st.dataframe(filtered_tickets)

# Staff performance
st.subheader("Staff Performance")
if len(staff_perf) > 0:
    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(staff_perf.set_index('assigned_to')['avg_resolution_time'])

    with col2:
        st.write("Performance Details:")
        st.dataframe(staff_perf)