import streamlit as st
import time
from streamlit_cookies_controller import CookieController
from st_supabase_connection import SupabaseConnection
from supabase_auth.errors import AuthApiError, AuthWeakPasswordError

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)
supabase = conn.session_client()
controller = CookieController()

st.set_page_config(initial_sidebar_state="collapsed", page_title="scholarOS")

def auth_page():
    st.title("Welcome!")
    st.write("Sign up/Log in here!")
    tab1, tab2 = st.tabs(["Log In", "Create Account"])
    with tab1:
        with st.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Log In")

            if login_submitted: 
                try:
                    res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_password})
                    if res.user and res.session:
                        profile_res = supabase.table("profiles").select("*").eq("id", res.user.id).single().execute()
                        st.session_state["user"] = profile_res.data
                        st.write(f"Welcome back!")
                        time.sleep(0.5)
                        token = res.session.refresh_token
                        controller.set("refresh_token", token)
                        time.sleep(0.5)
                        st.rerun()
                except Exception as e:
                    st.error(e)





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
                try:
                    res = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    profile = {
                        "id": res.user.id, # type: ignore
                        "username": username,
                        "name": name,
                        "age": age,
                        "school_year": school_year
                    }
                    supabase.table("profiles").insert(profile).execute()
                    st.session_state["user"] = profile
                    st.write(f"Welcome to ScholarOS, {username}!")
                    token = res.session.refresh_token # type: ignore
                    controller.set("refresh_token", token)
                    time.sleep(0.5)
                    st.rerun()
                except AuthWeakPasswordError:
                    st.write(f"Your password has {len(password)} characters and needs to be at least 6 characters long.")
                except AuthApiError:
                    st.write(f"This user already has an account. Maybe try logging in as {username}?")

if "user" not in st.session_state:
    saved_token = controller.get("refresh_token")
    if saved_token:
        try:
            res = supabase.auth.refresh_session(saved_token)
            if res.user and res.session:
                profile_res = supabase.table("profiles").select("*").eq("id", res.user.id).single().execute()
                st.session_state["user"] = profile_res.data
                controller.set("refresh_token", res.session.refresh_token)
                time.sleep(0.5)
                st.rerun()
        except Exception:
            controller.remove("refresh_token")

    pg = st.navigation([st.Page(auth_page, title="scholarOS")])
else:
    pg = st.navigation([st.Page("pages/0_home_page.py", title="Home")])
    with st.sidebar:
        with st.popover("Settings"):
            st.write(f"Logged in as {st.session_state['user'].get('username')}")
            log_out = st.button("Log Out")

            if log_out:
                supabase.auth.sign_out()
                controller.remove("refresh_token")
                time.sleep(0.5)
                del st.session_state["user"]
                st.rerun()


pg.run()