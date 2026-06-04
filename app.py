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

st.title("✅ AI Todo List")

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