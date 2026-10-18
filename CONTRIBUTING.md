# Contributing to Agentic-Driven Development

Thank you for contributing to the **Agentic-Driven Development** repository! This project serves as a central hub, testing ground, and backlog for **AI Agent Skills, Autonomous Subagents, and Disciplined Engineering Workflows** designed for **Google Antigravity (`agy`) and the Gemini CLI**.

---

##  Guiding Principles

1. **Progressive Disclosure**: Skills must be lightweight at index time (`name` and `description` in YAML frontmatter), revealing deeper checklists, schemas, and templates only upon activation.
2. **Deep Modules with Narrow Seams**: Whether developing code, skills, or agent definitions, encapsulate internal complexity behind simple, robust interfaces (`codebase-design`).
3. **Disciplined Lifecycle Boundaries**: Development flows systematically through distinct phases:
   `Triage / Alignment` ➔ `Specification & Ticket DAG` ➔ `TDD Construction` ➔ `Two-Axis Code Review` ➔ `PR & Retro`.
4. **Honest, Reproducible Verification**: Never claim unverified test results or speculative bug fixes. Every fix must be proven with automated tests or reproduction runs.

---

##  Contribution Areas

### 1. Adding or Refining a Skill (`.agents/skills/<skill-name>/`)
- Every skill directory must contain a valid `SKILL.md` with:
  ```yaml
  ---
  name: <skill-name>
  description: >-
    Action-oriented 3rd-person description of what the skill does and when to activate it.
  ---
  ```
- Store detailed guides, templates, or scripts in co-located files within the skill directory (e.g. `mocking.md`, `tests.md`, `scripts/`).
- Document newly added skills in both [`README.md`](README.md) and [`illustration.md`](illustration.md).

### 2. Enhancing Subagent Definitions (`.agents/agents/<agent-name>/`)
- Subagents live in `.agents/agents/<name>/agent.md` with proper YAML frontmatter (`name`, `description`, `tools`, `subagent: true`, `model`, `skills`).
- Each agent must specify:
  - **Role & When to Use**: Concrete boundaries preventing duplicate investigations or tool misuse.
  - **Lifecycle / ASCII Flow**: Step-by-step procedure the subagent follows.
  - **Explicit Boundaries**: What the subagent is strictly prohibited from doing.
  - **Required Output Schema**: Standardized handoff format.

### 3. Specifications & Task Backlog (`specs/` & `tasks/`)
- Complex features or skills should start with a specification in `specs/features/` using [`FEATURE_TEMPLATE.md`](specs/features/FEATURE_TEMPLATE.md).
- Track upcoming proposals and skill audits in [`tasks/backlog.md`](tasks/backlog.md).

---

##  Agentic Development Workflow

When contributing changes, follow the repository's native multi-agent workflow:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Contribution Lifecycle                          │
└────┬────────────┬─────────────┬─────────────┬────────────┬─────────────┘
     │            │             │             │            │             │
     ▼            ▼             ▼             ▼            ▼             ▼
[triage-agent] [architect]  [researcher] [implementer]  [debugger]   [reviewer]
Intake & Repro  Grill & DAG   Grounding    TDD Build    Hypothesis   2-Axis Gate
```

1. **Intake & Triage**: Use `triage-agent` or run `/triage` to reproduce reported bugs and write structured agent briefs (`AGENT-BRIEF.md`).
2. **Alignment & Specs**: For non-trivial ideas, use `architect` with `/grill-with-docs` to eliminate unspoken assumptions, document ADRs, and produce tracer-bullet ticket DAGs (`to-tickets`).
3. **Research**: Delegate substantial discovery and external API verification to `researcher` (`skills/research`) before modifying code.
4. **Implementation**: Use `implementer` following strict Test-Driven Development (`tdd`): write the failing test first (Red), implement minimal logic (Green), and refactor across deep seams.
5. **Debugging**: For tricky regressions or intermittent failures, use `debugger` (`diagnosing-bugs`) to isolate the root cause and verify stability with 50+ stress runs.
6. **Review**: Submit diffs to `reviewer` for an independent two-axis review (**Standards** + **Spec**) to obtain an explicit `[APPROVE]` gate verdict before merging.

---

## 🧪 Automated Quality Validation & Git Hooks

To make contributing effortless, quality verification is automated:

### 1. Automatic Verification on `git commit`
Whenever you run `git commit`, the pre-commit hook automatically pauses execution for 1–2 seconds to run `python3 scripts/validate_skills.py`.
- **If checks pass**: Your commit is saved.
- **If an error or broken link occurs**: The commit is halted, and a short remediation guide tells you exactly which file needs attention and how to fix it.
- **Note**: The hook does **not** run in the background on a timer; it only triggers at commit time.

### 2. Manual Commands & Tests
You can run validation and unit tests anytime during development:

```bash
# Validate all skills and subagents with colored report
python3 scripts/validate_skills.py

# Run unit tests verifying the validator tool
python3 -m unittest discover -s tests -v

# Ensure git hook is active
./scripts/install_hooks.sh
```

---

## 📋 Definition of Done (DoD)

A contribution is ready to be merged when:
- [ ] Acceptance criteria in the ticket or specification are fully met.
- [ ] Frontmatter in skills or agents adheres to the Antigravity specification (`python3 scripts/validate_skills.py` passes).
- [ ] Unit tests pass cleanly (`python3 -m unittest discover -s tests -v`).
- [ ] `AGENTS.md`, `README.md`, and `illustration.md` are updated if new skills or agents were introduced.
- [ ] The git diff has been reviewed with 0 unaddressed `Critical` or `High` findings.
- [ ] PR description follows the structured format generated by `/pr` (Mermaid visuals, proof, and blast radius).

