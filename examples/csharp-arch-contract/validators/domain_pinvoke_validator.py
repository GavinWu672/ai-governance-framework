#!/usr/bin/env python3
"""
Advisory validator for ARCH_DOMAIN_PINVOKE.

Detects P/Invoke declarations ([DllImport], [LibraryImport], extern static)
inside files that reside under domain_roots.  Infrastructure and test paths
are explicitly excluded to avoid false positives.

Enforcement: advisory (blocks on promotion after min_evaluations + FP=0).
"""

import re
from governance_tools.validator_interface import DomainValidator, ValidatorResult

# Patterns that indicate a native-interop declaration in C#.
_PINVOKE_PATTERNS = [
    re.compile(r"\[DllImport\s*\("),
    re.compile(r"\[LibraryImport\s*\("),
    re.compile(r"\bextern\s+static\b"),
]

# Single-line comment prefix — strip before pattern matching to avoid FP
# from documentation examples embedded in XML doc comments.
_COMMENT_LINE = re.compile(r"^\s*//")


def _is_comment_line(line: str) -> bool:
    return bool(_COMMENT_LINE.match(line))


def _strip_block_comments(source: str) -> str:
    """Remove /* ... */ block comments to reduce FP from doc blocks."""
    return re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)


def _matching_patterns(source: str) -> list[str]:
    """Return human-readable labels for every P/Invoke pattern found."""
    clean = _strip_block_comments(source)
    lines = clean.splitlines()
    found: list[str] = []
    for pattern in _PINVOKE_PATTERNS:
        for line in lines:
            if not _is_comment_line(line) and pattern.search(line):
                found.append(pattern.pattern)
                break  # one hit per pattern is enough
    return found


class DomainPinvokeValidator(DomainValidator):
    """
    ARCH_DOMAIN_PINVOKE — advisory.

    Raises a violation when a file whose path starts with a domain_root
    contains a P/Invoke declaration.

    Payload keys consumed:
      - file_path     (str)  : path of the file being reviewed
      - source_code   (str)  : full source text of that file
      - domain_roots  (list) : list of path prefixes from contract.yaml
                               (optional; falls back to contract defaults)
    """

    # Contract defaults — used when payload omits domain_roots.
    _DEFAULT_DOMAIN_ROOTS = ["src/HP.OCI.Core/"]

    @property
    def rule_ids(self) -> list[str]:
        return ["ARCH_DOMAIN_PINVOKE"]

    def validate(self, payload: dict) -> ValidatorResult:
        file_path: str = payload.get("file_path", "")
        source_code: str = payload.get("source_code", "")
        domain_roots: list[str] = payload.get(
            "domain_roots", self._DEFAULT_DOMAIN_ROOTS
        )

        # Normalise path separators so Windows paths match contract roots.
        normalised = file_path.replace("\\", "/")

        in_domain = any(normalised.startswith(root) for root in domain_roots)

        if not in_domain:
            return ValidatorResult(
                ok=True,
                rule_ids=self.rule_ids,
                evidence_summary=(
                    f"File '{file_path}' is outside domain_roots — skip."
                ),
                metadata={"mode": "advisory", "in_domain": False},
            )

        matched = _matching_patterns(source_code)

        if not matched:
            return ValidatorResult(
                ok=True,
                rule_ids=self.rule_ids,
                evidence_summary=(
                    f"No P/Invoke patterns found in domain file '{file_path}'."
                ),
                metadata={"mode": "advisory", "in_domain": True},
            )

        violations = [
            f"ARCH_DOMAIN_PINVOKE: '{pat}' found in domain file '{file_path}'"
            for pat in matched
        ]
        return ValidatorResult(
            ok=False,
            rule_ids=self.rule_ids,
            violations=violations,
            evidence_summary=(
                f"P/Invoke pattern(s) detected in domain file '{file_path}': "
                + ", ".join(matched)
            ),
            metadata={"mode": "advisory", "in_domain": True, "matched": matched},
        )
