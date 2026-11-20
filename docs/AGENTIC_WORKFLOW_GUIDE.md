# The 10-Step Agentic Engineering Workflow

A plain-English guide for teammates on how our skills and autonomous agents collaborate to take a feature or bug from an initial idea to production-ready code without chaos or guesswork.

---

## The Big Picture (Lifecycle Flow)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        The End-to-End Pipeline                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
       1. /triage ────────► Intake & Verification (Is it real & in-scope?)
                                    │
                                    ▼
       2. /grill-with-docs ─► Design Interview & Edge-Case Stress Test
                                    │
                                    ▼
       3. Domain Docs ────► Update GLOSSARY.md & ADRs inline
                                    │
                                    ▼
       4. /to-spec ───────► Draft the formal blueprint
                                    │
                                    ▼
       5. Goldfish Loop ──► /egm-review + /egm-resolve (Cold Audit)
                                    │
                                    ▼
       6. /to-tickets ────► Break spec into an ordered dependency DAG
                                    │
                                    ▼
       7. /implement-spec ─► Dispatch `implementer` subagents
                                    │
                                    ▼
       8. /tdd ───────────► Red-Green-Refactor at high-level seams
                                    │
                                    ▼
       9. /code-review ───► Two-Axis Audit (Standards + Spec Drift)
                                    │
                                    ▼
      10. /pr & /retro ───► Clean PR, Evidence, & Team Learnings
```

---

## Step 1: Intake & Triage (`/triage` & `triage-agent`)

* **What it does:** The gatekeeper. Whenever a user files an issue, feature request, or external PR, run `/triage`.
* **How it works:**
  - Checks if the feature is **already built**.
  - Checks if it was **previously rejected** (`.out-of-scope/`).
  - For bugs: attempts to **reproduce the issue** in an isolated sandbox.
* **Golden Rule:** **Triage NEVER writes code.** It only classifies (`needs-info`, `ready-for-agent`, `wontfix`) and writes an `AGENT-BRIEF.md`.

---

## Step 2: Grilling the Idea (`/grill-with-docs`) 
#### `grilling` + `domain-modeling`.

* **What it does:** A relentless question-and-answer session to eliminate silent assumptions.
* **How it works:**
  - Treats design choices as a **Design Tree** with "frontiers" (questions whose prerequisites are settled).
  - Presents questions in rounds with recommended answers. You just reply `"yes"` or specify your preference.
  - Zero flattery ("anti-glazing") and architectural neutrality on major trade-offs.

## Step 3: Domain Modeling & ADRs (`GLOSSARY.md` + `docs/adr/`)

* **What it does:** Captures the decisions from Step 2 directly onto disk.
* **How it works:**
  - **`GLOSSARY.md`:** Eliminates fuzzy words (e.g., clarifies whether "account" means the *billing organization* or the *login user*).
  - **`docs/adr/000X-*.md`:** Writes Architectural Decision Records only when choices are hard to reverse, surprising, or involve major trade-offs.

  # Why it writes inline instead of a report at the end
  
  The rule in domain-modeling explicitly says:
  
  │ "Don't batch these up: capture them as they happen."
  
  1. GLOSSARY.md is updated immediately:
  The moment you resolve what an ambiguous term means (e.g., distinguishing a Workspace from a Repository), it updates GLOSSARY.md right then. Subsequent questions in   
  the interview immediately use the new, precise term.
  2. ADRs are committed immediately:
  When you settle a hard-to-reverse architectural decision (e.g., choosing SQLite over Postgres for local cache), it creates docs/adr/0001-local-cache.md immediately    
  with the exact trade-offs and rationale.


---

## Step 4: Synthesizing the Blueprint (`/to-spec`)

* **What it does:** Takes all previous decisions and turns them into a formal specification (`docs/designs/<feature>.md`).
* **How it works:**
  - **Does not interview you.** It synthesizes what has already been decided.
  - Locates the highest-level **test seam** (testing external observable behavior rather than brittle internal functions).
  - Writes problem statements, exhaustive user stories, architecture contracts, and out-of-scope boundaries.

---
## ==🟡triggered automatic after `/to-spec`  and loops until the spec is 100% accurate==
## Step 5: The Elephant-Goldfish Review Gate (`/egm-review` & `/egm-resolve`)

* **What it does:** Eliminates author blind-spots so downstream coding agents don't get stuck.
* **The Mechanism:**

```
                  ┌────────────────────────────────────────┐
                  │        Draft Spec in Step 4            │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │  /egm-review (GOLDFISH: Zero-Context Subagents)  │
             │  • Reviews document cold with no chat memory     │
             │  • Catches missing prerequisites & ambiguities   │
             └────────────────────────┬─────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │  /egm-resolve (ELEPHANT: Persistent Coordinator) │ 
             │  • PROPOSE FIX: Auto-patches the spec file       │
             │  • CONTEST: Defends choices with code citations  │
             │  • ESCALATE: Asks human only on real forks       │
             └────────────────────────┬─────────────────────────┘
                                      │ (Loops until all Blockers  <-- IMP
                                      │  & Majors are resolved)
                                      ▼
                       100% Bulletproof Specification!
