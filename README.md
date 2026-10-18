# Agentic-Driven Development: Skills & Agents Backlog

A dedicated hub and backlog repository for **AI Agent Skills, Subagent Orchestrations, and Autonomous Engineering Workflows** built for **Google Antigravity (`agy`) and Gemini CLI**.

This repository is maintained as a central catalog, testing ground, and development backlog for agent capabilities, reusable engineering runbooks, and domain-driven design workflows.

---

##  Repository Purpose

The primary objective of this repository is to curate, maintain, test, and document production-grade skills and steering guidelines for autonomous coding agents:

1. **Skills Catalog**: Hosts a verified collection of **27 modular Antigravity skills** in [`.agents/skills/`](.agents/skills/), covering everything from initial requirements grilling to automated TDD and two-axis code reviews.
2. **Agent Steering & Subagent Roster**: Establishes universal guidelines in [`AGENTS.md`](AGENTS.md) and provides **6 specialized subagents** (`triage-agent`, `architect`, `researcher`, `implementer`, `debugger`, `reviewer`) under [`.agents/agents/`](.agents/agents/).
3. **Skills & Agents Backlog**: Manages upcoming skills, improvements to existing runbooks, subagent profiles, and agent evaluations in [`tasks/backlog.md`](tasks/backlog.md).
4. **Execution Runbooks & Guides**: Provides detailed visual architecture, lifecycle flowcharts, and concrete end-to-end usage scenarios in [`illustration.md`](illustration.md).

---

##  Repository Structure

```
├── .agents/
│   ├── agents/           # 6 Autonomous Antigravity specialized subagents
│   │   ├── triage-agent/ # Issue/PR intake, bug repro & agent briefs
│   │   ├── architect/    # Grilling, ADRs, interface contracts & ticket DAGs
│   │   ├── researcher/   # Read-only exploration & cited documentation search
│   │   ├── implementer/  # Strict TDD construction & deep module refactoring
│   │   ├── debugger/     # 6-phase scientific hypothesis testing & bug isolation
│   │   └── reviewer/     # 2-axis independent review (Standards + Spec)
│   └── skills/           # 27 Antigravity engineering & productivity skills
│       ├── ask-matt/                       # Workflow router & navigator
│       ├── code-review/                    # 2-axis review (Standards + Spec)
│       ├── codebase-design/                # Deep module design & interface seams
│       ├── diagnosing-bugs/                # 6-phase hypothesis & instrumentation loop
│       ├── domain-modeling/                # Ubiquitous language, GLOSSARY.md & ADRs
│       ├── grill-me/                       # Decision tree interview (general)
│       ├── grill-with-docs/                # Grilling + inline ADR & glossary generation
│       ├── handoff/                        # Multi-session context serialization
│       ├── implement/                      # Single-ticket TDD implementation
│       ├── implement-spec/                 # Concurrent subagent DAG implementation
│       ├── improve-codebase-architecture/  # Deepening scan & HTML candidate report
│       ├── pr/                             # High-signal PR generator & blast-radius
│       ├── prototype/                      # Fast throwaway logic & UI exploration
│       ├── research/                       # Primary-source cited technical discovery
│       ├── retro/                          # Session retrospective for AGENTS.md & checks
│       ├── setup-matt-pocock-skills/       # Issue tracker & triage initialization
│       ├── tdd/                            # Red-Green-Refactor vertical slice loop
│       ├── teach/                          # Stateful tutoring & missions workspace
│       ├── to-questionnaire/               # Async decision interview for third parties
│       ├── to-spec/                        # Conversation-to-spec synthesizer
│       ├── to-tickets/                     # Spec-to-DAG tracer-bullet decomposition
│       ├── triage/                         # 5-state issue & PR triage engine
│       ├── wait-what/                      # Plain-English re-pitch of confusing concepts
│       ├── wayfinder/                      # Epic-scale fog-of-war decision navigation
│       ├── wizard/                         # Interactive bash wizard for manual steps
│       └── writing-for-agents/             # Style guide for AGENTS.md & skill authoring
├── docs/                 # Agentic architecture, security, and design patterns
├── tasks/                # Skills and agents backlog (`tasks/backlog.md`)
├── specs/                # Specifications for new skills and agent workflows
├── scripts/              # Validation, linting, and installation scripts
├── AGENTS.md             # Core steering instructions for AI agents
├── illustration.md       # Complete visual and operational guide to all skills & agents
└── README.md             # Repository purpose and documentation
```

---

##  Specialized Subagent Roster

| Subagent | Role | Bound Skills | When to Use |
| :--- | :--- | :--- | :--- |
| **`triage-agent`** | Pre-Flight & Triage | `triage` | Ingesting issues/PRs, reproducing bugs with scripts, and authoring `AGENT-BRIEF.md`. |
| **`architect`** | System Architecture | `grill-with-docs`, `codebase-design`, `to-spec`, `to-tickets` | Relentless grilling of requirements, registering ADRs/glossaries, and decomposing specs into ticket DAGs. |
| **`researcher`** | Read-Only Exploration | `research` | Tracing unfamiliar execution paths, investigating external APIs, and providing cited findings without editing code. |
| **`implementer`** | TDD Construction | `tdd`, `codebase-design` | Building specific tickets using the Red-Green-Refactor cycle across clean, deep module boundaries. |
| **`debugger`** | Root-Cause Analysis | `diagnosing-bugs` | Resolving flaky tests, race conditions, or hard defects via hypothesis isolation and 50-run stress tests. |
| **`reviewer`** | Two-Axis Gatekeeper | `code-review` | Evaluating diffs on Standards (cleanliness/smells) and Spec (contracts/edge cases) with clear gate verdicts. |

