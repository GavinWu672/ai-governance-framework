import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_tools.test_result_ingestor import (
    ingest_junit_xml,
    ingest_pytest_text,
)


def test_ingest_pytest_text_success_summary():
    payload = ingest_pytest_text(
        """
============================= test session starts =============================
collected 3 items

tests/test_demo.py ...                                                  [100%]

============================== 3 passed in 0.12s ==============================
""".strip()
    )
    assert payload["ok"] is True
    assert payload["summary"]["passed"] == 3
    assert payload["summary"]["failed"] == 0


def test_ingest_pytest_text_failures_and_warnings():
    payload = ingest_pytest_text(
        """
FAILED tests/test_demo.py::test_refactor_guard - AssertionError: behavior changed
warning: something noisy
PytestCacheWarning: cache write skipped
========================= 1 failed, 2 passed in 0.50s =========================
""".strip()
    )
    assert payload["ok"] is False
    assert payload["summary"]["failed"] == 1
    assert any("FAILED tests/test_demo.py::test_refactor_guard" in e for e in payload["errors"])
    assert len(payload["warnings"]) >= 2


def test_ingest_junit_xml_collects_failures():
    payload = ingest_junit_xml(
        """
<testsuite name="pytest" tests="3" failures="1" errors="0" skipped="0">
  <testcase classname="tests.test_demo" name="test_ok" />
  <testcase classname="tests.test_demo" name="test_refactor_guard">
    <failure message="behavior changed">assert 1 == 2</failure>
  </testcase>
  <testcase classname="tests.test_demo" name="test_other" />
</testsuite>
""".strip()
    )
    assert payload["ok"] is False
    assert payload["summary"]["passed"] == 2
    assert payload["summary"]["failed"] == 1
    assert any("tests.test_demo::test_refactor_guard - behavior changed" == e for e in payload["errors"])