```

---

## Step 6: Ticket Decomposition (`/to-tickets`)

* **What it does:** Breaks the approved specification into atomic, bite-sized tasks.
* **How it works:**
  - Builds an explicit **dependency graph (DAG)**. (Task B knows it cannot start until Task A finishes).
  - Keeps tickets scoped like "tracer bullets" (thin end-to-end slices rather than horizontal layers).
  - Prevents multiple subagents from editing the same files at the same time.

---

## Step 7: Multi-Agent Dispatch (`/implement-spec`)

* **What it does:** Coordinates autonomous workers to execute the ticket graph.
* **How it works:**
  - Spawns isolated `implementer` subagents to work on unblocked tickets.
  - Monitors progress and merges work incrementally as tickets pass validation.

---
## ==🟡triggered automatic after `/implement-spec`==
## Step 8: Test-Driven Development (`/tdd`)

* **What it does:** The discipline every `implementer` must follow when writing code.
* **The Cycle:**
  1. **Red:** Write a failing test at the architectural seam that captures the user story.
  2. **Green:** Write the minimal production code needed to make the test pass.
  3. **Refactor:** Clean up duplication and enforce deep-module interfaces while keeping tests green.
* **Rule:** Never claim a test passed without running the command and showing real output.

---
## ==🟡triggered automatic after the agents finish implementation==
## Step 9: Two-Axis Code Review (`/code-review` & `reviewer`)

* **What it does:** An adversarial audit of the final pull request or branch diff before merging.
* **The Two Axes:**
  1. **Standards Axis:** Checks code quality, Fowler smells, test coverage, and repo conventions.
  2. **Spec Axis:** Compares the final code directly against the original specification from Step 4 to catch **Spec Drift** (features omitted or accidental scope creep).

---

## Step 10: PR Publishing & Session Retrospective (`/pr` & `/retro`)

* **What it does:** Ships the feature cleanly and improves the system for next time.
* **How it works:**
  - **`/pr`:** Generates a structured PR description with context, test verification evidence, and blast-radius analysis.
  - **`/retro`:** Reflects on what went wrong during the session and suggests improvements to project rules (`AGENTS.md`) or tooling.

---

## Quick Cheat-Sheet for the Team

| If you want to... | Use this Command / Agent |
| :--- | :--- |
| Check an issue or bug report without writing code | `/triage` or `triage-agent` |
| Brainstorm, resolve trade-offs, and update glossary | `/grill-with-docs` |
| Turn chat agreements into a concrete design document | `/to-spec` |
| Stress-test a design doc with a cold reviewer | `/egm-review` & `/egm-resolve` |
| Break a design doc into a ticket list | `/to-tickets` |
| Build tickets test-first | `/implement` or `/implement-spec` (uses `implementer`) |
| Isolate a flaky, complex bug | `debugger` (`/diagnosing-bugs`) |
| Review a PR or branch diff before merging | `/code-review` (uses `reviewer`) |
| Prepare a pull request summary | `/pr` |


