#!/usr/bin/env python3
"""Check a claimed low-energy fusion result against the physics in this repository.

Given a claimed excess power, the metal sample, its hydrogen-isotope loading and (optionally) the radiation
actually observed, report: the implied reaction rate per pair, how far that is above standard physics,
the pair spacing it would require, the radiation it should have produced, and which measured limits or
results from notebooks 03-07 it conflicts with.

Example:
    python tools/claim_check.py --power 1 --metal Pd --mass 1.0 --loading 0.9 --fuel dd --neutrons 1
"""
import argparse, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "notebooks"))
from cfsolve import (solve, V_lattice, V_lattice_pair, reduced_mass, BOHR_A, MU_DD, S_KEVB)

MEV_J = 1.602176634e-13
METALS = {  # density g/cm3, molar mass g/mol, nearest-neighbour interstitial sites (approx.), site spacing A
    "Pd": (12.02, 106.42, 12, 2.75),
    "Ni": (8.91, 58.69, 12, 2.49),
    "Ti": (4.51, 47.87, 12, 2.2),
}
FUELS = {  # S(0) keV b, products: list of (branch fraction, Q MeV, signature)
    "dd": (S_KEVB, [(0.5, 3.27, "neutron 2.45 MeV + 3He"), (0.5, 4.03, "proton 3.0 MeV + triton (tritium)"),
                    (1.06e-7*0.5, 23.85, "gamma 23.8 MeV")]),
    "pd": (2.0e-4, [(1.0, 5.49, "gamma 5.5 MeV")]),
    "heat-only": (S_KEVB, [(1.0, 23.85, "4He, no radiation (hypothetical; see notebook 07)")]),
}
NULL_LIMIT_DD = 2e-26          # per d-d pair per s, Aberdam et al., PRL 65, 1196 (1990)
HEAT_ONLY_MIN_WIDTH = 0.5e6    # eV: Gamma_strong lower end; Gamma_lat >= Gamma_strong / s_n (notebook 07)


def held_rate(d0_A, mu, S):
    lam = 0.574/BOHR_A; d0 = d0_A/BOHR_A; K = mu*(37e-3/27.211386)**2
    c = np.exp(-d0/lam)*(1/d0**2 + 1/(lam*d0))
    V = lambda R: np.exp(-R/lam)/R + 0.5*K*(R - d0)**2 + c*(R - d0)
    return solve(V, d0 + 7.0, r0=min(1e-5, d0*1e-3), Rmin_well=0.3*d0, mu=mu, S_keVb=S)["log10_rate"]


