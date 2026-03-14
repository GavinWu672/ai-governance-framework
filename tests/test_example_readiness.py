import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_tools.example_readiness import assess_examples, format_human_result


def test_example_readiness_reports_expected_examples():
    result = assess_examples(Path(".").resolve())

    assert result["ok"] is True
    names = [item["name"] for item in result["examples"]]
    assert names == ["todo-app-demo", "chaos-demo", "starter-pack", "usb-hub-contract"]

    by_name = {item["name"]: item for item in result["examples"]}
    assert by_name["todo-app-demo"]["kind"] == "runnable-demo"
    assert by_name["chaos-demo"]["kind"] == "walkthrough"
    assert by_name["starter-pack"]["kind"] == "scaffold"
    assert by_name["usb-hub-contract"]["kind"] == "domain-contract"
    assert by_name["usb-hub-contract"]["runtime_ready"] is True


def test_example_readiness_human_output_surfaces_runtime_status():
    result = assess_examples(Path(".").resolve())
    output = format_human_result(result)

    assert "[example_readiness]" in output
    assert "summary=name=todo-app-demo | kind=runnable-demo | ok=True" in output
    assert "summary=name=usb-hub-contract | kind=domain-contract | ok=True | runtime_ready=True" in output

    todo = next(item for item in result["examples"] if item["name"] == "todo-app-demo")
    if not todo["runtime_ready"]:
        assert any("fastapi" in warning.lower() for warning in todo["warnings"])
