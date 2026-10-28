---
name: to-spec
description: >-
  Synthesize current conversation context and codebase understanding into an actionable specification published to the issue tracker. Use when the user invokes /to-spec or asks to create a formal spec from discussion.
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

1. **Explore the repo**: Understand the current state of the codebase. Use the project's domain glossary (`GLOSSARY.md`) vocabulary throughout the spec, and respect any ADRs (`docs/adr/`) in the area you're touching.

2. **Identify test seams**: Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. The fewer seams across the codebase, the better - the ideal number is one. Confirm with the user that these seams match their expectations.

3. **Draft the specification**: Write the complete draft spec using the template below. Save it to `docs/designs/<feature-slug>.md` (or `.scratch/<feature-slug>/spec.md`).

4. **The Goldfish Review Gate (`/egm-review`)**:
   Do **not** rely on casual conversational sign-off. Models that draft a spec develop confirmation bias. Stress-test the draft cold:
   - Spawn a zero-context subagent (or invoke `/egm-review`) with zero conversation history to audit the saved spec file.
   - The Goldfish performs:
     - **Comprehension Test**: Paraphrases the system architecture back to verify the spec is 100% self-contained and clear without external context.
     - **Adversarial Critique & Implementation Readiness**: Probes for unstated assumptions, logical contradictions, incomplete data models, missing error handling, and vague completion criteria.
   - **Triage Feedback Taxonomy (`/egm-resolve`)**:
     Categorize every finding strictly using EGM's structured taxonomy:
     - `PROPOSE FIX`: Propose concrete spec modifications and apply approved edits directly to the spec.
     - `CONTEST`: Reject a finding only when citing verified code evidence or existing ADR invariants.
     - `ESCALATE`: Flag genuine architectural forks or business trade-offs to the human.
     - `DECLINE`: Reject out-of-scope nits with explicit justification.

5. **Publish to Issue Tracker**:
   Once the spec passes the Goldfish gate (all blockers and majors resolved), publish the verified spec to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage. Proceed to `/to-tickets`.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
