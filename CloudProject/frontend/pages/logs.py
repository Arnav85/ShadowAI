import streamlit as st
import requests
import os
import pandas as pd

api_url = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("📋 Audit Logs")
st.markdown("Immutable event log for all migration and janitor operations.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    event_filter = st.selectbox(
        "Filter by Event Type",
        ["All", "migration_run", "migration_rollback", "janitor_scan", "janitor_clean"],
    )
with col2:
    limit = st.number_input("Max rows", min_value=10, max_value=500, value=50, step=10)

if st.button("🔄 Refresh Logs"):
    st.rerun()

params = {"limit": limit}
if event_filter != "All":
    params["event_type"] = event_filter

try:
    r = requests.get(f"{api_url}/logs", params=params, timeout=5)
    if r.status_code == 200:
        logs = r.json()
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No audit logs found.")
    else:
        st.warning(f"Could not fetch logs: {r.text}")
except Exception as e:
    st.error(f"Backend unreachable: {e}")
