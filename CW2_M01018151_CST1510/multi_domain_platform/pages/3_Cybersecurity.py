import streamlit as st
import pandas as pd
from models.security_incident import SecurityIncident

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    page_icon="🔒",
    layout="wide"
)

# Check login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Go to Login Page"):
            st.switch_page("OOP_home.py")  # Changed to OOP_home.py
    with col2:
        if st.button(" Register New Account"):
            st.switch_page("OOP_home.py")  # Changed to OOP_home.py

    st.stop()

st.title("🔒 Cybersecurity Dashboard")

# sidebar
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
    if st.button("Refresh Data"):
        st.rerun()
    if st.button("Generate Report"):
        st.info("Report generation coming soon!")

# content
st.header("Incident Overview")

# Get data using OOP
try:
    # Get all incidents as DataFrame using SecurityIncident class method
    incidents_df = SecurityIncident.get_all_incidents()

    # Get type counts using SecurityIncident class method
    type_counts_df = SecurityIncident.get_incidents_by_type_count()

    # Create SecurityIncident objects from the data
    incidents_list = []
    for _, row in incidents_df.iterrows():
        incident = SecurityIncident(
            incident_id=row['incident_id'],
            incident_type=row['category'],
            severity=row['severity'],
            status=row['status'],
            description=row['description']
        )
        incidents_list.append(incident)

except Exception as e:
    st.error(f"Error loading data: {e}")
    incidents_df = pd.DataFrame()
    type_counts_df = pd.DataFrame()
    incidents_list = []

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", len(incidents_df))
col2.metric("High Severity", len(incidents_df[incidents_df['severity'] == 'High']))
col3.metric("Open Incidents", len(incidents_df[incidents_df['status'] == 'Open']))
col4.metric("Categories", len(type_counts_df))

st.divider()

# charts
st.header("Visualizations")

# Use columns for layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Category")
    # Bar chart from tutorial
    if not type_counts_df.empty:
        st.bar_chart(type_counts_df.set_index('category'))

with col2:
    st.subheader("Severity Distribution")
    # Create data for pie chart
    if not incidents_df.empty:
        severity_data = incidents_df['severity'].value_counts()
        st.bar_chart(severity_data)

# showing row datafiles from the csv
if show_raw_data:
    st.header("Raw Incident Data")
    st.dataframe(incidents_df)

# widgets
st.divider()
st.header("Incident Analysis")

# Selectbox
selected_category = st.selectbox(
    "Analyze Category",
    incidents_df['category'].unique() if len(incidents_df) > 0 else []
)

if selected_category:
    category_data = incidents_df[incidents_df['category'] == selected_category]
    st.write(f"**{len(category_data)}** incidents in {selected_category}")

    # Show line chart of incidents over time
    if 'timestamp' in category_data.columns:
        category_data['datetime'] = pd.to_datetime(category_data['timestamp'], format='mixed')
        weekly_counts = category_data.set_index('datetime').resample("W").size().fillna(0)
        st.subheader("Weekly Incident Trend")
        st.line_chart(weekly_counts)