import streamlit as st
import pandas as pd
import numpy as np
from app.data.incidents import get_all_incidents, get_incidents_by_type_count

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
# Page config from tutorial
st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")
st.title("🔒 Cybersecurity Dashboard")

# ---- SIDEBAR (from tutorial layout section) ----
with st.sidebar:
    st.header("Filters")
    severity_filter = st.multiselect(
        "Select Severity",
        ["Low", "Medium", "High", "Critical"],
        default=["High", "Critical"]
    )
    show_raw_data = st.checkbox("Show raw data")

    st.divider()
    st.header("Quick Actions")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    if st.button("📊 Generate Report"):
        st.info("Report generation coming soon!")

# ---- MAIN CONTENT ----
st.header("Incident Overview")

# Get data
incidents = get_all_incidents()
type_counts = get_incidents_by_type_count()

# Metrics (like tutorial's mini dashboard)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", len(incidents))
col2.metric("High Severity", len(incidents[incidents['severity'] == 'High']))
col3.metric("Open Incidents", len(incidents[incidents['status'] == 'Open']))
col4.metric("Categories", len(type_counts))

st.divider()

# ---- CHARTS (from tutorial charts section) ----
st.header("Visualizations")

# Use columns for layout (from tutorial layout section)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Category")
    # Bar chart from tutorial
    st.bar_chart(type_counts.set_index('category'))

with col2:
    st.subheader("Severity Distribution")
    # Create data for pie chart
    severity_data = incidents['severity'].value_counts()
    st.bar_chart(severity_data)

# ---- DATA TABLE (from tutorial data section) ----
if show_raw_data:
    st.header("Raw Incident Data")
    st.dataframe(incidents)

# ---- WIDGETS FOR INTERACTION (from tutorial widgets section) ----
st.divider()
st.header("Incident Analysis")

# Selectbox from tutorial
selected_category = st.selectbox(
    "Analyze Category",
    incidents['category'].unique() if len(incidents) > 0 else []
)

if selected_category:
    category_data = incidents[incidents['category'] == selected_category]
    st.write(f"**{len(category_data)}** incidents in {selected_category}")

    # Show line chart of incidents over time
    if 'timestamp' in category_data.columns:
        category_data['date'] = pd.to_datetime(category_data['timestamp']).dt.date
        daily_counts = category_data.groupby('date').size()
        st.line_chart(daily_counts)