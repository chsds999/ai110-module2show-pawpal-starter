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
        st.caption("Frequency is recorded; automatic recurrence is not implemented.")

        if st.form_submit_button("Add task"):
            if task_title.strip():
                priority_values = {"high": 1, "medium": 2, "low": 3}

                task = Task(
                    name=task_title.strip(),
                    category=category,
                    duration_minutes=int(duration),
                    priority=priority_values[priority],
                    description=description.strip(),
                    frequency=frequency,
                )

                owner.pets[pet_index].add_task(task)
                clear_plan()
                st.success("Task added.")
            else:
                st.error("Enter a task title.")

else:
    st.info("Add a pet to start creating tasks.")

st.subheader("Current Tasks")

priority_labels = {1: "high", 2: "medium", 3: "low"}

task_rows = [
    {
        "Pet": pet.name,
        "Task": task.name,
        "Minutes": task.duration_minutes,
        "Priority": priority_labels[task.priority],
        "Frequency": task.frequency,
        "Completed": task.completed,
    }
    for pet in owner.pets
    for task in pet.tasks
]

if task_rows:
    st.table(task_rows)
else:
    st.info("No tasks yet.")

st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler.generate_plan()

if scheduler.explanations:
    if scheduler.scheduled_tasks:
        schedule_rows = []

        for task in scheduler.scheduled_tasks:
            pet_name = next(
                pet.name
                for pet in owner.pets
                if any(pet_task is task for pet_task in pet.tasks)
            )
            schedule_rows.append({
                "Pet": pet_name,
                "Task": task.name,
                "Minutes": task.duration_minutes,
                "Priority": priority_labels[task.priority],
            })

        st.table(schedule_rows)

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