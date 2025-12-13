import streamlit as st
import os
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.title(" Login to Intelligence Platform")

# Get the correct database path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
db_path = os.path.join(project_root, "intelligence_platform.db")

print(f"Database path: {db_path}")  # Debugging

# Create DatabaseManager and AuthManager
try:
    db = DatabaseManager(db_path)
    auth = AuthManager(db)
    print(" Database and AuthManager initialized successfully")
except Exception as e:
    st.error(f"Failed to initialize database: {e}")
    import traceback
    st.code(traceback.format_exc())
    st.stop()

# Create tabs
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.header("Existing Users")

    # Text input widget
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Button widget
    if st.button("Login"):
        if username and password:
            user = auth.login_user(username, password)
            if user is None:
                st.error("Login failed: Invalid username or password")
            else:
                st.success(f"Welcome, {user.get_username()}!")
                # Set session state
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.user_role = user.get_role()
                st.rerun()
        else:
            st.warning("Please enter both username and password")

with tab2:
    st.header("New User Registration")

    # Registration form
    new_user = st.text_input("Choose Username")
    new_pass = st.text_input("Choose Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    # Selectbox
    role = st.selectbox("Select Role", ["user", "analyst", "admin"])

    # Checkbox
    agree = st.checkbox("I agree to terms and conditions")

    if st.button("Register"):
        if not agree:
            st.error("You must agree to the terms")
        elif new_pass != confirm_pass:
            st.error("Passwords don't match")
        elif new_user and new_pass:
            # Validate username
            is_valid_username, username_error = auth.validate_username(new_user)
            if not is_valid_username:
                st.error(username_error)
            else:
                # Validate password
                is_valid_password, password_error = auth.validate_password(new_pass)
                if not is_valid_password:
                    st.error(password_error)
                else:
                    success = auth.register_user(new_user, new_pass, role)
                    if success:
                        st.success(f"User '{new_user}' registered successfully!")
                    else:
                        st.error(f"Registration failed: Username '{new_user}' may already exist")
        else:
            st.warning("Please fill all fields")

# Show test credentials
with st.expander("🔧 Test Credentials"):
    st.markdown("""
    **For testing:**
    - Username: `alice`
    - Password: `SecurePass123!`
    - Role: `analyst`
    """)