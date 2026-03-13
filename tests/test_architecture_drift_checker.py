import sys
from pathlib import Path
import shutil

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_tools.architecture_drift_checker import check_architecture_drift


@pytest.fixture
def local_drift_root():
    path = Path("tests") / "_tmp_architecture_drift"
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_architecture_drift_checker_flags_cross_project_private_include(local_drift_root):
    target = local_drift_root / "sample.cpp"
    target.write_text('#include "../etoken_server/Global.h"\n', encoding="utf-8")

    result = check_architecture_drift(file_paths=[target], scope="feature")

    assert result["ok"] is False
    assert any("Cross-project private include detected" in error for error in result["errors"])


def test_architecture_drift_checker_flags_additional_include_directories_peer_path(local_drift_root):
    target = local_drift_root / "DatabaseService.vcxproj"
    target.write_text(
        "<AdditionalIncludeDirectories>$(ProjectDir);..\\etoken_server\\include</AdditionalIncludeDirectories>",
        encoding="utf-8",
    )

    result = check_architecture_drift(file_paths=[target], scope="feature")

    assert result["ok"] is False
    assert any("AdditionalIncludeDirectories references peer-private path" in error for error in result["errors"])


def test_architecture_drift_checker_warns_on_refactor_boundary_drift():
    diff_text = "Move Domain logic to Infrastructure to simplify reference graph"

    result = check_architecture_drift(diff_text=diff_text, scope="refactor")

    assert result["ok"] is True
    assert any("Potential refactor boundary drift" in warning for warning in result["warnings"])
