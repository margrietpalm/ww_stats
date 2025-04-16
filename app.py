import streamlit as st
from utils.data_loader import load_data
from components.player_roles import render_player_roles_tab
from components.role_timeline import render_role_timeline_tab
import bcrypt  # Import bcrypt for password hashing

# Hashed credentials
USERNAME = "ikbenburger"
PASSWORD_HASH = b'$2b$12$bdo995MFO9JGmEl3bgaGg.SwZVuzw6/NbblDE2z1B162H9tum12wO'

# Simple authentication
def authenticate():
    """Simple username-password authentication."""
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        # Check username and hashed password
        if username == USERNAME and bcrypt.checkpw(password.encode(), PASSWORD_HASH):
            st.session_state["authenticated"] = True
        else:
            st.sidebar.error("Invalid username or password")

# Check authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    authenticate()
    st.stop()

# Initialize data
st.title("WW Stats")
data = load_data()

# Tabs
tabs = st.tabs(["Rolverdeling per speler", "Tijdlijn per rol"])

# Tab 1: Player Roles
with tabs[0]:
    render_player_roles_tab(data)

# Tab 2: Role Timeline
with tabs[1]:
    render_role_timeline_tab(data)