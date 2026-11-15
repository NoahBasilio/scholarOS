import streamlit as st
import time

st.set_page_config(layout="wide")
supabase = st.session_state["supabase"]

with st.container(border=True):
    subject_res = supabase.table("todo").select("*").eq("user_id", st.session_state["user"].get("id")).execute()

    if "subjects" not in st.session_state:
        st.session_state["subjects"] = ["Other"]



    st.title("To-Do List")
    col1, col2 = st.columns(2)

    with col1:
        with st.popover("+ Add Subject"):
            new_subject = st.text_input("Subject Name")
            submit_subject = st.button("Save Subject")
            st.caption("Add a task to a created subject to save it permanently. This will be fixed later... Sorry!")

            if submit_subject and new_subject.strip() and new_subject.strip() not in st.session_state["subjects"]:
                if new_subject.strip() not in st.session_state["subjects"]:
                    st.session_state["subjects"].append(new_subject.strip())


    for i in subject_res.data:
        if i.get("subject") and i.get("subject") not in st.session_state["subjects"]: # type: ignore
            st.session_state["subjects"].append(i.get("subject")) # type: ignore

    with col2:
        with st.popover("+ New Task"):
            new_task = st.text_input("Task Name")
            due_date = st.date_input("Due Date")
            due_date = due_date.isoformat()
            priority = st.selectbox("Priority", ["None", "Low", "Medium", "High"])
            task_subject = st.selectbox("Subject", st.session_state["subjects"])
            submit_task = st.button("Save Task")

            if submit_task:
                if new_task.strip():
                    supabase.table("todo").insert({"user_id": st.session_state["user"].get("id"), "task": new_task.strip(), "due_date": due_date, "priority": priority, "subject": task_subject, "is_done": False}).execute()
                    time.sleep(0.5)
                    st.rerun()

    # Sorry for all the "type: ignore" comments... Pylance doesn't stop bugging me about the strict typing LMAO
    for subject in st.session_state["subjects"]:
        tasks_for_subject = [row for row in subject_res.data if row.get("subject") == subject] # type: ignore

        with st.container(border=True):
            st.subheader(subject)
            if not tasks_for_subject:
                st.write("No tasks for this subject.")
            else:
                for task in tasks_for_subject:
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        checked = st.checkbox(task["task"], value=task["is_done"], key=f"done_{task['id']}") # type: ignore
                    with c2:
                        st.write(task["due_date"]) # type: ignore
                    with c3:
                        st.write(task["priority"]) # type: ignore
                    with c4:
                        deleted_check = st.button("Delete Task", key=f"del_{task['id']}") # type: ignore
                    
                    if checked != task["is_done"]: # type: ignore
                        supabase.table("todo").update({"is_done": checked}).eq("id", task["id"]).execute() # type: ignore
                        time.sleep(0.5)
                        st.rerun()

                    if deleted_check:
                        supabase.table("todo").delete().eq("id", task["id"]).execute() # type: ignore
                        time.sleep(0.5)
                        st.rerun()
