---
name: human-readable-cli
description: Rules for readable, low-friction developer-facing CLI output. Use when improving human-facing command output without weakening machine-readable contracts.
---

# Human Readable CLI Skill

## Goals

- reduce cognitive load
- make governance outputs usable in daily work
- preserve signal without overwhelming the user

## Output Rules

- surface the most important message first
- group related warnings
- make next steps explicit
- avoid dumping raw internal detail unless requested
- keep wording concrete and actionable

## Warning Rules

When warning the user:

- distinguish hard-stop from advisory
- explain why the warning matters
- show how to resolve it
- avoid generic wording

## Preview Rules

Suggested packs or actions should be presented as:

- relevant
- minimal
- easy to understand
- easy to accept or ignore
