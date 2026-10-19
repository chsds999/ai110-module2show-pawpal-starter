# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My design includes four classes:

Owner: Stores owner information, available time, preferences, and pets.

Pet: Stores pet information and care tasks.

Task: Stores an activity’s duration, priority, and completion status.

Scheduler: Selects tasks within the available time and explains the plan.

Users can enter owner and pet information, manage tasks, and generate a daily plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. AI reviewed the skeleton and suggested skipping completed tasks, enforcing the time limit, and clearing old plans when generating a new one, and I addressed these during implementation. The design then grew in four ways:

- Tasks gained `frequency`, `due_date`, and an optional `scheduled_time` so the app can handle dates, times, and recurrence.
- `Owner.get_all_tasks()` lets the Scheduler read tasks from every pet without reaching into each pet itself.
- `Pet.complete_task()` handles recurrence. The Pet owns the task list, so it can add the next daily or weekly occurrence when a task is completed.
- The Scheduler gained sorting, filtering, and conflict detection methods.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers available time, task priority, owner preferences, completion status, and due date. Available time is a hard limit, and priority decides which tasks are chosen first. Owner preferences break ties between tasks of equal priority, so a preferred category never outranks a more urgent task. Completed tasks and tasks not yet due are skipped, and each decision is explained.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Conflict detection only checks for matching dates and start times, and it warns without rescheduling anything. A 30-minute task at 08:00 and another at 08:15 are not flagged. This keeps the check simple and predictable, and it leaves the decision with the owner, who knows which task can move. Overlapping-duration detection would be a natural next step.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm classes, create UML, implement the backend, and draft a CLI demo and tests. Providing my existing skeleton and asking for matching code helped keep the design consistent. AI also helped with UI integration, test planning, and documentation. I kept algorithm planning and testing in separate chats, which kept each conversation focused on one job.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I reviewed the AI-generated code against the assignment requirements, especially the requirement for the Scheduler to retrieve all pets' tasks through Owner.get_all_tasks(). I verified the CLI output included tasks from both pets and stayed within the 45-minute limit.

I also ran the task completion and task addition tests, and both passed. Recurrence was added later through `Pet.complete_task()`, so frequency is now more than stored information.

I did not accept AI’s suggested helper-method refactor because the existing conflict detection was short and readable. I kept the implementation already verified by nine conflict tests.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The tests cover sorting, filtering, multi-pet scheduling, time-budget boundaries (exact fit, oversized tasks skipped while smaller ones still fit, zero time), recurrence, conflict detection, and input validation. These are the behaviors the plan depends on, and the edge cases are where scheduling code is most likely to break.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

The latest `python -m pytest` run passed all 58 tests. The CLI demo showed multi-pet scheduling working end to end, and the automated tests verified the core behaviors and edge cases. I rate my confidence 4 out of 5. The remaining gaps are that conflict detection does not look at overlapping durations, and the Streamlit UI has no automated tests. Next I would test overlapping tasks with different start times and the UI flows.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied that the core backend behaviors are covered by automated tests and that the CLI demo and the Streamlit UI both run on the same four classes.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add overlapping-duration conflict detection and persistent storage, since data currently lasts only for the Streamlit session.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

As lead architect, I needed to review AI suggestions, control scope, and verify behavior myself. AI sped up the UML, code, tests, and documentation, but I decided what to keep, such as rejecting the conflict-detection refactor, and confirmed it with tests and the CLI output.
