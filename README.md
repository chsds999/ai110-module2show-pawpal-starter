# PawPal+ (Module 2 Project)

PawPal+ helps pet owners organize care tasks and generate a daily plan based on available time, task priorities, and preferences.

## Scenario

A busy pet owner needs help staying consistent with pet care. The app:

- Tracks tasks such as walks, feeding, medication, enrichment, and grooming across several pets.
- Considers available time, priorities, and owner preferences.
- Produces a daily plan and explains why tasks were selected or skipped.

## Features

- **Owner and pet management:** set the owner's name, available minutes, and preferred categories, and add any number of pets.
- **Tasks with details:** category, description, duration, priority (1 = high, 2 = medium, 3 = low), frequency (`once`, `daily`, `weekly`), a due date, and an optional `HH:MM` start time. Invalid values are rejected.
- **Priority-based planning:** tasks are chosen by priority, then preferred category, then pet order and task order. A task that does not fit the remaining time is skipped and smaller tasks are still considered.
- **Plan explanations:** every task is reported as selected or skipped, with the reason (completed, not yet due, or not enough time left).
- **Sorting:** tasks are ordered by time of day, with untimed tasks last. The plan is shown in this order, but time does not affect which tasks are selected.
- **Filtering:** by pet name and by completion status, combined when both are set.
- **Recurring tasks:** completing a daily or weekly task creates the next occurrence due 1 or 7 days later (counted from today if the task was overdue). One-time tasks create nothing, and completing a task twice never duplicates it.
- **Conflict warnings:** incomplete timed tasks that share a date and start time are reported, across pets and within one pet. Warnings never block the plan.

The backend is four classes in `pawpal_system.py` (`Owner`, `Pet`, `Task`, `Scheduler`). See the [final UML diagram](diagrams/uml_final.mmd).

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

### Run

```bash
streamlit run app.py   # Streamlit UI
python main.py         # CLI demo
python -m pytest       # tests
```

## Project Files

- `pawpal_system.py`: Backend classes and scheduling logic.
- `app.py`: Streamlit UI.
- `main.py`: Terminal demonstration using two pets.
- `tests/`: Automated tests for the backend.
- `diagrams/uml_final.mmd`: Final UML class diagram. `diagrams/uml.mmd` is the initial draft.
- `reflection.md`: Design decisions and project reflections.
- `ai_interactions.md`: AI collaboration notes.
- `requirements.txt`: Project dependencies.

## Using the App

1. Start the UI with `streamlit run app.py`.
2. Under **Owner Settings**, enter your name, available minutes, and preferred categories, then save.
3. Under **Add a Pet**, add one or more pets.
4. Under **Add a Task**, choose a pet and fill in the title, category, duration, priority, frequency, and due date. Tick **Set a scheduled time** to give the task a start time, or leave it unticked for an untimed task.
5. In **Current Tasks**, use **Filter by pet** and **Filter by status** to narrow the table. Rows are sorted by time, with untimed tasks last.
6. If two pending tasks share a date and start time, a warning appears above the table. It compares start times only, not overlapping durations.
7. To finish a task, pick it under **Task to complete** and click **Mark complete**. Completing a daily or weekly task shows the next due date and adds the new occurrence to the table.
8. Click **Generate schedule** to build the plan. Tasks are chosen by priority and available time, shown in time order, and explained under **Why this plan?**. Any change to owners, pets, or tasks clears the old plan.

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

## Limitations

- Conflict detection compares exact start times only and ignores task durations, so overlapping tasks with different start times are not flagged.
- There is no automatic rescheduling. Conflicts are reported, and the owner must fix them.
- Data is stored in the Streamlit session only, so pets and tasks are lost when the session ends.
- Recurrence is created only by `Pet.complete_task()`. Calling `Task.mark_complete()` directly does not create a next occurrence.
