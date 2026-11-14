import streamlit as st
from st_supabase_connection import SupabaseConnection


conn = st.connection("supabase", type=SupabaseConnection)
supabase = conn.session_client()

st.write("You're logged in!")
st.write("(Theres just nothing here yet...)")