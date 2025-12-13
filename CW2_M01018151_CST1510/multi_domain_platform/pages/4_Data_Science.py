import streamlit as st
import pandas as pd
from models.dataset import Dataset

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

# if not logged in, send user back to login
if not st.session_state.logged_in:
    st.error(" You must be logged in to access this dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Go to Login Page"):
            st.switch_page("OOP_home.py")  # Fixed
    with col2:
        if st.button("📝 Register New Account"):
            st.switch_page("OOP_home.py")  # Fixed

    st.stop()

# domain page
st.title("🔬 Data Science Dashboard")

# dataset sidebar
with st.sidebar:
    st.header("Dataset Filters")
    min_rows = st.slider("Minimum Rows", 0, 1000000, 0, 10000)
    show_large_only = st.checkbox("Show only large datasets (>100MB)")

# main content
st.header("Dataset Governance")

# Get data using OOP
try:
    # Get all datasets as DataFrame using Dataset class method
    datasets_df = Dataset.get_all_datasets()

    # Get summary using Dataset class method
    summary = Dataset.get_dataset_summary()

    # Create Dataset objects from the data
    datasets_list = []
    for _, row in datasets_df.iterrows():
        dataset = Dataset(
            dataset_id=row['dataset_id'],
            name=row['name'],
            rows=row['rows'],
            columns=row['columns'],
            source=row.get('source', 'Unknown'),
            uploaded_by=row.get('uploaded_by'),
            upload_date=row.get('upload_date')
        )
        datasets_list.append(dataset)

except Exception as e:
    st.error(f"Error loading data: {e}")
    datasets_df = pd.DataFrame()
    summary = (0, 0, 0.0)
    datasets_list = []

# Metrics
col1, col2, col3 = st.columns(3)
if summary:
    col1.metric("Total Datasets", summary[0])
    col2.metric("Total Rows", f"{summary[1]:,}")
    col3.metric("Avg Columns", f"{summary[2]:.1f}")

# Apply filters
filtered_datasets = datasets_df.copy()
if min_rows > 0:
    filtered_datasets = filtered_datasets[filtered_datasets['rows'] >= min_rows]
if show_large_only:
    # Calculate estimated size if size_bytes column doesn't exist
    if 'size_bytes' not in filtered_datasets.columns:
        # Estimate size: rows * columns * 100 bytes (rough estimate)
        filtered_datasets['estimated_size_bytes'] = filtered_datasets['rows'] * filtered_datasets['columns'] * 100
        filtered_datasets['size_mb'] = filtered_datasets['estimated_size_bytes'] / (1024 * 1024)
        filtered_datasets = filtered_datasets[filtered_datasets['size_mb'] > 100]
    else:
        # Use actual size_bytes if column exists
        filtered_datasets['size_mb'] = filtered_datasets['size_bytes'] / (1024 * 1024)
        filtered_datasets = filtered_datasets[filtered_datasets['size_mb'] > 100]

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
        # Create size column for visualization
        if 'size_bytes' in filtered_datasets.columns:
            # Use actual size_bytes if available
            filtered_datasets['size_mb'] = filtered_datasets['size_bytes'] / (1024 * 1024)
        else:
            # Estimate size for visualization
            filtered_datasets['size_mb'] = filtered_datasets['rows'] * filtered_datasets['columns'] * 100 / (
                        1024 * 1024)

        st.area_chart(filtered_datasets.set_index('name')['size_mb'])