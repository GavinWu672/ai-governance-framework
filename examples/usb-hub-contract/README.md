# USB-Hub Contract Example

This example is a minimal dual-repo style domain plugin sample.

It is intentionally small and exists to validate three things:

1. `contract.yaml` discovery works
2. `session_start.py --contract ...` injects domain context
3. `pre_task_check.py --contract ...` can see external rule packs

## Files

- `contract.yaml`
- `AGENTS.md`
- `USB_HUB_FW_CHECKLIST.md`
- `USB_HUB_ARCHITECTURE.md`
- `rules/hub-firmware/safety.md`
- `validators/interrupt_safety_validator.py`

## Verify

PowerShell:

```powershell
$env:AI_GOVERNANCE_PYTHON='C:\Users\daish\AppData\Local\Python\pythoncore-3.14-64\python.exe'

& $env:AI_GOVERNANCE_PYTHON governance_tools\domain_contract_loader.py `
  --contract examples\usb-hub-contract\contract.yaml `
  --format human

& $env:AI_GOVERNANCE_PYTHON runtime_hooks\core\session_start.py `
  --project-root . `
  --plan PLAN.md `
  --rules common,hub-firmware `
  --risk medium `
  --oversight review-required `
  --memory-mode candidate `
  --task-text "Validate USB hub firmware response flow" `
  --contract examples\usb-hub-contract\contract.yaml `
  --format human

& $env:AI_GOVERNANCE_PYTHON runtime_hooks\core\pre_task_check.py `
  --project-root . `
  --rules common,hub-firmware `
  --risk medium `
  --oversight review-required `
  --memory-mode candidate `
  --task-text "Validate USB hub firmware response flow" `
  --contract examples\usb-hub-contract\contract.yaml `
  --format json
```
