
#streamlit run C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\home.py

import streamlit as st
from app.services.user_service import login_user, register_user

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform - Login",
    page_icon="🔑",
    layout="centered"
)

# ---------- Initialize session state (from tutorial) ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

st.title(" Multi-Domain Intelligence Platform")


# If already logged in, go straight to dashboard (from tutorial)
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}** ({st.session_state.user_role}).")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(" Go to Dashboard", type="primary"):
            st.switch_page("pages/dashboard.py")
    with col2:
        if st.button(" Cybersecurity"):
            st.switch_page("pages/cybersecurity.py")
    with col3:
        if st.button(" IT Operations"):
            st.switch_page("pages/it_operations.py")

    if st.button(" Logout"):
        # Clear session state
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.user_data = {}
        st.rerun()

    st.stop()  # Don't show login/register again

# ---------- Tabs: Login / Register (from tutorial) ----------
tab_login, tab_register = st.tabs([" Login", " Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login to Your Account")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", type="primary", key="login_button"):
        if login_username and login_password:
            # Use your actual database authentication
            success, message, user_data = login_user(login_username, login_password)

            if success:
                # Set session state (from tutorial)
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.session_state.user_role = user_data.get('role', 'user')
                st.session_state.user_data = user_data

                st.success(f"Welcome back, {login_username}! ")

                # Redirect to dashboard (from tutorial)
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error(message)
        else:
            st.warning("Please enter username and password")

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Create New Account")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    col1, col2 = st.columns(2)
    with col1:
        role = st.selectbox(
            "Account Role",
            ["user", "analyst", "admin"],
            format_func=lambda x: {
                "user": " User (Basic access)",
                "analyst": " Analyst (Multi-domain access)",
                "admin": " Admin (Full access)"
            }[x]
        )

    with col2:
        st.caption("Role descriptions:")
        st.caption("• User: Access to one domain")
        st.caption("• Analyst: Access to all domains")
        st.caption("• Admin: Full system control")

    if st.button("Create Account", type="primary", key="register_button"):
        # Basic validation (from tutorial)
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Use your actual database registration
            success, message = register_user(new_username, new_password, role)

            if success:
                st.success("Account created! You can now log in from the Login tab.")
                st.info("Tip: Go to the Login tab and sign in with your new account.")

                # Auto-fill login form
                st.session_state.login_username = new_username
                st.session_state.login_password = new_password
            else:
                st.error(message)

# Show test credentials (optional)
with st.expander("🔧 Test Credentials"):
    st.markdown("""
    **For testing purposes:**

    | Username | Password | Role | Access |
    |----------|----------|------|--------|
    | `alice` | `SecurePass123!` | `analyst` | All domains |
    | `admin` | `AdminPass123!` | `admin` | Full system |
    | `user1` | `UserPass123!` | `user` | One domain |

    *Or register your own account*
    """)

# Footer
st.divider()
st.caption(" Multi-domain intelligence platform for CST1510 Coursework 2")