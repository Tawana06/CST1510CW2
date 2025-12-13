#streamlit run C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\multi_domain_platform\OOP_home.py [ARGUMENTS]
import os
import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform - Login",
    page_icon="🔑",
    layout="centered"
)
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "intelligence_platform.db")

print(f"Database path: {db_path}")

# Create DatabaseManager and AuthManager
try:
    db = DatabaseManager(db_path)
    auth = AuthManager(db)
except Exception as e:
    st.error(f"Failed to initialize database: {e}")
    st.stop()

# initialisation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

st.title(" Multi-Domain Intelligence Platform")

# If already logged in, go straight to dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}** ({st.session_state.user_role}).")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button(" Go to Dashboard", type="primary"):
            st.switch_page("pages/2_Dashboard.py")
    with col2:
        if st.button(" Cybersecurity"):
            st.switch_page("pages/3_Cybersecurity.py")
    with col3:
        if st.button("Data Science"):
            st.switch_page("pages/4_Data_Science.py")
    with col4:
        if st.button("IT Operations"):
            st.switch_page("pages/5_IT_Operations.py")
    with col5:
        if st.button("🤖 AI Chat"):
            st.switch_page("pages/6_AI_Assistant.py")

    if st.button(" Logout"):
        # Clear session state
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.session_state.user_data = {}
        st.rerun()

    st.stop()  # Don't show login/register again

# tabs using tutorial trial
tab_login, tab_register = st.tabs([" Login", " Register"])

# login tab
with tab_login:
    st.subheader("Login to Your Account")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", type="primary", key="login_button"):
        if login_username and login_password:
            # Use AuthManager for authentication
            user = auth.login_user(login_username, login_password)

            if user:
                # Set session state
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.user_role = user.get_role()
                st.session_state.user_data = {
                    'username': user.get_username(),
                    'role': user.get_role()
                }

                st.success(f"Welcome back, {login_username}! ")

                # Redirect to dashboard
                st.switch_page("pages/2_dashboard.py")
            else:
                st.error("Login failed: Invalid username or password")
        else:
            st.warning("Please enter username and password")

# register tab
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
        # validation
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Validate username
            is_valid_username, username_error = auth.validate_username(new_username)
            if not is_valid_username:
                st.error(username_error)
            else:
                # Validate password
                is_valid_password, password_error = auth.validate_password(new_password)
                if not is_valid_password:
                    st.error(password_error)
                else:
                    # Use AuthManager for registration
                    success = auth.register_user(new_username, new_password, role)

                    if success:
                        st.success("Account created! You can now log in from the Login tab.")
                        st.info("Tip: Go to the Login tab and sign in with your new account.")

                        # Auto-fill login form
                        st.session_state.login_username = new_username
                        st.session_state.login_password = new_password
                    else:
                        st.error(f"Registration failed: Username '{new_username}' may already exist")

# Show test credentials
with st.expander("🔧 Test Credentials"):
    st.markdown("""
    **For testing purposes:**

    | Username | Password | Role | Access |
    |----------|----------|------|--------|
    | `alice` | `SecurePass123!` | `analyst` | All domains |

    *Or register your own account*
    """)

# Footer
st.divider()
st.caption(" Multi-domain intelligence platform for CST1510 Coursework 2")