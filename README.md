# SCHOLAROS
Hey! This is scholarOS (it's not ACTUALLY an OS... but don't tell anyone...)! It's a website made with Python and Streamlit and it uses Supabase databases so that users can have accounts and stuff! I made this because I wanted a website that was free and where students could use many features that would prove beneficial to them like a GPA calculator and pomodoro timer, as well as a todo list.
## HOW THIS WAS MADE
This project was made with Python using the Streamlit module and a module that connects Streamlit with Supabase (st_supabase_connection)!

## Live Demo:
**[Open scholarOS](https://scholaros.streamlit.app/)

## heres how to run the project :)
1. Clone the source code to your device
```bash
git clone https://github.com/NoahBasilio/scholarOS
cd scholarOS
```

2. Install the project's dependencies
**Using `uv` (recommended):**
```bash
uv sync
```

**Or using standard `pip` (totally OK too!!):**
```bash
pip install -r requirements.txt
```

## CURRENT FEATURES:
- **User accounts:** Signup and login, powered by Supabase Auth.
- **To-Do List:** Organize your tasks by subject, due date, priority, and includes completion tracking (Also Supabase Database syncing!!
- **Dashboard/Home Page:** A home page where you can see your student metrics (like a "unfinished tasks" metric, and a "time studied" metric, though we're still working on those...)
- **Coming Soon!:** Pomodoro Focus Timer and a Weighted GPA Calculator!!


## AI DISCLOSURE
AI was used to help create Supabase links with Streamlit since this was my first time using Supabase databases.