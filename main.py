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

dog.add_task(Task("Morning walk", "walk", 30, 1))
dog.add_task(Task("Grooming", "grooming", 20, 3))
cat.add_task(Task("Feeding", "feeding", 10, 1))
cat.add_task(Task("Playtime", "enrichment", 5, 2))

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