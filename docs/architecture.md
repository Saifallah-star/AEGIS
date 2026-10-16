# Agentic Skills & Subagents Architecture

This document describes the architectural model of the skills and autonomous subagents system hosted in this repository for **Google Antigravity (`agy`) / Gemini CLI**.

---

## 1. System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                       Developer / User                      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Prompts / Slash Commands
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Primary Agent (Antigravity / agy)             │
│   • Top-level Context (Catalog of Skill Names & Summaries)  │
│   • Steering Rules (AGENTS.md / GEMINI.md)                  │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼ Progressive Disclosure       ▼ Autonomous Dispatch
┌──────────────────────────────┐ ┌────────────────────────────┐
│      .agents/skills/         │ │     Specialized Subagents  │
│ • 20 Engineering Skills      │ │ • researcher (read-only)   │
│ • 7 Productivity Skills      │ │ • implementer (TDD/build)  │
│ • Supporting docs & scripts  │ │ • reviewer (2-axis audit)  │
└──────────────────────────────┘ └────────────────────────────┘
```

---

## 2. Progressive Disclosure

In Antigravity, skills are designed to minimize context token usage:
- **Index Injection**: When an agent session starts, Antigravity parses the YAML frontmatter (`name` and `description`) of all skills under `.agents/skills/<name>/SKILL.md`.
- **On-Demand Activation**: The agent only reads the full text of `SKILL.md` (and its supporting docs like `mocking.md` or `DEEPENING.md`) when explicitly activated by a user command or when a task matches the skill's trigger description.
- **Reference Compartmentalization**: Bulky documentation, checklists, and templates are stored as co-located files within the skill directory and reached via context pointers.

---

## 3. Subagent Orchestration Patterns

Antigravity supports spawning autonomous subagents using the `invoke_subagent` tool:
- **`researcher`**: Used before implementation to investigate code, search documentation, and explore third-party APIs without modifying files.
- **`implementer`**: Used to build specific tickets within an integration branch or worktree, executing the Red-Green-Refactor loop (`tdd`).
- **`reviewer`**: Runs in parallel to review diffs along two orthogonal axes:
  - *Standards Axis*: Adherence to repository patterns, cleanliness, and code smell avoidance.
  - *Spec Axis*: Verification that acceptance criteria and edge cases are satisfied.

---

## 4. Skills Taxonomy

The repository categorizes skills into two primary domains:

1. **Engineering Skills**:
   - High-rigor development workflows: Triage (`triage`), Requirements Grilling (`grill-with-docs`), System Design (`codebase-design`), Specification (`to-spec`), Ticket DAG (`to-tickets`), Concurrent Execution (`implement-spec`), Test-Driven Development (`tdd`), Two-Axis Review (`code-review`), Bug Diagnosis (`diagnosing-bugs`), and PR Formatting (`pr`).

2. **Productivity Skills**:
   - Universal collaboration and communication: General Grilling (`grill-me`), Cross-Session Handoff (`handoff`), Interactive Tutoring (`teach`), External Questionnaires (`to-questionnaire`), Clarification Circuit-Breaker (`wait-what`), and Agent-Facing Documentation (`writing-for-agents`).

For detailed usage, diagrams, and end-to-end examples, see [`illustration.md`](../illustration.md).
