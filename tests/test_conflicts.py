from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task

TODAY = date.today()


def setup():
    owner = Owner("Sai", 120)
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat, Scheduler(owner)


def test_cross_pet_conflict_warns_with_details():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1, scheduled_time="08:00"))
    cat.add_task(Task("Feeding", "feeding", 10, 1, scheduled_time="08:00"))

    assert scheduler.detect_conflicts() == [
        f"Conflict on {TODAY} at 08:00: Biscuit (Walk), Luna (Feeding)."
    ]


def test_same_pet_conflict():
    _, dog, _, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1, scheduled_time="08:00"))
    dog.add_task(Task("Bath", "grooming", 15, 3, scheduled_time="08:00"))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Biscuit (Walk), Biscuit (Bath)" in warnings[0]


def test_three_way_clash_is_one_warning():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("A", "other", 5, 1, scheduled_time="08:00"))
    dog.add_task(Task("B", "other", 5, 1, scheduled_time="08:00"))
    cat.add_task(Task("C", "other", 5, 1, scheduled_time="08:00"))

    assert len(scheduler.detect_conflicts()) == 1


def test_different_times_do_not_conflict():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1, scheduled_time="08:00"))
    cat.add_task(Task("Feeding", "feeding", 10, 1, scheduled_time="08:01"))

    assert scheduler.detect_conflicts() == []


def test_different_dates_do_not_conflict():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1, scheduled_time="08:00"))
    cat.add_task(
        Task("Feeding", "feeding", 10, 1, scheduled_time="08:00",
             due_date=TODAY + timedelta(days=1))
    )

    assert scheduler.detect_conflicts() == []


def test_none_due_date_matches_explicit_today():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1, scheduled_time="08:00"))
    cat.add_task(
        Task("Feeding", "feeding", 10, 1, scheduled_time="08:00",
             due_date=TODAY)
    )

    assert len(scheduler.detect_conflicts()) == 1


def test_completed_tasks_are_ignored():
    _, dog, cat, scheduler = setup()
    done = Task("Walk", "walk", 30, 1, scheduled_time="08:00")
    dog.add_task(done)
    cat.add_task(Task("Feeding", "feeding", 10, 1, scheduled_time="08:00"))
    done.mark_complete()

    assert scheduler.detect_conflicts() == []


def test_untimed_tasks_are_ignored():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1))
    cat.add_task(Task("Feeding", "feeding", 10, 1))

    assert scheduler.detect_conflicts() == []


def test_conflicts_do_not_block_plan_generation():
    _, dog, cat, scheduler = setup()
    dog.add_task(Task("Walk", "walk", 30, 1, scheduled_time="08:00"))
    cat.add_task(Task("Feeding", "feeding", 10, 1, scheduled_time="08:00"))

    assert scheduler.detect_conflicts()
    assert len(scheduler.generate_plan()) == 2
