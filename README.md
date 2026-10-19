# PawPal+ (Module 2 Project)

PawPal+ helps pet owners organize care tasks and generate a daily plan based on available time, task priorities, and preferences.

## Scenario

A busy pet owner needs help staying consistent with pet care. The app is designed to:

- Track tasks such as walks, feeding, medication, enrichment, and grooming.
- Consider available time, priorities, and owner preferences.
- Produce a daily plan and explain why tasks were selected or skipped.

## Current Implementation

The backend works through four Python classes:

- **Owner:** Stores owner information, available time, preferences, and pets. Provides `get_all_tasks()` to retrieve tasks across all pets.
- **Pet:** Stores pet information, supports adding and removing tasks, and completes tasks with `complete_task()`, which creates the next daily or weekly occurrence.
- **Task:** Stores an activity's name, description, category, duration, priority, frequency, completion status, optional due date, and optional `HH:MM` scheduled time.
- **Scheduler:** Retrieves tasks through the Owner, selects tasks within the time budget, sorts and filters tasks, warns about time conflicts, and explains its decisions.

The CLI demo in `main.py` demonstrates scheduling, sorting, filtering, recurrence, and conflict warnings for two pets. The Streamlit UI is connected to the backend but does not yet expose the sorting, filtering, recurrence, or conflict features.

## Getting Started

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

For Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Run the CLI Demo

```bash
python main.py
```

## Project Files

- `pawpal_system.py`: Backend classes and scheduling logic.
- `main.py`: Terminal demonstration using two pets.
- `tests/`: Automated tests for tasks, recurrence, and conflict detection.
- `app.py`: Streamlit UI starter.
- `diagrams/uml_draft.mmd`: Initial UML class diagram.
- `reflection.md`: Design decisions and project reflections.
- `ai_interactions.md`: AI collaboration notes.
- `requirements.txt`: Project dependencies.

## Sample Output

Actual output from running `python main.py` on 2026-10-19. Dates in the recurrence and conflict sections depend on the day the demo is run.

```text
Today's Schedule for Sai
Available time: 45 minutes
----------------------------------------
1. Biscuit: Morning walk (30 min) [priority: 1]
2. Luna: Feeding (10 min) [priority: 1]
3. Luna: Playtime (5 min) [priority: 2]

Total scheduled: 45 minutes

Why this plan?
- Selected Morning walk: priority 1, fits the remaining time. Matches an owner preference.
- Selected Feeding: priority 1, fits the remaining time.
- Selected Playtime: priority 2, fits the remaining time.
- Skipped Grooming: needs 20 minutes, but only 0 remain.

All tasks sorted by time
- 07:30 Luna: Feeding [todo]
- 08:00 Biscuit: Morning walk [todo]
- 18:00 Luna: Playtime [todo]
- --:-- Biscuit: Grooming [done]

Luna's tasks
- 07:30 Luna: Feeding [todo]
- 18:00 Luna: Playtime [todo]

Completed tasks
- --:-- Biscuit: Grooming [done]

Biscuit's incomplete tasks, by time
- 08:00 Biscuit: Morning walk [todo]

Recurrence
- Completed Morning walk; next due 2026-10-20
- Completing it again creates: None
- Weekly Bath next due 2026-10-26
- One-time Vet visit creates: None

Future-dated tasks are skipped:
- Skipped Morning walk: not due until 2026-10-20.
- Skipped Bath: not due until 2026-10-26.

Conflict warnings
- Before adding clashes: none
- Conflict on 2026-10-19 at 09:00: Biscuit (Vet call), Luna (Medication), Luna (Brushing).
- Plan still generates 5 tasks
```

## Smarter Scheduling

