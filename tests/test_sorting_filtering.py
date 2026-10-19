from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler():
    owner = Owner("Sai", 120)
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Luna", "Cat", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    return dog, cat, Scheduler(owner)


def test_sort_by_time_is_chronological():
    _, _, scheduler = make_scheduler()
    late = Task("Late", "other", 5, 1, scheduled_time="10:30")
    early = Task("Early", "other", 5, 1, scheduled_time="08:15")
    mid = Task("Mid", "other", 5, 1, scheduled_time="09:00")

    assert scheduler.sort_by_time([late, early, mid]) == [early, mid, late]


def test_sort_by_time_puts_untimed_tasks_last():
    _, _, scheduler = make_scheduler()
    untimed = Task("Untimed", "other", 5, 1)
    timed = Task("Timed", "other", 5, 1, scheduled_time="23:59")

    assert scheduler.sort_by_time([untimed, timed]) == [timed, untimed]


def test_sort_by_time_does_not_change_input():
    _, _, scheduler = make_scheduler()
    tasks = [
        Task("B", "other", 5, 1, scheduled_time="10:00"),
        Task("A", "other", 5, 1, scheduled_time="08:00"),
    ]
    original = list(tasks)

    scheduler.sort_by_time(tasks)

    assert tasks == original


def test_filter_by_pet():
    dog, cat, scheduler = make_scheduler()
    walk = Task("Walk", "walk", 30, 1)
    feed = Task("Feed", "feeding", 10, 1)
    dog.add_task(walk)
    cat.add_task(feed)

    assert scheduler.filter_tasks(pet_name="Biscuit") == [walk]
    assert scheduler.filter_tasks(pet_name="Luna") == [feed]


def test_filter_by_completion_status():
    dog, cat, scheduler = make_scheduler()
    done = Task("Walk", "walk", 30, 1)
    todo = Task("Feed", "feeding", 10, 1)
    dog.add_task(done)
    cat.add_task(todo)
    done.mark_complete()

    assert scheduler.filter_tasks(completed=True) == [done]
    assert scheduler.filter_tasks(completed=False) == [todo]


def test_filter_combines_pet_and_status():
    dog, cat, scheduler = make_scheduler()
    done = Task("Walk", "walk", 30, 1)
    todo = Task("Bath", "grooming", 15, 3)
    other = Task("Feed", "feeding", 10, 1)
    dog.add_task(done)
    dog.add_task(todo)
    cat.add_task(other)
    done.mark_complete()

    assert scheduler.filter_tasks(pet_name="Biscuit", completed=False) == [todo]
    assert scheduler.filter_tasks(pet_name="Luna", completed=True) == []


def test_filter_unknown_pet_returns_empty_list():
    dog, _, scheduler = make_scheduler()
    dog.add_task(Task("Walk", "walk", 30, 1))

    assert scheduler.filter_tasks(pet_name="Nobody") == []
