# Agentic-Driven Development: Skills & Agents Backlog

A dedicated hub and backlog repository for **AI Agent Skills, Subagent Orchestrations, and Autonomous Engineering Workflows** built for **Google Antigravity (`agy`) and Gemini CLI**.

This repository is maintained as a central catalog, testing ground, and development backlog for agent capabilities, reusable engineering runbooks, and domain-driven design workflows.

---

##  Repository Purpose

The primary objective of this repository is to curate, maintain, test, and document production-grade skills and steering guidelines for autonomous coding agents:

1. **Skills Catalog**: Hosts a verified collection of **27 modular Antigravity skills** in [`.agents/skills/`](.agents/skills/), covering everything from initial requirements grilling to automated TDD and two-axis code reviews.
2. **Agent Steering & Standards**: Establishes universal instructions, context efficiency rules, and subagent delegation patterns in [`AGENTS.md`](AGENTS.md).
3. **Skills & Agents Backlog**: Manages upcoming skills, improvements to existing runbooks, subagent profiles, and agent evaluations in [`tasks/backlog.md`](tasks/backlog.md).
4. **Execution Runbooks & Guides**: Provides detailed visual architecture, lifecycle flowcharts, and concrete end-to-end usage scenarios in [`illustration.md`](illustration.md).

---

##  Repository Structure

```
├── .agents/
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
├── illustration.md       # Complete visual and operational guide to all skills
└── README.md             # Repository purpose and documentation
```

---

##  How to Use These Skills in Your Projects

All skills adhere strictly to the **Antigravity Customization Specification**:
- Located under `.agents/skills/<skill-name>/`
- Valid YAML frontmatter with `name` and descriptive 3rd-person `description`
- Progressive disclosure friendly (only name and description loaded until activated)
- Antigravity subagent native (`implementer`, `researcher`, `reviewer`)

### Option A: Direct Copy into Any Project
Copy the desired skill or the entire `.agents/skills/` folder into your target workspace:

```bash
mkdir -p /path/to/your/project/.agents
cp -r .agents/skills /path/to/your/project/.agents/
```

### Option B: Global Machine Installation
Install skills globally into your Antigravity configuration directory:

```bash
mkdir -p ~/.gemini/antigravity-cli/skills
cp -r .agents/skills/* ~/.gemini/antigravity-cli/skills/
```

---

##  Core Skill Workflows

| Lifecycle Phase | Skills | Trigger / Command | What It Does |
| :--- | :--- | :--- | :--- |
| **Router & Navigator** | `ask-matt` | `/ask-matt` | Guides you to the right skill for your specific task |
| **Alignment & Grilling** | `grill-with-docs`, `grill-me` | `/grill-with-docs` | Relentlessly stress-tests ideas and builds `GLOSSARY.md` & ADRs |
| **Specification** | `to-spec` | `/to-spec` | Synthesizes discussion into formal user stories and contracts |
| **Decomposition** | `to-tickets` | `/to-tickets` | Decomposes specs into a directed acyclic graph (DAG) of tickets |
| **Execution** | `implement-spec`, `implement` | `/implement-spec` | Coordinates subagents to implement ticket DAGs concurrently |
| **Quality & TDD** | `tdd`, `codebase-design` | Auto / `/tdd` | Strict Red-Green-Refactor loop & deep module seam enforcement |
| **Review & PR** | `code-review`, `pr` | `/code-review`, `/pr` | Two-axis review (Standards + Spec) and production PR formatting |
| **Debugging** | `diagnosing-bugs` | `/diagnosing-bugs` | 6-phase disciplined diagnosis and regression testing |
| **Continuity** | `handoff`, `retro` | `/handoff`, `/retro` | Serializes session context or audits agent performance |

For complete diagrams, sequence charts, and real-world scenarios, consult [`illustration.md`](illustration.md).

---

##  Active Backlog

Check [`tasks/backlog.md`](tasks/backlog.md) for the active roadmap, including:
- Automated skill verification & frontmatter validation tooling
- Domain-specific skills (DevOps, database migrations, security audits)
- Subagent role definitions and custom system prompts
- Multi-model evaluation and reliability benchmarks