Priority values are **1 = high, 2 = medium, and 3 = low**. Tasks may have an optional `due_date` (a missing date is treated as today) and an optional `scheduled_time` in zero-padded 24-hour `HH:MM` format. Frequency must be `once`, `daily`, or `weekly`.

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Multi-pet scheduling | `Owner.get_all_tasks()`, `Scheduler.generate_plan()` | Retrieves tasks from every pet belonging to the owner. |
| Priority scheduling | `Scheduler.generate_plan()` | Sorts by priority, then preferred category, preserving original order for remaining ties. Skips tasks that exceed the remaining time and continues checking other tasks. |
| Skipped tasks | `Scheduler.generate_plan()` | Skips completed tasks and future-dated tasks, with an explanation for each. Tasks due today, overdue, or undated remain eligible. |
| Time sorting | `Scheduler.sort_by_time()` | Returns tasks ordered by `HH:MM` time, with untimed tasks last. Sorts by time of day only, not by date. It does not affect which tasks the plan selects. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status. Filters are optional and combined. |
| Recurring tasks | `Pet.complete_task()` | Marks the task complete. Daily and weekly tasks get a new incomplete copy due 1 or 7 days after `max(due_date or today, today)`, so overdue tasks do not create overdue repeats. `once` tasks create nothing. Completing an already completed task does nothing, so repeated completion never creates duplicates. Raises `ValueError` if the task does not belong to the pet. |
| Conflict warnings | `Scheduler.detect_conflicts()` | Returns warnings for incomplete timed tasks sharing the same date and time across all pets, including the same pet. Ignores completed and untimed tasks. Exact matches only, and it never blocks plan generation. |
| Plan explanations | `Scheduler.explain_plan()` | Explains why each task was selected or skipped. |
| Input validation | `Owner.update_available_time()`, `Task.update_details()`, `Task` construction | Rejects negative available time, nonpositive durations, priorities outside 1–3, invalid frequencies, and times not in `HH:MM` format. |
| Plan regeneration | `Scheduler.generate_plan()` | Clears the previous plan and explanations before rebuilding. |

Limitations: conflict detection compares start times only and ignores task durations, and recurrence is triggered only through `Pet.complete_task()`. Calling `Task.mark_complete()` directly does not create a next occurrence.

## Testing PawPal+

Install pytest and run the suite from the project root with:

```bash
python -m pip install pytest
python -m pytest
```

For optional coverage reporting:

```bash
python -m pip install pytest-cov
python -m pytest --cov=pawpal_system
```

### Behaviors Covered

- **Sorting:** chronological order by `HH:MM`, untimed tasks last, and the input list left unchanged.
- **Filtering:** by pet, by completion status, by both combined, and an unknown pet returning nothing.
- **Multi-pet scheduling:** a shared time budget across pets, priority before preference, preference breaking priority ties, ties resolved by pet order then task order, empty task lists, and repeated generation without duplicates.
- **Time-budget boundaries:** a task that exactly fits is selected, oversized tasks are skipped while smaller ones still fit, and zero available time schedules nothing.
- **Recurrence:** daily, weekly, and one-time tasks, overdue and future due dates, preserved time, description, priority, and category, no duplicates on repeated completion, and rejection of tasks that belong to another pet.
- **Conflicts:** same-time clashes across and within pets, three-way clashes reported once, and different times, different dates, completed tasks, and untimed tasks ignored. Conflicts never block plan generation.
- **Validation:** invalid durations, priorities, frequencies, and `HH:MM` times are rejected.

### Latest Test Results

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/saicherukuru/Desktop/Code Path AI/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 58 items

tests/test_conflicts.py .........                                        [ 15%]
tests/test_pawpal.py ..                                                  [ 18%]
tests/test_recurrence.py ............                                    [ 39%]
tests/test_scheduling.py .........                                       [ 55%]
tests/test_sorting_filtering.py .......                                  [ 67%]
tests/test_validation.py ...................                             [100%]

============================== 58 passed in 0.03s ==============================
```

### Confidence Level: ★★★★☆ (4/5)

The core backend behaviors (scheduling, sorting, filtering, recurrence, conflict warnings, and validation) all pass. Confidence is not 5/5 for two reasons:

- Conflict detection compares exact start times, not overlapping durations, so a 30-minute task at 08:00 and another task at 08:15 are not flagged.
- Automated UI testing is outside this suite, so the Streamlit app in `app.py` is not covered by automated tests.

## CLI Demo Walkthrough

1. Run `python main.py`.
2. The script creates an owner with 45 minutes available and a preference for walks.
3. It creates two pets, Biscuit and Luna, with timed and untimed tasks.
4. The scheduler orders tasks by priority and preference, selects the walk, feeding, and playtime tasks (45 minutes), and explains why grooming was skipped.
5. It sorts tasks by time and filters them by pet and completion status.
6. It completes daily, weekly, and one-time tasks to show recurrence, including that repeated completion creates nothing and future-dated tasks are skipped by the next plan.
7. It adds three tasks at the same time to show a conflict warning, then confirms the plan still generates.

## Next Steps

- Expose time and date inputs, filters, completion (through `Pet.complete_task()`), and conflict warnings in the Streamlit UI.
- Update the UML to match the final implementation.
- Complete the remaining project reflections.
