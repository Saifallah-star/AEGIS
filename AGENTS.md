
# Project Instructions

## General Rules
- Read relevant source files before changing code.
- Follow the existing architecture and conventions.
- Make the smallest coherent change that satisfies the task.
- Preserve unrelated user changes.
- Run targeted tests and inspect the final diff.
- Never claim unverified test results.

## Delegation
- Use `triage-agent` for evaluating issues/PRs, reproduction, and writing agent briefs.
- Use `architect` for requirements grilling, ADRs, system specs, and ticket DAG decomposition.
- Use `researcher` for substantial read-only exploration and documentation lookup.
- Use `implementer` for clearly scoped code changes and test-driven development (`tdd`).
- Use `debugger` for isolating hard/flaky bugs, hypothesis testing, and regression proofs.
- Use `reviewer` for independent two-axis review (Standards + Spec) of diffs.
- Keep trivial tasks in the primary agent.
- Parallelize only independent work with clear file ownership.
- Avoid duplicate investigations and redundant agent reports.

## Context Efficiency
- Read only relevant files.
- Request concise reports with file paths and evidence.
- Do not paste full files or large logs into the main conversation.
- Persist important decisions and current progress when useful.
- Verify delegated changes before integrating them.
