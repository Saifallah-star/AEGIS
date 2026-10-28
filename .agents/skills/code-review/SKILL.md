---
name: code-review
description: >-
  Two-axis adversarial code review: Standards (repo patterns & Fowler smells) and Spec (EGM Goldfish audit with AST drift detection). Persists structured reports under docs/reviews/. Use when reviewing a branch, PR, or proposed changes, or when invoked via /code-review.
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards and clean code heuristics?
- **Spec**: does the code faithfully implement the originating issue / spec without architectural drift, missing features, or ADR violations?

Both axes run as **parallel, zero-context sub-agents (Goldfish Protocol)** so they evaluate the diff cold without confirmation bias or conversational sycophancy. Findings are aggregated and persisted as an artifact under `docs/reviews/`.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Strict Review Invariants (EGM Protocol)

1. **Zero-Context Evaluation (Goldfish Isolation)**: Review sub-agents are spawned cold with only the relevant diff, spec, and standards. They hold no conversational memory of previous drafting or rationale to prevent confirmation bias.
2. **Artifact-First Delivery**: Full review findings are **never** dumped in bulk into the chat pane. Instead, they are compiled and saved directly into `docs/reviews/{YYYY-MM-DD}_{target}_review.md`. The chat pane receives only a concise executive summary and the file link.
3. **Anti-Sycophancy (Anti-Glazing)**:
   - Absolute ban on validating adjectives (*"brilliant"*, *"great"*, *"perfect"*, *"excellent"*, *"spot-on"*).
   - Absolute ban on conversational apologies (*"I apologize"*, *"I am sorry"*).
   - Factual, plain-English critique: lead with what is broken, divergent, or risky before noting what works.
4. **Severity Taxonomy**: Every finding must be classified as:
   - 🔴 `[BLOCKER]`: Hard spec violation, missing required capability, ADR invariant violation, or regression.
   - 🟡 `[MAJOR]`: Logic shortcut, incomplete data model, missing validation/edge case handling, or notable Fowler smell.
   - 🟢 `[NIT]`: Scope creep, minor naming or typing inconsistency, or subjective stylistic recommendation.

---

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside two parallel sub-agents.

### 2. Identify the spec and architecture sources

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in the tracker doc.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

Additionally, locate architectural constraints:
- Central domain glossary: `GLOSSARY.md` (if present).
- Architectural Decision Records: `docs/adr/*.md` (if present).
- High-level design documents: `docs/designs/*.md` (if present).

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Issue both sub-agent calls together, in the foreground, and aggregate the reports they return. Spawn each sub-agent in a fresh, isolated context (`invoke_subagent`).

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- Anti-sycophancy rules: no praise, no apologies, plain English.
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Classify findings as [MAJOR] or [NIT]. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt (Goldfish & AST Drift Audit)** should include:

- The diff command and commit list.
- The path or fetched contents of the spec, along with relevant ADRs (`docs/adr/`) or design docs.
- Anti-sycophancy rules: no praise, no apologies, plain English.
- The brief: "Perform an adversarial Goldfish audit and AST drift detection comparing the diff cold against the spec and architectural invariants. Specifically check for:
  1. **Missing Features**: logic or capabilities specified in the spec/ADRs but omitted in code.
  2. **Incomplete Models**: types, classes, structs, interfaces, or schemas missing fields or constraints specified in the design.
  3. **Logic Shortcuts**: hardcoded fallback values, magic values, or skipped edge cases where dynamic logic was required.
  4. **Architectural Divergence**: implementations violating ADR invariants, using unauthorized libraries/patterns, or bypassing declared module seams.
  5. **Scope Creep**: behavior present in the diff that was neither requested nor justified.
  Classify each finding strictly as [BLOCKER], [MAJOR], or [NIT]. Quote the exact spec/ADR requirement and the offending code hunk for every finding. Under 500 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate and Save to `docs/reviews/`

1. **Ensure Destination Directory Exists**:
   Check if `docs/reviews/` exists in the repository. If not, create it immediately:
   ```bash
   mkdir -p docs/reviews
   ```

2. **Generate Report File Name**:
   Derive the filename using the current date and the sanitized target branch or commit ref:
   `docs/reviews/{YYYY-MM-DD}_{target_ref}_review.md`
   (Example: `docs/reviews/2026-10-28_feature-auth_review.md`).

3. **Write the Report**:
   Write the full report into `docs/reviews/{YYYY-MM-DD}_{target_ref}_review.md` using your file writing tool. Format:

   ```markdown
   # Code Review Report: <target_ref>

   - **Date**: YYYY-MM-DD
   - **Base Ref**: <fixed-point>
   - **HEAD**: <HEAD-commit>
   - **Spec Source**: <path or issue reference>
   - **Status**: [PASSED / CHANGES REQUIRED]

   ## Executive Summary

   - **Standards Findings**: X total (Y Major, Z Nit)
   - **Spec Findings**: A total (B Blocker, C Major, D Nit)
   - **Worst Standards Finding**: <one-line summary or "None">
   - **Worst Spec Finding**: <one-line summary or "None">

   ---

   ## Standards Review

   <Verbatim Standards sub-agent findings>

   ---

   ## Spec Review (Goldfish & AST Drift Audit)

   <Verbatim Spec sub-agent findings with [BLOCKER], [MAJOR], [NIT]>

   ---

   ## Actionable Remediation Checklist

   - [ ] <Fix for Blocker 1>
   - [ ] <Fix for Major 1>
   ```

4. **Chat Pane Delivery**:
   Do **not** dump the entire report in the chat pane. Output a concise plain-text message:
   - Provide the clickable link to the generated report: `[Review Report](file:///path/to/docs/reviews/{file})`.
   - Include the executive summary table (counts per axis, worst issue per axis).
   - If `BLOCKER` or `MAJOR` issues exist, state: `Changes required before merge.` Otherwise: `Review passed.`

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
