from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner(minutes, preferred=()):
    owner = Owner("Sai", minutes, preferred_categories=list(preferred))
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


def test_multi_pet_tasks_share_one_budget():
    owner, dog, cat = make_owner(40)
    walk = Task("Walk", "walk", 30, 1)
    feed = Task("Feed", "feeding", 20, 2)
    brush = Task("Brush", "grooming", 10, 3)
    dog.add_task(walk)
    cat.add_task(feed)
    cat.add_task(brush)

    plan = Scheduler(owner).generate_plan()

    assert plan == [walk, brush]


def test_priority_beats_preference():
    owner, dog, cat = make_owner(120, preferred=["grooming"])
    urgent = Task("Meds", "medical", 10, 1)
    preferred = Task("Brush", "grooming", 10, 2)
    dog.add_task(preferred)
    cat.add_task(urgent)

    assert Scheduler(owner).generate_plan() == [urgent, preferred]


def test_preference_breaks_priority_ties():
    owner, dog, _ = make_owner(120, preferred=["grooming"])
    plain = Task("Walk", "walk", 10, 2)
    preferred = Task("Brush", "grooming", 10, 2)
    dog.add_task(plain)
    dog.add_task(preferred)

    assert Scheduler(owner).generate_plan() == [preferred, plain]


def test_full_ties_use_pet_order_then_task_order():
    owner, dog, cat = make_owner(120)
    dog_first = Task("Dog 1", "walk", 10, 1)
    dog_second = Task("Dog 2", "walk", 10, 1)
    cat_first = Task("Cat 1", "walk", 10, 1)
    dog.add_task(dog_first)
    dog.add_task(dog_second)
    cat.add_task(cat_first)

    assert Scheduler(owner).generate_plan() == [dog_first, dog_second, cat_first]


def test_task_that_exactly_fits_the_budget_is_selected():
    owner, dog, _ = make_owner(30)
    walk = Task("Walk", "walk", 30, 1)
    dog.add_task(walk)
    scheduler = Scheduler(owner)

    assert scheduler.generate_plan() == [walk]
    assert not any("Skipped" in e for e in scheduler.explain_plan())


def test_oversized_task_is_skipped_and_smaller_ones_still_fit():
    owner, dog, _ = make_owner(30)
    first = Task("First", "walk", 25, 1)
    too_big = Task("Too big", "walk", 20, 2)
    small = Task("Small", "walk", 5, 3)
    for task in (first, too_big, small):
        dog.add_task(task)
    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan == [first, small]
    assert any(
        "Skipped Too big: needs 20 minutes, but only 5 remain." in e
        for e in scheduler.explain_plan()
    )


def test_no_tasks_gives_empty_plan():
    owner, _, _ = make_owner(60)
    scheduler = Scheduler(owner)

    assert scheduler.generate_plan() == []
    assert scheduler.explain_plan() == []


def test_zero_available_time_schedules_nothing():
    owner, dog, _ = make_owner(0)
    dog.add_task(Task("Walk", "walk", 10, 1))
    scheduler = Scheduler(owner)

    assert scheduler.generate_plan() == []
    assert len(scheduler.explain_plan()) == 1
    assert "Skipped Walk" in scheduler.explain_plan()[0]


def test_repeated_generation_does_not_duplicate():
    owner, dog, cat = make_owner(60)
    dog.add_task(Task("Walk", "walk", 30, 1))
    cat.add_task(Task("Feed", "feeding", 10, 2))
    scheduler = Scheduler(owner)

    first = scheduler.generate_plan()
    first_explanations = scheduler.explain_plan()
    second = scheduler.generate_plan()

    assert second == first
    assert len(scheduler.scheduled_tasks) == 2
    assert scheduler.explain_plan() == first_explanations
