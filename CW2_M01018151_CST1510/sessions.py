"""
Session management utilities
"""

import streamlit as st

def init_session():
    """Initialize session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "user_role" not in st.session_state:
        st.session_state.user_role = ""
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

def login(username, user_data):
    """Login user and set session state."""
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_role = user_data.get('role', 'user')
    st.session_state.user_data = user_data

def logout():
    """Logout user and clear session state."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_role = ""
    st.session_state.user_data = {}

def require_login():
    """Check if user is logged in, redirect if not."""
    if not st.session_state.logged_in:
        st.error("You must be logged in to access this page.")
        if st.button("Go to Login"):
            st.switch_page("app.py")
        st.stop()

def require_role(required_role):
    """Check if user has required role."""
    if st.session_state.user_role != required_role:
        st.error(f"⛔ Access denied. {required_role} role required.")
        st.stop()