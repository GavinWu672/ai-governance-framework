import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_tools.domain_contract_loader import load_domain_contract
from runtime_hooks.core.pre_task_check import run_pre_task_check
from runtime_hooks.core.session_start import build_session_start_context, format_human_result


EXAMPLE_CONTRACT = Path("examples/usb-hub-contract/contract.yaml")


def test_usb_hub_example_contract_loads():
    loaded = load_domain_contract(EXAMPLE_CONTRACT)

    assert loaded is not None
    assert loaded["name"] == "usb-hub-firmware-contract"
    assert len(loaded["documents"]) == 2
    assert len(loaded["ai_behavior_override"]) == 1
    assert loaded["validators"][0]["name"] == "interrupt_safety_validator"


def test_usb_hub_example_session_start_includes_domain_previews():
    result = build_session_start_context(
        project_root=Path(".").resolve(),
        plan_path=Path("PLAN.md"),
        rules="common,hub-firmware",
        risk="medium",
        oversight="review-required",
        memory_mode="candidate",
        task_text="Validate USB hub firmware response flow",
        contract_file=EXAMPLE_CONTRACT,
    )

    output = format_human_result(result)
    assert "domain_contract=usb-hub-firmware-contract" in output
    assert "domain_documents=USB_HUB_FW_CHECKLIST.md,USB_HUB_ARCHITECTURE.md" in output
    assert "domain_behavior_overrides=AGENTS.md" in output
    assert "behavior_preview[AGENTS.md]=# USB-Hub Firmware Agent Rules" in output
    assert "document_preview[USB_HUB_FW_CHECKLIST.md]=# USB Hub Firmware Checklist" in output


def test_usb_hub_example_pre_task_check_loads_external_rule_pack():
    result = run_pre_task_check(
        project_root=Path(".").resolve(),
        rules="common,hub-firmware",
        risk="medium",
        oversight="review-required",
        memory_mode="candidate",
        task_text="Validate USB hub firmware response flow",
        contract_file=EXAMPLE_CONTRACT,
    )

    names = [pack["name"] for pack in result["active_rules"]["active_rules"]]
    content = "\n".join(
        file["content"]
        for pack in result["active_rules"]["active_rules"]
        if pack["name"] == "hub-firmware"
        for file in pack["files"]
    )

    assert result["ok"] is True
    assert names == ["common", "hub-firmware"]
    assert "HUB-001 - cfu-response-must-follow-request" in content
    assert "HUB-004 - dptr-guard" in content
