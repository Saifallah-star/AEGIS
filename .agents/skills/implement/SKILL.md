---
name: implement
description: >-
  Build out work based on a spec or tickets by driving TDD at pre-agreed seams and closing with code review. Use when the user requests implementation of a planned task or ticket, or invokes /implement.
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

consult and apply the `tdd` skill (`.agents/skills/tdd/SKILL.md`) where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, consult and apply the `code-review` skill (`.agents/skills/code-review/SKILL.md`) to review the work.

Commit your work to the current branch.