def check(power_W, metal, mass_g, loading, fuel, neutrons=None, gammas=None, helium=None, h_fraction=0.0, quick=False):
    rho, M, z, spacing = METALS[metal]
    S, branches = FUELS[fuel]
    a, b = ("p", "d") if fuel == "pd" else ("d", "d")
    mu = reduced_mass(a, b)
    out = []
    p = out.append
    N_sites = mass_g/M*6.02214076e23
    xD = loading*(1 - h_fraction); xH = loading*h_fraction
    pairs = N_sites*z/2*(2*xH*xD if fuel == "pd" else xD**2)
    Q_mean = sum(f*Q for f, Q, _ in branches)/sum(f for f, _, _ in branches)
    R = power_W/(Q_mean*MEV_J)
    rate = R/pairs
    p(f"Claim: {power_W:g} W from {mass_g:g} g {metal}, loading {loading:g} (H fraction {h_fraction:g}), fuel {fuel}")
    p(f"  implied reactions: {R:.2e} /s;  {pairs:.2e} nearest-neighbour {a}-{b} pairs;  rate per pair {rate:.1e} /s")
    base = solve(V_lattice_pair(a, b, d0_A=spacing), spacing/BOHR_A + 7.0, Rmin_well=0.4*spacing/BOHR_A,
                 mu=mu, S_keVb=S)["log10_rate"]
    p(f"  standard physics at the lattice spacing ({spacing} A): 10^{base:.1f} /s  ->  claim is {np.log10(rate)-base:.0f} orders above")
    if not quick:
        d0s = np.logspace(np.log10(0.03), np.log10(spacing), 30)
        lr = np.array([held_rate(d, mu, S) for d in d0s])
        if lr.max() > np.log10(rate) > lr.min():
            dneed = 10**np.interp(np.log10(rate), lr[::-1], np.log10(d0s)[::-1])
            cost = 14.3996*(np.exp(-dneed/0.574)/dneed - np.exp(-spacing/0.574)/spacing)
            p(f"  pair spacing that rate requires: {dneed*100:.1f} pm (lattice holds {spacing*100:.0f} pm); "
              f"holding it costs ~{cost:.0f} eV per pair (lattice binding ~0.1-0.3 eV)")
    p("  expected signatures with standard branching:")
    for f, Q, sig in branches:
        p(f"     {sig:52s} {R*f:.2e} /s")
    issues = []
    if fuel == "dd":
        n_exp = R*0.5
        if rate > NULL_LIMIT_DD:
            issues.append(f"rate per d-d pair {rate:.1e} exceeds the 1990 null limit {NULL_LIMIT_DD:.0e} by {rate/NULL_LIMIT_DD:.0e}x "
                          "(PRL 65, 1196; Pd and Ti at rest)")
        if neutrons is not None and n_exp > 0:
            s_n = max(neutrons, 1e-300)/n_exp
            p(f"  observed neutrons {neutrons:g} /s vs expected {n_exp:.1e} /s -> suppression s_n = {s_n:.1e}")
            if s_n < 1e-3:
                need = HEAT_ONLY_MIN_WIDTH/s_n
                issues.append(f"neutron suppression {s_n:.0e} needs a lattice decay width >= {need:.0e} eV, "
                              f"{need/23.85e6:.0e}x the 23.85 MeV transition energy (notebook 07: excluded)")
    if fuel == "pd" and gammas is not None:
        g_exp = R
        if gammas < 1e-3*g_exp:
            issues.append(f"observed 5.5 MeV gammas {gammas:g}/s vs {g_exp:.1e}/s expected: disposing of 5.5 MeV without the "
                          "gamma needs multi-phonon or coherent transfer, excluded in notebook 07 (energy-gap law, causality)")
    if fuel == "heat-only":
        issues.append("heat-only conversion of 23.85 MeV is excluded for any process through excited 4He (notebook 07); "
                      "coherent transfer is also causality-limited (< 0.003 A in the compound-nucleus lifetime)")
    if helium is not None:
        he_exp = power_W/(23.85*MEV_J)
        p(f"  helium: reported {helium:.1e} /s; heat-only 23.85 MeV/He would give {he_exp:.1e} /s (ratio {helium/he_exp:.2f})")
    p("  verdict:" if issues else "  no conflicts found with the limits in this repository")
    for i in issues:
        p(f"     - {i}")
    return "\n".join(out), dict(rate=rate, base=base, issues=issues)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--power", type=float, required=True, help="claimed excess power, W")
    ap.add_argument("--metal", choices=METALS, default="Pd")
    ap.add_argument("--mass", type=float, required=True, help="metal mass, g")
    ap.add_argument("--loading", type=float, default=0.9, help="(H+D)/metal atom ratio")
    ap.add_argument("--h-fraction", type=float, default=0.0, help="fraction of the loading that is H (for pd)")
    ap.add_argument("--fuel", choices=FUELS, default="dd")
    ap.add_argument("--neutrons", type=float, help="observed neutron emission, n/s (upper limit if none seen)")
    ap.add_argument("--gammas", type=float, help="observed 5.5 MeV gammas, /s (for pd)")
    ap.add_argument("--helium", type=float, help="reported 4He production, atoms/s")
    ap.add_argument("--quick", action="store_true", help="skip the pair-spacing scan (~20 s)")
    a = ap.parse_args()
    text, _ = check(a.power, a.metal, a.mass, a.loading, a.fuel, a.neutrons, a.gammas, a.helium, a.h_fraction, a.quick)
    print(text)


if __name__ == "__main__":
    main()
