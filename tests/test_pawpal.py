from pawpal_system import Pet, Task


def test_task_completion():
    task = Task("Morning walk", "walk", 30, 1)

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Biscuit", "Dog", 3)
    task = Task("Feeding", "feeding", 10, 1)
    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[-1] is task