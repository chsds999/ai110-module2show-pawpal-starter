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

No design changes were needed yet. AI reviewed the skeleton and suggested skipping completed tasks, enforcing the time limit, and clearing old plans when generating a new one. I will address these during implementation.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm classes, create UML, implement the backend, and draft a CLI demo and tests. Providing my existing skeleton and asking for matching code helped keep the design consistent.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I reviewed the AI-generated code against the assignment requirements, especially the requirement for the Scheduler to retrieve all pets' tasks through Owner.get_all_tasks(). I verified the CLI output included tasks from both pets and stayed within the 45-minute limit.

I also ran the task completion and task addition tests, and both passed. Automatic recurrence remains unimplemented; frequency is currently stored as task information.

I did not accept AI’s suggested helper-method refactor because the existing conflict detection was short and readable. I kept the implementation already verified by nine conflict tests.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