---

##  How to Use in Your Projects

All skills and agents adhere strictly to the **Antigravity Customization Specification**:
- Agents located under `.agents/agents/<name>/agent.md`
- Skills located under `.agents/skills/<name>/SKILL.md`
- Progressive disclosure friendly (only metadata loaded until activated)
- Antigravity subagent native with sandbox command execution policies

### Option A: Direct Copy into Any Project
Copy `.agents` into your target repository root:

```bash
mkdir -p /path/to/your/project/.agents
cp -r .agents/agents /path/to/your/project/.agents/
cp -r .agents/skills /path/to/your/project/.agents/
```

### Option B: Global Machine Installation
Install skills and agents globally into your Antigravity configuration directory:

```bash
mkdir -p ~/.gemini/antigravity-cli/skills ~/.gemini/antigravity-cli/agents
cp -r .agents/skills/* ~/.gemini/antigravity-cli/skills/
cp -r .agents/agents/* ~/.gemini/antigravity-cli/agents/
```

---

##  Core Skill Workflows

| Lifecycle Phase | Primary Agent / Subagent | Key Skills | Trigger / Command | What It Does |
| :--- | :--- | :--- | :--- | :--- |
| **Triage & Intake** | `triage-agent` | `triage` | `/triage` | Verifies reproducibility and moves issues into ready states |
| **Design & Grilling** | `architect` | `grill-with-docs`, `grill-me` | `/grill-with-docs`, `/grill-me` | Stress-tests requirements and generates `GLOSSARY.md` & ADRs |
| **Specification** | `architect` | `to-spec`, `codebase-design` | `/to-spec` | Synthesizes contracts into formal user stories and specs |
| **Decomposition** | `architect` | `to-tickets` | `/to-tickets` | Decomposes specs into a directed acyclic graph (DAG) of tickets |
| **Research** | `researcher` | `research` | Model-dispatched | Traces execution paths and reads official docs with citations |
| **Execution** | `implementer` | `implement-spec`, `implement`, `tdd` | `/implement-spec`, `/implement` | Red-Green-Refactor implementation across ticket DAG |
| **Bug Isolation** | `debugger` | `diagnosing-bugs` | `/diagnosing-bugs` | 6-phase hypothesis testing and 50-run stress verification |
| **Review & Quality** | `reviewer` | `code-review` | `/code-review` | Two-axis audit (Standards + Spec) with gate verdict |
| **Delivery & PR** | Primary / `implementer` | `pr` | `/pr` | Formats high-signal PR descriptions with proof & blast radius |
| **Retrospective** | Primary Agent | `retro`, `handoff` | `/retro`, `/handoff` | Audits agent friction and updates `AGENTS.md` rules |

For complete diagrams, sequence charts, and real-world scenarios, consult [`illustration.md`](illustration.md).

---

## 🧪 Skill Quality, Verification & Automated Checks

The repository includes automated quality tooling to ensure all skills and subagents stay healthy and conform to the Antigravity specification.

### Automatic Pre-Commit Hook
You don't need to remember to run checks manually. A Git pre-commit hook is installed in `.git/hooks/pre-commit`:
- **When it runs**: It runs automatically at the exact moment you type `git commit`. It does **not** run on a background timer.
- **What it does**: Git pauses your commit for 1–2 seconds to run `python3 scripts/validate_skills.py`:
  - **If all checks pass (0 errors)**: The commit proceeds normally.
  - **If an error is found**: Git aborts the commit, keeps your changes intact, and prints a clear guide explaining what failed and how to fix it.

### What the Validator Checks
The validation script (`scripts/validate_skills.py`) inspects:
1. **YAML Frontmatter**: Verifies `name`, `description`, `tools`, and `subagent: true`.
2. **Context Token Weight**: Calculates progressive disclosure token cost so skills don't bloat the AI's initial index context.
3. **Vendor Syntax Scan**: Flags deprecated syntax or vendor-specific XML tags (such as `<thinking>` tags).
4. **Dead Links**: Verifies that any local file referenced in markdown (like `[mocking.md](mocking.md)`) actually exists on disk.

### Running Tools & Tests Manually
You can run the checks and automated test suite manually anytime:

```bash
# Run the skill & agent quality validator
python3 scripts/validate_skills.py

# Run the automated unit test suite
python3 -m unittest discover -s tests -v

# Re-install git hooks on a fresh clone
./scripts/install_hooks.sh
```

---

##  Active Backlog

Check [`tasks/backlog.md`](tasks/backlog.md) for the active roadmap, including:
- Automated agent frontmatter and tool policy validation tooling
- Multi-agent orchestration test fixtures
- Specialized domain skills (database migrations, security scanning)
- Subagent performance and token efficiency benchmarks

