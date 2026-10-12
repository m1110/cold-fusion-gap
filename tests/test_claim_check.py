import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "notebooks"))
from claim_check import check
from cfsolve import solve, V_molecule


def test_solver_reproduces_koonin_nauenberg():
    assert abs(solve(V_molecule(), 8.0, Rmin_well=0.5)["log10_rate"] - (-63.6)) < 0.2


def test_one_watt_dd_conflicts_with_null_limit():
    _, r = check(1.0, "Pd", 1.0, 0.9, "dd", neutrons=1.0, quick=True)
    assert r["rate"] > 2e-26
    assert any("null limit" in i for i in r["issues"])
    assert any("lattice decay width" in i for i in r["issues"])


def test_tiny_power_is_consistent():
    _, r = check(1e-30, "Pd", 1.0, 0.9, "dd", quick=True)
    assert r["issues"] == []
