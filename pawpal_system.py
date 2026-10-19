from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    """Stores owner information, preferences, and available care time."""

    name: str
    available_minutes: int
    preferred_categories: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        pass

    def update_available_time(self, minutes: int) -> None:
        """Update the owner's available care time."""
        pass


@dataclass
class Pet:
    """Stores pet information and its care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass


@dataclass
class Task:
    """Represents a pet care activity."""

    name: str
    category: str
    duration_minutes: int
    priority: int  # 1 = high, 2 = medium, 3 = low
    completed: bool = False

    def update_details(
        self,
        duration_minutes: int,
        priority: int,
    ) -> None:
        """Update the task's duration and priority."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Scheduler:
    """Builds a daily plan using the owner's constraints."""

    owner: Owner
    scheduled_tasks: list[Task] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)

    def generate_plan(self) -> list[Task]:
        """Select and order tasks within the available time."""
        pass

    def explain_plan(self) -> list[str]:
        """Explain why tasks were selected or skipped."""
        pass