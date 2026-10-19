from __future__ import annotations

from dataclasses import dataclass, field


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

    def __post_init__(self) -> None:
        """Validate the initial duration and priority."""
        self.update_details(self.duration_minutes, self.priority)

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
        """Select incomplete tasks by priority, preferences, and time."""
        self.scheduled_tasks.clear()
        self.explanations.clear()
        remaining_minutes = self.owner.available_minutes

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

    def explain_plan(self) -> list[str]:
        """Return explanations for the most recently generated plan."""
        return self.explanations.copy()