import streamlit as st
from app.services.user_service import login_user, register_user

st.title("🔐 Login to Intelligence Platform")

# Create tabs as in tutorial
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.header("Existing Users")

    # Text input widget from tutorial
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Button widget from tutorial
    if st.button("Login"):
        if username and password:
            success, message, user_data = login_user(username, password)
            if success:
                st.success(f"Welcome, {username}! 👋")
                # Set session state (we'll add proper session later)
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error(message)
        else:
            st.warning("Please enter both username and password")

with tab2:
    st.header("New User Registration")

    # Registration form using tutorial widgets
    new_user = st.text_input("Choose Username")
    new_pass = st.text_input("Choose Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    # Selectbox from tutorial
    role = st.selectbox("Select Role", ["user", "analyst", "admin"])

    # Checkbox from tutorial
    agree = st.checkbox("I agree to terms and conditions")

    if st.button("Register"):
        if not agree:
            st.error("You must agree to the terms")
        elif new_pass != confirm_pass:
            st.error("Passwords don't match")
        elif new_user and new_pass:
            success, message = register_user(new_user, new_pass, role)
            if success:
                st.success(message)
            else:
                st.error(message)
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