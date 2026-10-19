from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta

VALID_FREQUENCIES = ("once", "daily", "weekly")
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Owner:
    """Stores owner information, preferences, and pets."""

    name: str
    available_minutes: int
    preferred_categories: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the initial available time."""
        self.update_available_time(self.available_minutes)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def update_available_time(self, minutes: int) -> None:
        """Update available time without allowing negative values."""
        if minutes < 0:
            raise ValueError("Available time cannot be negative.")
        self.available_minutes = minutes

    def get_all_tasks(self) -> list[Task]:
        """Return tasks from every pet belonging to the owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Pet:
    """Stores pet information and care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from the pet."""
        self.tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and add its next occurrence if it recurs.

        Returns the new task, or None if nothing was created. Completing an
        already completed task does nothing, so repeats never duplicate it.
        """
        if not any(pet_task is task for pet_task in self.tasks):
            raise ValueError(f"{task.name} does not belong to {self.name}.")
        if task.completed:
            return None

        task.mark_complete()

        days = RECURRENCE_DAYS.get(task.frequency)
        if days is None:
            return None

        # Overdue tasks recur from today, not from their old due date.
        today = date.today()
        base = max(task.due_date or today, today)
        next_task = replace(
            task,
            completed=False,
            due_date=base + timedelta(days=days),
        )
        self.tasks.append(next_task)
        return next_task


@dataclass
class Task:
    """Represents one pet care activity."""

    name: str
    category: str
    duration_minutes: int
    priority: int  # 1 = high, 2 = medium, 3 = low
    completed: bool = False
    description: str = ""
    frequency: str = "daily"
    due_date: date | None = None  # None is treated as today
    scheduled_time: str | None = None  # "HH:MM"; None means untimed

    def __post_init__(self) -> None:
        """Validate the initial duration, priority, frequency, and time."""
        self.update_details(self.duration_minutes, self.priority)
        if self.frequency not in VALID_FREQUENCIES:
            raise ValueError(
                f"Frequency must be one of {', '.join(VALID_FREQUENCIES)}."
            )
        self._validate_scheduled_time(self.scheduled_time)

    @staticmethod
    def _validate_scheduled_time(value: str | None) -> None:
        """Require a zero-padded 24-hour HH:MM string, or None."""
        if value is None:
            return
        try:
            if len(value) != 5:
                raise ValueError
            datetime.strptime(value, "%H:%M")
        except (ValueError, TypeError):
            raise ValueError("Scheduled time must use HH:MM format.") from None

    def update_details(
        self,
        duration_minutes: int,
        priority: int,
    ) -> None:
        """Update the task after validating duration and priority."""
        if duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if priority not in (1, 2, 3):
            raise ValueError("Priority must be 1, 2, or 3.")

        self.duration_minutes = duration_minutes
        self.priority = priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Scheduler:
    """Builds a daily plan across the owner's pets."""

    owner: Owner
    scheduled_tasks: list[Task] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)

    def generate_plan(self) -> list[Task]:
        """Select due, incomplete tasks by priority, preferences, and time."""
        self.scheduled_tasks.clear()
        self.explanations.clear()
        remaining_minutes = self.owner.available_minutes
        today = date.today()

        # Retrieve tasks from ALL pets through the Owner method.
        tasks = self.owner.get_all_tasks()

        # Lower priority numbers come first.
        # For equal priorities, preferred categories come first.
        # Original order is preserved for remaining ties.
        tasks = sorted(
            tasks,
            key=lambda task: (
                task.priority,
                task.category not in self.owner.preferred_categories,
            ),
        )

        for task in tasks:
            if task.completed:
                self.explanations.append(
                    f"Skipped {task.name}: already completed."
                )
                continue

            if task.due_date is not None and task.due_date > today:
                self.explanations.append(
                    f"Skipped {task.name}: not due until {task.due_date}."
                )
                continue

            if task.duration_minutes <= remaining_minutes:
                self.scheduled_tasks.append(task)
                remaining_minutes -= task.duration_minutes

                preference_note = ""
                if task.category in self.owner.preferred_categories:
                    preference_note = " Matches an owner preference."

                self.explanations.append(
                    f"Selected {task.name}: priority {task.priority}, "
                    f"fits the remaining time.{preference_note}"
                )
            else:
                self.explanations.append(
                    f"Skipped {task.name}: needs {task.duration_minutes} "
                    f"minutes, but only {remaining_minutes} remain."
                )

        return self.scheduled_tasks.copy()

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by scheduled time, untimed tasks last."""
        return sorted(
            tasks,
            key=lambda task: (
                task.scheduled_time is None,
                task.scheduled_time or "",
            ),
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks matching the given pet name and completion status.

        Filters are optional and combined with AND. Tasks are read from each
        pet's own list, so no pet information is stored on the task.
        """
        matches = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                matches.append(task)
        return matches

    def detect_conflicts(self) -> list[str]:
        """Warn about incomplete timed tasks sharing a date and time.

        Checks across all pets since one owner cannot do two things at once.
        Untimed and completed tasks are ignored, and a missing due date
        counts as today. Only exact matches are reported.
        """
        today = date.today()
        slots: dict[tuple[date, str], list[tuple[str, Task]]] = {}
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed or task.scheduled_time is None:
                    continue
                slot = (task.due_date or today, task.scheduled_time)
                slots.setdefault(slot, []).append((pet.name, task))

        warnings = []
        for (day, time), entries in sorted(slots.items()):
            if len(entries) < 2:
                continue
            clashing = ", ".join(
                f"{pet_name} ({task.name})" for pet_name, task in entries
            )
            warnings.append(f"Conflict on {day} at {time}: {clashing}.")
        return warnings

    def explain_plan(self) -> list[str]:
        """Return explanations for the most recently generated plan."""
        return self.explanations.copy()