import streamlit as st
import requests
import os

api_url = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🔄 Database Migrations")
st.markdown("Trigger, monitor, and rollback database migrations.")
st.markdown("---")

tab1, tab2 = st.tabs(["▶ Run Migration", "↩ Rollback"])

with tab1:
    st.subheader("Run a New Migration")
    with st.form("run_migration"):
        migration_name = st.text_input("Migration Name", placeholder="e.g. add_users_table")
        target_db = st.selectbox("Target Database", ["production", "staging", "dev"])
        dry_run = st.checkbox("Dry Run (preview only, no changes applied)", value=True)
        sql_script = st.text_area(
            "SQL Script",
            height=200,
            placeholder="ALTER TABLE users ADD COLUMN last_login TIMESTAMP;",
        )
        submitted = st.form_submit_button("🚀 Run Migration")

    if submitted:
        if not migration_name or not sql_script:
            st.error("Migration name and SQL script are required.")
        else:
            with st.spinner("Running migration..."):
                payload = {
                    "name": migration_name,
                    "target_db": target_db,
                    "dry_run": dry_run,
                    "sql_script": sql_script,
                }
                try:
                    r = requests.post(f"{api_url}/migrations/run", json=payload, timeout=30)
                    if r.status_code == 200:
                        result = r.json()
                        st.success(f"Migration completed: {result.get('message')}")
                        st.json(result)
                    else:
                        st.error(f"Migration failed: {r.text}")
                except Exception as e:
                    st.error(f"Could not reach backend: {e}")

with tab2:
    st.subheader("Rollback Last Migration")
    target_db_rb = st.selectbox("Target Database", ["production", "staging", "dev"], key="rb_db")
    if st.button("↩ Rollback Last Migration", type="primary"):
        with st.spinner("Rolling back..."):
            try:
                r = requests.post(
                    f"{api_url}/migrations/rollback",
                    json={"target_db": target_db_rb},
                    timeout=30,
                )
                if r.status_code == 200:
                    st.success("Rollback successful.")
                    st.json(r.json())
                else:
                    st.error(f"Rollback failed: {r.text}")
            except Exception as e:
                st.error(f"Could not reach backend: {e}")
