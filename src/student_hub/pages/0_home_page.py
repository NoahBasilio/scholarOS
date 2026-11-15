import streamlit as st
from st_supabase_connection import SupabaseConnection


conn = st.connection("supabase", type=SupabaseConnection)
supabase = conn.session_client()
st.set_page_config(initial_sidebar_state="collapsed", page_title="scholarOS", layout="wide")
st.title(f"Welcome back, {st.session_state['user'].get('username')}!")

with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Study Time", "0h 0m", border=True, delta="+0m today")

    with col2:
        tasks_res = supabase.table("todo").select("*").eq("user_id", st.session_state["user"].get("id")).eq("is_done", False).execute()
        st.metric("Unfinished Tasks", len(tasks_res.data), border=True)

    with col3:
        st.subheader("Placeholder!")

    with col4:
        st.subheader("Placeholder! (again!)")