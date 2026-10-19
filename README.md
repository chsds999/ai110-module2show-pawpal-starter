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
- **Pet:** Stores pet information and supports adding and removing tasks.
- **Task:** Stores an activity's name, description, category, duration, priority, frequency, and completion status.
- **Scheduler:** Retrieves tasks through the Owner, selects tasks within the time budget, and explains its decisions.

The CLI demo in `main.py` demonstrates scheduling tasks for two pets. Streamlit integration and automated tests are upcoming steps.

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
- `app.py`: Streamlit UI starter.
- `diagrams/uml_draft.mmd`: Initial UML class diagram.
- `reflection.md`: Design decisions and project reflections.
- `ai_interactions.md`: AI collaboration notes.
- `requirements.txt`: Project dependencies.

## Sample Output

Actual output from running `python main.py`:

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
```

## Scheduling Behavior

Priority values are **1 = high, 2 = medium, and 3 = low**.

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Multi-pet scheduling | `Owner.get_all_tasks()`, `Scheduler.generate_plan()` | Retrieves tasks from every pet belonging to the owner. |
| Task sorting | `Scheduler.generate_plan()` | Sorts by priority, then preferred category. Preserves original order for remaining ties. |
| Time filtering | `Scheduler.generate_plan()` | Skips tasks that exceed the remaining time and continues checking other tasks. |
| Completion filtering | `Scheduler.generate_plan()` | Skips completed tasks. |
| Plan explanations | `Scheduler.explain_plan()` | Explains why each task was selected or skipped. |
| Input validation | `Owner.update_available_time()`, `Task.update_details()` | Rejects negative available time, nonpositive task durations, and priorities outside 1–3. |
| Plan regeneration | `Scheduler.generate_plan()` | Clears the previous plan and explanations before rebuilding. |
| Conflict handling | Not implemented | The current plan uses a total time budget without appointment times or overlapping time slots. |
| Recurring tasks | `Task.frequency` | Stores frequency; automatic recurrence and due-date tracking are not implemented. |

## Testing

Automated tests will be added in the next project step.

Install pytest and run tests with:

```bash
python -m pip install pytest
python -m pytest
```

For optional coverage reporting:

```bash
python -m pip install pytest-cov
python -m pytest --cov=pawpal_system
```

### Test Results

Pending implementation and execution of the initial automated tests.

## CLI Demo Walkthrough

1. Run `python main.py`.
2. The script creates an owner with 45 minutes available and a preference for walks.
3. It creates two pets: Biscuit and Luna.
4. It adds walking, grooming, feeding, and playtime tasks.
5. The scheduler retrieves tasks from both pets and orders them by priority and preference.
6. It selects the walk, feeding, and playtime tasks, totaling 45 minutes.
7. It prints the plan and explains why grooming was skipped.

## Next Steps

- Add automated tests for task completion and task addition.
- Test important scheduling behaviors and edge cases.
- Connect the backend to the Streamlit UI.
- Update the UML to match the final implementation.
- Complete the remaining project reflections.