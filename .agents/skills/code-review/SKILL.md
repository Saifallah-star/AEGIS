
---
name: code-review
description: Review code diffs for correctness, security vulnerabilities, regressions, error handling, and missing tests. Use when reviewing a proposed implementation or preparing changes for a commit.
---

# Code Review Skill

## Review Process

1. Establish the intended behavior from the task and relevant documentation.
2. Inspect the diff before reading unrelated files.
3. Trace modified code through its callers and dependencies.
4. Inspect tests covering the modified behavior.
5. Check failure paths and important boundary conditions.
6. Report only actionable findings supported by code evidence.

## General Checks

### Correctness
- Does the implementation meet the acceptance criteria?
- Are conditions, loops, state transitions, and return values correct?
- Are boundary cases handled?

### Error Handling
- Are failures handled consistently?
- Can errors be silently swallowed?
- Are resources cleaned up when operations fail?

### Security
- Is untrusted input validated?
- Are secrets or sensitive data exposed?
- Are filesystem paths, subprocesses, URLs, and external inputs handled safely?

### Maintainability
- Does the change follow established project patterns?
- Is complexity unnecessarily increased?
- Are duplicated abstractions or unnecessary dependencies introduced?

### Testing
- Are important success and failure paths covered?
- Are existing tests still applicable?
- Do tests assert meaningful behavior instead of merely executing code?

## Finding Quality

A valid finding should explain:
1. What is wrong.
2. Where it occurs.
3. Under what conditions it causes a problem.
4. Why the problem matters.
5. How to fix it.

Do not reportirst. Your skill currently lives at: personal preferences as bugs.
Do not speculate beyond the available evidence.
Do not claim a test passed unless it was executed and its result observed.

## Context Efficiency

- Inspect the diff first.
- Read only relevant code and tests.
- Do not dump full files or entire logs.
- Avoid repeating findings.
- Keep the final report concise and severity-ordered.
