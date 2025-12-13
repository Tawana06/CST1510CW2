import streamlit as st
import pandas as pd
from app.data.datasets import get_all_datasets, get_dataset_summary



# login check
# Page configuration
st.set_page_config(
    page_title="Data Science Dashboard",
    page_icon="🔬",
    layout="wide"
)

# Check login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#if not logged in, send user back to login
if not st.session_state.logged_in:
    st.error(" You must be logged in to access this dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Go to Login Page"):
            st.switch_page("home.py")
    with col2:
        if st.button("📝 Register New Account"):
            st.switch_page("home.py")

    st.stop()


# domain page
#
st.set_page_config(page_title="Data Science Dashboard", layout="wide")
st.title("🔬 Data Science Dashboard")

# dataset sidebar
with st.sidebar:
    st.header("Dataset Filters")
    min_rows = st.slider("Minimum Rows", 0, 1000000, 0, 10000)
    show_large_only = st.checkbox("Show only large datasets (>100MB)")

#main content
st.header("Dataset Governance")

# Get data
datasets = get_all_datasets()
summary = get_dataset_summary()

# Metrics
col1, col2, col3 = st.columns(3)
if summary:
    col1.metric("Total Datasets", summary[0])
    col2.metric("Total Rows", f"{summary[1]:,}")
    col3.metric("Avg Columns", f"{summary[2]:.1f}")

# Apply filters
filtered_datasets = datasets.copy()
if min_rows > 0:
    filtered_datasets = filtered_datasets[filtered_datasets['rows'] >= min_rows]
if show_large_only:

    if 'file_size_mb' in filtered_datasets.columns:
        filtered_datasets = filtered_datasets[filtered_datasets['file_size_mb'] > 100]

# Display
st.subheader("Dataset Catalog")
st.dataframe(filtered_datasets)

# Visualizations
if len(filtered_datasets) > 0:
    st.subheader("Size Distribution")

    # Create columns for layout
    col1, col2 = st.columns(2)

    with col1:
        if 'rows' in filtered_datasets.columns:
            st.bar_chart(filtered_datasets.set_index('name')['rows'])

    with col2:
        if 'file_size_mb' in filtered_datasets.columns:
            st.area_chart(filtered_datasets.set_index('name')['file_size_mb'])