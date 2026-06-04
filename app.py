import streamlit as st

from supabase_db import (
    get_tasks,
    add_task,
    delete_task,
    update_status
)

from groq_ai import generate_tasks

st.set_page_config(
    page_title="AI Todo List",
    page_icon="✅",
    layout="wide"
)

st.markdown("""
<div style='text-align:center;padding:20px'>
    <h1 style='font-size:48px;color:#38bdf8'>
        AI Todo List
    </h1>
    <p style='font-size:18px;color:#cbd5e1'>
        Organize tasks manually or let AI create your roadmap.
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(
    [
        "Tasks",
        "AI Generator"
    ]
)

# -----------------------------
# TASK TAB
# -----------------------------

with tab1:

    st.subheader("Add New Task")

    title = st.text_input(
        "Task Title"
    )

    description = st.text_area(
        "Description"
    )

    if st.button("Add Task"):

        if title.strip():

            add_task(
                title,
                description
            )

            st.success(
                "Task Added!"
            )

            st.rerun()

    st.divider()

    st.subheader("My Tasks")

    tasks = get_tasks()

    if not tasks:
        st.info(
            "No tasks found."
        )

    for task in tasks:

        col1, col2, col3 = st.columns(
            [6, 2, 1]
        )

        with col1:

            checked = st.checkbox(
                f"{task['title']}",
                value=task["status"],
                key=f"check_{task['id']}"
            )

            if task["description"]:
                st.caption(
                    task["description"]
                )

        with col2:

            if checked != task["status"]:

                update_status(
                    task["id"],
                    checked
                )

                st.rerun()

        with col3:

            if st.button(
                "🗑️",
                key=f"delete_{task['id']}"
            ):

                delete_task(
                    task["id"]
                )

                st.rerun()

# -----------------------------
# AI TAB
# -----------------------------

with tab2:

    st.subheader(
        "AI Task Generator"
    )

    goal = st.text_area(
        "Describe your goal",
        placeholder="Build a portfolio website"
    )

    if st.button(
        "Generate Tasks"
    ):

        if goal.strip():

            with st.spinner(
                "Generating..."
            ):

                result = generate_tasks(
                    goal
                )

            st.markdown(
                result
            )

            st.divider()

            if st.button(
                "Add Generated Tasks"
            ):

                lines = result.split("\n")

                for line in lines:

                    line = line.strip()

                    if not line:
                        continue

                    if line[0].isdigit():

                        task = line.split(
                            ".",
                            1
                        )[-1].strip()

                        if task:
                            add_task(task)

                st.success(
                    "Tasks Added!"
                )

                st.rerun()
                
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Title */
h1 {
    text-align: center;
    color: #38bdf8 !important;
    font-weight: 700;
}

/* Cards */
[data-testid="stVerticalBlock"] > div {
    border-radius: 15px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: linear-gradient(
        135deg,
        #06b6d4,
        #3b82f6
    );
    color: white;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(59,130,246,0.4);
}

/* Input boxes */
.stTextInput input,
.stTextArea textarea {
    border-radius: 12px !important;
    border: 2px solid #334155 !important;
    background-color: #1e293b !important;
    color: white !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
    border-radius: 10px;
}

.stTabs [aria-selected="true"] {
    background-color: #0ea5e9 !important;
    color: white !important;
}

/* Checkbox text */
.stCheckbox label {
    font-size: 16px;
    font-weight: 500;
}

/* Success messages */
.stSuccess {
    border-radius: 10px;
}

/* Info boxes */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)                
