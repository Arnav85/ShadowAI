import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Cloud Janitor",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("🧹 Cloud Janitor")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")
st.sidebar.page_link("app.py", label="🏠 Dashboard")
st.sidebar.page_link("pages/migrations.py", label="🔄 DB Migrations")
st.sidebar.page_link("pages/logs.py", label="📋 Audit Logs")

st.sidebar.markdown("---")
st.sidebar.markdown("**Backend API**")
api_url = os.getenv("BACKEND_URL", "http://localhost:8000")
st.sidebar.code(api_url, language=None)

# Main dashboard
st.title("🧹 Cloud Janitor — Dashboard")
st.markdown("Manage database migrations and cloud resource cleanup from one place.")
st.markdown("---")

# Health check
import requests
col1, col2, col3, col4 = st.columns(4)

def get_health():
    try:
        r = requests.get(f"{api_url}/health", timeout=3)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def get_stats():
    try:
        r = requests.get(f"{api_url}/migrations/stats", timeout=3)
        return r.json() if r.status_code == 200 else {}
    except Exception:
        return {}

health = get_health()
stats = get_stats()

with col1:
    status = "🟢 Online" if health else "🔴 Offline"
    st.metric("API Status", status)

with col2:
    st.metric("Total Migrations", stats.get("total", "—"))

with col3:
    st.metric("Successful", stats.get("success", "—"))

with col4:
    st.metric("Failed", stats.get("failed", "—"))

st.markdown("---")

# Recent jobs table
st.subheader("Recent Migration Jobs")
try:
    r = requests.get(f"{api_url}/migrations/history?limit=10", timeout=5)
    if r.status_code == 200:
        jobs = r.json()
        if jobs:
            import pandas as pd
            df = pd.DataFrame(jobs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No migration jobs found. Run your first migration from the Migrations page.")
    else:
        st.warning("Could not fetch migration history.")
except Exception as e:
    st.error(f"Backend unreachable: {e}")
