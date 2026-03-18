# C# Architecture Rules

## ARCH_DOMAIN_PINVOKE

- Domain layer must not contain P/Invoke declarations.
  Direct interop (`[DllImport]`, `[LibraryImport]`, `extern static`) belongs
  in the infrastructure layer or a dedicated native wrapper assembly.
- Evidence required:
  - pinvoke_review
- Enforcement:
  - advisory (current)
  - promote to hard_stop when: evaluations >= 20, false_positive_rate == 0.0

## ARCH_DOMAIN_OS_AWARENESS

- Domain layer must not contain OS detection or platform branching.
  `RuntimeInformation`, `OperatingSystem.Is*`, and `Environment.OSVersion`
  belong in infrastructure adapters, not domain services.
- Evidence required:
  - os_awareness_review
- Enforcement:
  - advisory (planned — not yet implemented)
