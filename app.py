from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Sai", available_minutes=45)

owner = st.session_state.owner

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner)

scheduler = st.session_state.scheduler


def clear_plan():
    """Clear the displayed plan when its inputs change."""
    scheduler.scheduled_tasks.clear()
    scheduler.explanations.clear()


def complete_selected_task():
    """Complete the chosen task through its owning pet.

    Runs as a button callback, so it finishes before the page is redrawn
    and the task tables show the new state immediately.
    """
    selection = st.session_state.get("complete_choice")
    if selection is None:
        return
    pet_index, task_index = selection
    pet = owner.pets[pet_index]
    task = pet.tasks[task_index]
    next_task = pet.complete_task(task)
    clear_plan()
    st.session_state.completion_message = (pet.name, task.name, next_task)


st.title("🐾 PawPal+")
st.write("Manage your pets and build a daily care plan.")

st.subheader("Owner Settings")

with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    available_minutes = st.number_input(
        "Available time (minutes)",
        min_value=0,
        value=owner.available_minutes,
    )
    preferences = st.multiselect(
        "Preferred categories",
        ["walk", "feeding", "medication", "enrichment", "grooming", "other"],
        default=owner.preferred_categories,
    )

    if st.form_submit_button("Save settings"):
        if owner_name.strip():
            owner.name = owner_name.strip()
            owner.update_available_time(int(available_minutes))
            owner.preferred_categories = preferences
            clear_plan()
            st.success("Owner settings saved.")
        else:
            st.error("Enter an owner name.")

st.subheader("Add a Pet")

with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, value=1)

    if st.form_submit_button("Add pet"):
        if pet_name.strip():
            pet = Pet(
                name=pet_name.strip(),
                species=species,
                age=int(age),
            )
            owner.add_pet(pet)
            clear_plan()
            st.success(f"Added {pet.name}.")
        else:
            st.error("Enter a pet name.")

if owner.pets:
    st.write("Your pets:")
    st.table([
        {"Name": pet.name, "Species": pet.species, "Age": pet.age}
        for pet in owner.pets
    ])

    st.subheader("Add a Task")

    with st.form("task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet",
            options=range(len(owner.pets)),
            format_func=lambda index: (
                f"{index + 1}. {owner.pets[index].name}"
            ),
        )
        task_title = st.text_input("Task title")
        description = st.text_input("Description (optional)")
        category = st.selectbox(
            "Category",
            ["walk", "feeding", "medication", "enrichment", "grooming", "other"],
        )
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        st.caption(
            "Daily and weekly tasks create their next occurrence "
            "when completed."
        )
        due_date = st.date_input("Due date", value=date.today())
        has_time = st.checkbox("Set a scheduled time")
        scheduled_time = st.time_input("Scheduled time", value=time(8, 0))
        st.caption("The scheduled time is used only when the box above is checked.")

        if st.form_submit_button("Add task"):
            if task_title.strip():
                priority_values = {"high": 1, "medium": 2, "low": 3}

                try:
                    task = Task(
                        name=task_title.strip(),
                        category=category,
                        duration_minutes=int(duration),
                        priority=priority_values[priority],
                        description=description.strip(),
                        frequency=frequency,
                        due_date=due_date,
                        scheduled_time=(
                            scheduled_time.strftime("%H:%M") if has_time else None
                        ),
                    )
                except ValueError as error:
                    st.error(str(error))
                else:
                    owner.pets[pet_index].add_task(task)
                    clear_plan()
                    st.success("Task added.")
            else:
                st.error("Enter a task title.")

else:
    st.info("Add a pet to start creating tasks.")

st.subheader("Current Tasks")

priority_labels = {1: "high", 2: "medium", 3: "low"}


def due_label(task):
    """Show a missing due date as today, matching the backend."""
    return str(task.due_date) if task.due_date else "Today"


def task_row(pet_name, task):
    """Build one table row describing a task."""
    return {
        "Pet": pet_name,
        "Task": task.name,
        "Due": due_label(task),
        "Time": task.scheduled_time or "-",
        "Minutes": task.duration_minutes,
        "Priority": priority_labels[task.priority],
        "Frequency": task.frequency,
        "Status": "Done" if task.completed else "Pending",
    }


# Tasks hold no pet reference, so look up the owner by identity.
pet_by_task = {id(task): pet for pet in owner.pets for task in pet.tasks}

completion = st.session_state.pop("completion_message", None)
if completion:
    done_pet, done_name, next_task = completion
    st.success(f"Completed {done_name} for {done_pet}.")
    if next_task is not None:
        st.success(f"Next occurrence of {done_name} is due {due_label(next_task)}.")

owner_conflicts = scheduler.detect_conflicts()
for warning in owner_conflicts:
    st.warning(warning)
if owner_conflicts:
    st.caption(
        "Conflict warnings check for matching start times only, "
        "not overlapping durations."
    )

if owner.get_all_tasks():
    filter_pet_col, filter_status_col = st.columns(2)
    pet_names = list(dict.fromkeys(pet.name for pet in owner.pets))
    pet_filter = filter_pet_col.selectbox("Filter by pet", ["All pets", *pet_names])
    status_filter = filter_status_col.selectbox(
        "Filter by status", ["All", "Pending", "Done"]
    )

    visible = scheduler.filter_tasks(
        pet_name=None if pet_filter == "All pets" else pet_filter,
        completed={"All": None, "Pending": False, "Done": True}[status_filter],
    )
    visible = scheduler.sort_by_time(visible)

    if visible:
        st.table([task_row(pet_by_task[id(task)].name, task) for task in visible])
    else:
        st.info("No tasks match these filters.")

    pending = [
        (pet_index, task_index)
        for pet_index, pet in enumerate(owner.pets)
        for task_index, task in enumerate(pet.tasks)
        if not task.completed
    ]
    if pending:
        st.selectbox(
            "Task to complete",
            options=pending,
            key="complete_choice",
            format_func=lambda choice: (
                f"{owner.pets[choice[0]].name}: "
                f"{owner.pets[choice[0]].tasks[choice[1]].name} "
                f"(due {due_label(owner.pets[choice[0]].tasks[choice[1]])})"
            ),
        )
        st.button("Mark complete", on_click=complete_selected_task)
else:
    st.info("No tasks yet.")

st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler.generate_plan()

if scheduler.explanations:
    if scheduler.scheduled_tasks:
        # Selection is priority-based; display is chronological.
        ordered_plan = scheduler.sort_by_time(scheduler.scheduled_tasks)
        st.table([task_row(pet_by_task[id(task)].name, task) for task in ordered_plan])
        st.caption(
            "Tasks were chosen by priority and available time, "
            "and are shown in time order with untimed tasks last."
        )

        total_minutes = sum(
            task.duration_minutes for task in scheduler.scheduled_tasks
        )
        st.write(
            f"Total scheduled: {total_minutes} / "
            f"{owner.available_minutes} minutes"
        )
    else:
        st.info("No tasks fit the current plan.")

    st.write("Why this plan?")
    for explanation in scheduler.explain_plan():
        st.write(f"- {explanation}")
elif not owner.get_all_tasks():
    st.info("Add tasks before generating a schedule.")
else:
    st.info("Click Generate schedule to build your plan.")
