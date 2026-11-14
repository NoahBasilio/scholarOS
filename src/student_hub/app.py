import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

supabase = conn.session_client()

tab1, tab2 = st.tabs(["Log In", "Create Account"])

with tab2:
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        name = st.text_input("Your Name")
        age = st.number_input("Age", min_value=13, max_value=100)
        school_year = st.selectbox("School Year", ["Middle School", "Freshman", "Sophomore", "Junior", "Senior", "College"])
        submitted = st.form_submit_button("Create Account")

        if submitted:
            st.write(f"Welcome to ScholarOS, {username}!")
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            profile = {
                "id": res.user.id,
                "username": username,
                "name": name,
                "age": age,
                "school_year": school_year
            }
            supabase.table("profiles").insert(profile).execute()