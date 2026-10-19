from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task

TODAY = date.today()


def make_pet(task):
    pet = Pet("Biscuit", "Dog", 3)
    pet.add_task(task)
    return pet


def test_daily_task_creates_next_occurrence():
    task = Task("Walk", "walk", 30, 1, frequency="daily", due_date=TODAY)
    pet = make_pet(task)

    new_task = pet.complete_task(task)

    assert task.completed is True
    assert new_task is pet.tasks[-1]
    assert new_task is not task
    assert new_task.completed is False
    assert new_task.due_date == TODAY + timedelta(days=1)
    assert (new_task.name, new_task.category, new_task.duration_minutes) == (
        "Walk", "walk", 30
    )
    assert new_task.frequency == "daily"


def test_weekly_task_creates_next_occurrence():
    task = Task("Bath", "grooming", 15, 3, frequency="weekly", due_date=TODAY)
    pet = make_pet(task)

    new_task = pet.complete_task(task)

    assert new_task.due_date == TODAY + timedelta(days=7)


def test_none_due_date_is_treated_as_today():
    task = Task("Walk", "walk", 30, 1, frequency="daily")
    pet = make_pet(task)

    assert pet.complete_task(task).due_date == TODAY + timedelta(days=1)


def test_overdue_task_recurs_from_today():
    task = Task(
        "Walk", "walk", 30, 1, frequency="daily",
        due_date=TODAY - timedelta(days=10),
    )
    pet = make_pet(task)

    assert pet.complete_task(task).due_date == TODAY + timedelta(days=1)


def test_future_task_recurs_from_its_due_date():
    due = TODAY + timedelta(days=3)
    task = Task("Walk", "walk", 30, 1, frequency="daily", due_date=due)
    pet = make_pet(task)

    assert pet.complete_task(task).due_date == due + timedelta(days=1)


def test_once_task_creates_nothing():
    task = Task("Vet", "other", 30, 1, frequency="once")
    pet = make_pet(task)

    assert pet.complete_task(task) is None
    assert task.completed is True
    assert pet.tasks == [task]


def test_repeated_completion_does_not_duplicate():
    task = Task("Walk", "walk", 30, 1, frequency="daily")
    pet = make_pet(task)

    pet.complete_task(task)
    assert pet.complete_task(task) is None
    assert pet.complete_task(task) is None

    assert len(pet.tasks) == 2


def test_task_from_another_pet_is_rejected():
    task = Task("Walk", "walk", 30, 1)
    make_pet(task)
    other = Pet("Luna", "Cat", 2)

    with pytest.raises(ValueError):
        other.complete_task(task)
    assert task.completed is False


def test_equal_copy_is_not_accepted_as_owned_task():
    pet = make_pet(Task("Walk", "walk", 30, 1))

    with pytest.raises(ValueError):
        pet.complete_task(Task("Walk", "walk", 30, 1))


def test_plan_skips_future_tasks_but_keeps_today_and_undated():
    owner = Owner("Sai", 120)
    pet = Pet("Biscuit", "Dog", 3)
    owner.add_pet(pet)
    undated = Task("Undated", "walk", 10, 1)
    today = Task("Today", "walk", 10, 1, due_date=TODAY)
    future = Task("Future", "walk", 10, 1, due_date=TODAY + timedelta(days=1))
    for task in (undated, today, future):
        pet.add_task(task)
    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan == [undated, today]
    assert any("Skipped Future: not due" in e for e in scheduler.explain_plan())


def test_completed_recurring_task_is_not_replanned_today():
    owner = Owner("Sai", 60)
    pet = Pet("Biscuit", "Dog", 3)
    owner.add_pet(pet)
    task = Task("Walk", "walk", 30, 1, frequency="daily")
    pet.add_task(task)
    pet.complete_task(task)

    assert Scheduler(owner).generate_plan() == []
