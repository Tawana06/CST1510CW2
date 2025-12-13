import streamlit as st
import pandas as pd
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

# Page configuration
st.set_page_config(
    page_title="Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

#Checking login
# Ensure state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

# if not logged in, send user back
if not st.session_state.logged_in:
    st.error(" You must be logged in to view the dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Go to Login Page"):
            st.switch_page("home.py")
    with col2:
        if st.button("📝 Register New Account"):
            st.switch_page("home.py")

    st.stop()

# Load data using OOP
try:
    incidents_df = SecurityIncident.get_all_incidents()
    datasets_df = Dataset.get_all_datasets()
    tickets_df = ITTicket.get_all_tickets()
except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
    incidents_df = pd.DataFrame()
    datasets_df = pd.DataFrame()
    tickets_df = pd.DataFrame()

#dashboard content
st.title(f"📊 Welcome, {st.session_state.username}!")
st.success(
    f"Role: **{st.session_state.user_role}** | Access level: {'Full system' if st.session_state.user_role == 'admin' else 'Multi-domain' if st.session_state.user_role == 'analyst' else 'Basic'}")

# Quick navigation buttons
st.markdown("### Quick Navigation")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(" Cybersecurity Dashboard", use_container_width=True):
        st.switch_page("pages/cybersecurity.py")
with col2:
    if st.button("🔬 Data Science Dashboard", use_container_width=True):
        st.switch_page("pages/data_Science.py")
with col3:
    if st.button("🖥️ IT Operations Dashboard", use_container_width=True):
        st.switch_page("pages/it_Operations.py")

st.divider()

#system overview
st.header("System Overview")

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(" Incidents", len(incidents_df))
    if len(incidents_df) > 0:
        open_incidents = len(incidents_df[incidents_df['status'] == 'Open'])
        st.caption(f"{open_incidents} open")

with col2:
    st.metric("🔬 Datasets", len(datasets_df))
    if len(datasets_df) > 0:
        total_rows = datasets_df['rows'].sum() if 'rows' in datasets_df.columns else 0
        st.caption(f"{total_rows:,} total rows")

with col3:
    st.metric("🖥️ Tickets", len(tickets_df))
    if len(tickets_df) > 0:
        open_tickets = len(tickets_df[tickets_df['status'] == 'Open'])
        st.caption(f"{open_tickets} open")

with col4:
    st.metric("👥 Your Role", st.session_state.user_role)
    st.caption("Access level")

st.divider()

# recent activity buttons added
st.header(" Recent Activity")

# Create tabs for recent data
tab1, tab2, tab3 = st.tabs([" Recent Incidents", " Recent Datasets", " Recent Tickets"])

with tab1:
    if len(incidents_df) > 0:
        recent_incidents = incidents_df.head(5)
        st.dataframe(recent_incidents[['incident_id', 'timestamp', 'severity', 'category', 'status']])
    else:
        st.info("No incident data available.")

with tab2:
    if len(datasets_df) > 0:
        recent_datasets = datasets_df.head(5)
        st.dataframe(recent_datasets[['dataset_id', 'name', 'rows', 'upload_date']])
    else:
        st.info("No dataset data available.")

with tab3:
    if len(tickets_df) > 0:
        recent_tickets = tickets_df.head(5)
        st.dataframe(recent_tickets[['ticket_id', 'priority', 'status', 'assigned_to', 'created_at']])
    else:
        st.info("No ticket data available.")

st.divider()

# quick actions
st.header("⚡ Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button(" Report Incident", use_container_width=True):
        st.info("Redirecting to incident creation...")
        # Would switch to incident creation page

with action_col2:
    if st.button(" Generate Report", use_container_width=True):
        st.info("Generating system report...")

with action_col3:
    if st.button(" View Alerts", use_container_width=True):
        st.info("Showing system alerts...")

# creating sidebar
with st.sidebar:
    st.header(" User Profile")
    st.write(f"**Username:** {st.session_state.username}")
    st.write(f"**Role:** {st.session_state.user_role}")
    st.write(
        f"**Access:** {'Full system' if st.session_state.user_role == 'admin' else 'Multi-domain' if st.session_state.user_role == 'analyst' else 'Basic'}")

    st.divider()

    st.header(" Quick Tools")
    if st.button(" Refresh Data"):
        st.rerun()

    if st.button(" Export Data"):
        st.info("Export functionality coming soon!")

    st.divider()

    # Logout button
    if st.button(" Logout", type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.user_data = {}
        st.info("You have been logged out.")
        st.switch_page("OOP_home.py")

# Footer
st.divider()
st.caption(
    f" Multi-Domain Intelligence Platform | User: {st.session_state.username} | Role: {st.session_state.user_role}")