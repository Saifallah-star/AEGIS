# Skills & Agents Development Backlog

This backlog tracks the ongoing development, curation, optimization, and testing of agent skills, subagent configurations, and engineering workflows for **Google Antigravity (`agy`) / Gemini CLI**.

---

##  Active Initiatives

### 1. Skill Quality & Verification Tooling
- [x] Implement an automated validator script (`scripts/validate_skills.py`) to verify:
  - Correct YAML frontmatter formatting (`name`, `description`).
  - Absence of hardcoded tool syntax or deprecated vendor flags.
  - Valid internal markdown links (`[reference.md](reference.md)`).
- [x] Add pre-commit check to ensure skills conform to the Antigravity customization specification.
- [x] Measure token weight of skill descriptions to optimize context overhead.

### 2. Subagent Orchestration & Custom Agents
- [ ] Define standardized agent personas and configurations for Antigravity's `define_subagent` tool:
  - `planner`: Specialized in high-level architectural decomposition.
  - `implementer`: Code modification, targeted testing, and seam implementation.
  - `researcher`: Read-only discovery and citation synthesis.
  - `reviewer`: Strict two-axis code reviewer.
- [ ] Document subagent communication patterns and state passing via context pointers.

### 3. New Skill Proposals
- [ ] **`db-migration`**: Safe database schema migrations, rollback scripts, and seed testing.
- [ ] **`security-audit`**: Pre-merge static analysis, dependency vulnerability scans, and secret leak detection.
- [ ] **`api-contract`**: OpenAPI/Protobuf schema design with consumer-driven contract testing.
- [ ] **`release-notes`**: Automated changelog and release notes generation from PR bodies.

### 4. Continuous Refinement of Existing Skills
- [x] Port and optimize 27 core skills from `mattpocock/skills`.
- [x] Remove vendor-specific artifacts (OpenAI configs and Claude-specific hooks).
- [x] Adapt inter-skill references to Antigravity file conventions.
- [x] Author comprehensive illustrations and workflow guides in `illustration.md`.
- [ ] Test `/diagnosing-bugs` across Python and TypeScript projects to calibrate the 6-phase loop.
- [ ] Benchmark `/implement-spec` concurrency with multiple subagents on real task graphs.

---

##  Ideas & Explorations

- Experiment with MCP (Model Context Protocol) tool integration within custom skills.
- Build an interactive CLI wizard for creating new Antigravity skills following `writing-for-agents` principles.
- Benchmark skill activation accuracy across various Gemini model tiers (`flash`, `flash_lite`, `pro`).
