---
name: code-style
description: Common code quality and change discipline rules. Use for general implementation work when the agent needs shared guidance on keeping diffs small, reviewable, explicit, and in scope.
---

# Code Style Skill

Apply these rules across all languages unless a more specific skill overrides them.

## Core Rules

- prefer small, reviewable diffs
- preserve existing naming conventions unless there is a strong reason to change them
- avoid unnecessary abstractions
- avoid large functions when smaller focused functions improve clarity
- prefer explicitness over magic
- preserve local readability

## Change Discipline

- do not rewrite unrelated code
- do not clean up outside the task scope
- do not mix refactor and behavior change unless necessary
- do not introduce hidden coupling

## Reviewability

Changes should allow a reviewer to answer:

- what changed
- why it changed
- what risk it introduces
- what evidence supports it
