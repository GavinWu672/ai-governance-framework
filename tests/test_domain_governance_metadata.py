import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_tools.domain_governance_metadata import domain_priority_rank, normalize_domain_name


def test_normalize_domain_name_lowercases_and_trims():
    assert normalize_domain_name("  Kernel-Driver ") == "kernel-driver"


def test_domain_priority_rank_prefers_high_risk_domains():
    assert domain_priority_rank("kernel-driver") < domain_priority_rank("firmware")


def test_domain_priority_rank_returns_default_for_unknown_domain():
    assert domain_priority_rank("mobile-app") == 50
    assert domain_priority_rank(None) == 99
