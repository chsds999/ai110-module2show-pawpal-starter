from pawpal_system import Owner, Pet, Task, Scheduler


owner = Owner(
    name="Sai",
    available_minutes=45,
    preferred_categories=["walk"],
)

dog = Pet(name="Biscuit", species="Dog", age=3)
cat = Pet(name="Luna", species="Cat", age=2)

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Morning walk", "walk", 30, 1, scheduled_time="08:00"))
dog.add_task(Task("Grooming", "grooming", 20, 3))
cat.add_task(Task("Feeding", "feeding", 10, 1, scheduled_time="07:30"))
cat.add_task(Task("Playtime", "enrichment", 5, 2, scheduled_time="18:00"))

scheduler = Scheduler(owner)
plan = scheduler.generate_plan()

print(f"Today's Schedule for {owner.name}")
print(f"Available time: {owner.available_minutes} minutes")
print("-" * 40)

total_minutes = 0

for number, task in enumerate(plan, start=1):
    pet_name = next(
        pet.name
        for pet in owner.pets
        if any(pet_task is task for pet_task in pet.tasks)
    )
    print(
        f"{number}. {pet_name}: {task.name} "
        f"({task.duration_minutes} min) [priority: {task.priority}]"
    )
    total_minutes += task.duration_minutes

print(f"\nTotal scheduled: {total_minutes} minutes")
print("\nWhy this plan?")

for explanation in scheduler.explain_plan():
    print(f"- {explanation}")


def pet_name_for(task):
    return next(
        pet.name
        for pet in owner.pets
        if any(pet_task is task for pet_task in pet.tasks)
    )


def show(title, tasks):
    print(f"\n{title}")
    for task in tasks:
        time = task.scheduled_time or "--:--"
        status = "done" if task.completed else "todo"
        print(f"- {time} {pet_name_for(task)}: {task.name} [{status}]")


dog.tasks[1].mark_complete()  # Grooming

show("All tasks sorted by time", scheduler.sort_by_time(owner.get_all_tasks()))
show("Luna's tasks", scheduler.filter_tasks(pet_name="Luna"))
show("Completed tasks", scheduler.filter_tasks(completed=True))
show(
    "Biscuit's incomplete tasks, by time",
    scheduler.sort_by_time(
        scheduler.filter_tasks(pet_name="Biscuit", completed=False)
    ),
)


print("\nRecurrence")
walk = dog.tasks[0]  # Morning walk, daily
next_walk = dog.complete_task(walk)
print(f"- Completed {walk.name}; next due {next_walk.due_date}")
print(f"- Completing it again creates: {dog.complete_task(walk)}")

weekly = Task("Bath", "grooming", 15, 3, frequency="weekly")
dog.add_task(weekly)
print(f"- Weekly {weekly.name} next due {dog.complete_task(weekly).due_date}")

once = Task("Vet visit", "other", 30, 1, frequency="once")
dog.add_task(once)
print(f"- One-time {once.name} creates: {dog.complete_task(once)}")

future_plan = Scheduler(owner)
future_plan.generate_plan()
print("\nFuture-dated tasks are skipped:")
for explanation in future_plan.explain_plan():
    if "not due until" in explanation:
        print(f"- {explanation}")


print("\nConflict warnings")
print(f"- Before adding clashes: {scheduler.detect_conflicts() or 'none'}")
cat.add_task(Task("Medication", "medication", 5, 1, scheduled_time="09:00"))
dog.add_task(Task("Vet call", "other", 10, 2, scheduled_time="09:00"))
cat.add_task(Task("Brushing", "grooming", 10, 3, scheduled_time="09:00"))
for warning in scheduler.detect_conflicts():
    print(f"- {warning}")
print(f"- Plan still generates {len(scheduler.generate_plan())} tasks")
