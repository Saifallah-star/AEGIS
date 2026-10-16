# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Two primary patterns for agent discovery and activation:

- A **model-invoked** skill provides a description explicitly indicating when the agent should proactively consult and follow it during autonomous tasks (e.g., during code implementation, debugging, or code review). The description is the skill's top-level context pointer loaded into the agent's available skills catalog, enabling progressive disclosure.
- A **user-invoked** skill specifies in its description that it triggers when explicitly requested by the user or through a specific slash command (e.g. `Use when the user invokes /grill-me...`). This keeps the skill targeted and prevents unexpected unsolicited execution while remaining discoverable.

In Antigravity (`agy`), every skill uses clean YAML frontmatter with `name` and `description` under `.agents/skills/<skill-name>/SKILL.md`. Progressive disclosure ensures only skill names and descriptions are in the top-level prompt context until the skill is actually read.

Shared reference that two user-invoked skills both need can live in neither: with no descriptions, neither can fire the other. Push it to a plain file outside the skill system: external reference any skill can point at.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human has one skill to remember instead of many. It can only hint, never fire them: user-invoked skills have no description, so nothing but the human can reach them.
