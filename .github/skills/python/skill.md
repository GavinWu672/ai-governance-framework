---
name: python
description: Python implementation standards for validators, runtime hooks, scripts, ingestors, and tests. Use when editing Python code in this repository.
---

# Python Skill

## Coding Rules

- prefer straightforward Python
- use type hints where practical
- keep side effects visible
- avoid overusing metaprogramming
- prefer standard library unless a dependency is justified

## Testing Rules

- add or update tests when behavior changes
- keep fixtures minimal and readable
- avoid brittle tests tied to irrelevant formatting
- verify edge cases when changing validators or parsers

## CLI And Tooling Rules

- keep exit codes intentional
- separate machine-readable and human-readable output
- preserve backwards compatibility where possible
- document breaking changes explicitly
