---
title: "How far is cold fusion from known physics? A validated rate calculation, a two-sided bound on anomalous screening at rest, and a bound on the heat-only channel"
author: "[Author names and affiliations to be added]"
date: "Draft, October 2026"
abstract: |
  We compute deuterium–deuterium (and other hydrogen-isotope) fusion rates for nuclei at rest with a log-grid Numerov solver for the relative-motion ground state, $\Gamma = A|\psi(0)|^2$. The solver reproduces the D$_2$, HD and H$_2$ binding energies to $\le 0.001$ eV and the Koonin–Nauenberg molecular rates (d+d: $2.5\times10^{-64}$ vs $3\times10^{-64}$ s$^{-1}$; p+d: $10^{-55.2}$ vs $\sim10^{-55}$ s$^{-1}$). For deuterons at the PdD lattice spacing the rate is $\sim10^{-124}$ s$^{-1}$, about 114 orders of magnitude below the $\sim6\times10^{-11}$ s$^{-1}$ per pair needed for 1 W cm$^{-3}$. Compressing a pair, every hydrogen-isotope fuel except p+p reaches that level at a common spacing of 7–8 pm. We then model the anomalous electron screening reported in low-energy beam experiments on deuterated metals (165–800 eV) as a profile of strength fixed by the beam data and unknown range $\ell$. As $\ell$ grows, the rate jumps once the extra attraction binds a new short-range d–d state. Combining the beam constraint with the null neutron limit for loaded Pd and Ti at rest ($<2\times10^{-26}$ s$^{-1}$ per pair) bounds $\ell$ to $\approx 0.01$–$0.3$ Å across 40+ model variants. In every variant, rates approaching 1 W cm$^{-3}$ occur only at ranges already excluded by the neutron limit. Finally, we bound the "heat-only" channel, in which fusion energy goes directly to the lattice. Suppressing neutrons by even $10^{-3}$ requires a lattice decay width exceeding the 23.85 MeV transition energy. Electromagnetic, multi-phonon and coherent many-nucleus mechanisms fall short by $\sim$11, $\sim10^9$ and $\gtrsim 12$ orders of magnitude, and coherent transfer is additionally excluded by causality. We propose three experiments that test the remaining assumptions: a 5.5 MeV gamma search for p+d fusion in H/D co-loaded Pd at rest, beam screening in a heavy-fermion compound with a temperature switch, and same-target p+d vs d+d screening.
---

# 1. Introduction

Claims of nuclear fusion in deuterium-loaded metals at room temperature [Fleischmann–Pons 1989; Jones et al. 1989] were followed within months by calculations of the molecular d+d fusion rate [Koonin & Nauenberg 1989], by general bounds on barrier penetration in many-body systems at equilibrium [Leggett & Baym 1989], and by null neutron searches [e.g. Aberdam et al. 1990]. A large Google-funded re-examination found no evidence for the effect [Berlinguette et al. 2019].

One genuine anomaly has since been established by accelerator experiments. Low-energy d(d,p)t cross-sections in deuterated metals imply **electron screening energies** $U_e \approx 200$–$800$ eV [Raiola et al. 2002, 2004; Czerski et al.], an order of magnitude above the $\approx 25$ eV measured with gas targets and the $\approx 28$ eV adiabatic limit. Recent work reports a 15% increase in beam-driven fusion with electrochemical loading [Chen et al. 2025] and a sub-keV yield plateau in Pd and Ti deuterides [Karahadian et al. 2026]. Whether such effects persist for nuclei *at rest*, and how far they could go towards practical rates, has not been quantified jointly with the null searches.

This paper asks a narrow question: **how far, in orders of magnitude, is room-temperature fusion in metals from known physics, and which variables can close the gap?** We use one validated solver throughout. All code, notebooks and figures are public [repository].

# 2. Method

For a bound pair, the fusion rate is
$$\Gamma = A\,|\psi(0)|^2, \qquad A = \frac{S(0)\,c}{\pi\alpha\,\mu c^2},$$
where $S(0)$ is the zero-energy astrophysical S-factor and $\psi$ the s-wave ground state of the relative motion in potential $V(R)$. For d+d with $S(0) = 109.3$ keV b (Bosch–Hale, both branches), $A = 1.52\times10^{-16}$ cm$^3$ s$^{-1}$. We solve $u'' = 2\mu(V-E)u$ on a logarithmic grid from 0.5 fm, starting from the regular repulsive-Coulomb solution $u\simeq R(1+\mu R)$. The energy comes from node-counting bisection, and amplitudes are tracked in log space ($\psi(0)$ is $\sim10^{-37}$ of its peak).

**Potentials.** *Molecular:* the H$_2$ Born–Oppenheimer curve [Kolos & Wolniewicz 1965], splined to the He united-atom limit; heavier screening particles (mass $m^*$) via the exact scaling $V_{m^*}(R)=m^*V_1(m^*R)$. *Lattice:* Thomas–Fermi-screened repulsion (0.57 Å for Pd) plus a harmonic restoring force on the separation set by the PdD optical phonon (37 meV). *Anomalous screening:* $\Delta V(R) = -\Delta U\,g(R/\ell)$ with $g$ exponential, Gaussian, step or Yukawa-type. $\Delta U$ is fixed by requiring $\Delta V = -U_{\rm meas}$ at the beam turning point ($\approx 0.004$ Å). When $\Delta V$ creates a bound state at short range, we take the effective rate as the smaller of the bound-state fusion rate and the WKB tunneling rate into it.

**Validation** (Table 1). The solver reproduces D$_2$, HD and H$_2$ binding energies to $\le 0.001$ eV, the D$_2$ zero-point energy to $<1\%$, and the Koonin–Nauenberg rates for d+d and p+d. It is converged to 0.002 decades in step size and starting radius. The main systematic is the short-range potential: a 0.05 Ha error below 0.3 Å shifts the rate by 0.7 decades. We adopt $\pm1$ decade as the working uncertainty.

| Quantity | This work | Reference |
|---|---|---|
| D$_2$ binding $D_0$ | 4.5556 eV | 4.5562 eV |
| HD / H$_2$ binding | 4.5129 / 4.4771 eV | 4.5139 / 4.4781 eV |
| d+d rate in D$_2$ | $2.5\times10^{-64}$ s$^{-1}$ | $3\times10^{-64}$ [KN89]; $5.7\times10^{-64}$ [2025] |
| p+d rate in HD | $10^{-55.2}$ s$^{-1}$ | $\sim10^{-55}$ [KN89] |
| Thermal reactivity (Gamow integral) | within 1–2% | Bosch–Hale fit, 0.2–50 keV |

# 3. Results

## 3.1 The gap

1 W cm$^{-3}$ in PdD requires $\sim6\times10^{-11}$ fusions per pair per second. A d–d pair at the lattice spacing (2.75 Å) gives $10^{-124}$ s$^{-1}$, a gap of **~114 orders of magnitude**. The often-quoted ~53 orders is against a D$_2$ molecule (0.74 Å), which the lattice does not provide. Varying spacing (1.5–2.75 Å), phonon energy and Thomas–Fermi length moves the lattice rate by at most tens of orders.

## 3.2 Closer and lighter

Scaling the molecular potential by a heavier screening particle compresses the pair. Watt-level rates need $m^*\approx 9.2$ for d+d (Koonin & Nauenberg: 5–10), i.e. a **pair spacing of 8.0 pm**. Repeating this for all hydrogen-isotope pairs, p+d, p+t, d+d and d+t all reach watt level at **7.3–8.2 pm**; p+p never does (weak-interaction S-factor). Lighter pairs lead at long range (p+d is $10^{8}$ above d+d in a molecule, $10^{17}$ at lattice spacing), but larger S-factors win near the watt zone. An independent calculation for a lattice-type pair held at fixed spacing by an external force gives the same 7.3 pm, at an energy cost of ~170 eV per pair (Boltzmann factor $10^{-2900}$ at 300 K). Deuterium clusters in a Pd vacancy (N = 2–6) do not help: mutual repulsion places the nearest pair at 2.8–3.8 Å.

## 3.3 Anomalous screening at rest: a two-sided bound

Fig. 1 shows the effective rate for a lattice pair along the beam-consistent curve. If the screening reaches only the few-hundredths of an ångström the beam data probe, the rate stays below $10^{-100}$ s$^{-1}$. As $\ell$ increases, the rate **jumps** when $\Delta V$ binds a new d–d state at 0.07–0.24 Å (deeper and closer for larger $U_{\rm meas}$). It is then limited by tunneling into that state and by fusion within it.

The null neutron limit for Pd and Ti at rest, $<2\times10^{-26}$ s$^{-1}$ per pair [Aberdam et al. 1990], then bounds $\ell$. For an exponential profile, $\ell < 0.154$ Å (300 eV), $0.137$ Å (575 eV) and $0.129$ Å (800 eV). Across 40 variants (profile shape, harmonic vs barrier-capped lattice, spacing, Thomas–Fermi length, phonon energy, attempt frequency $\times10^{\pm3}$, weaker null limit) plus the 800 eV case, the bound spans **0.012–0.315 Å** (median 0.137 Å). It is dominated by profile shape and screening length; lattice stiffness and tunneling kinetics hardly matter. At 165 eV and for step profiles the static limit does not constrain $\ell$, but those cases never come within 20 orders of watt level.

**Watts imply neutrons.** Several variants reach $\ge 1$ W cm$^{-3}$ at $U_{\rm meas}\ge 575$ eV. In every one, the rate crosses the neutron limit at a *shorter* range than it reaches watt level (e.g. Yukawa profile at 800 eV: 0.012 Å vs 0.016 Å). No variant jumps from below the limit to watt level.

## 3.4 p+d in mixed H/D lattices

p+d → $^3$He + γ (5.49 MeV) has no neutron branch. With the same beam-consistent screening, the p+d lattice rate peaks at $10^{-12.3}$ s$^{-1}$ (575 eV), so even at a 50/50 H/D mix it is ~2.5 orders short of watt level. Past the bound-state jump, d+d and p+d converge to within an order of magnitude, so the coexisting d+d pairs would still violate the neutron limit first. p+d also cannot be "heat-only": 1 W would emit $\sim10^{12}$ gammas per second.

## 3.5 The heat-only channel

The d+d compound state $^4$He$^*$ (23.85 MeV) decays strongly with widths $\Gamma_{\rm strong}\sim0.5$–6 MeV (lifetimes $10^{-22}$–$10^{-21}$ s), and radiatively with $\Gamma_\gamma/\Gamma_p\approx 10^{-7}$ [Zhou et al. 2006]. Suppressing neutrons by $s_n$ needs a lattice width $\Gamma_{\rm lat}\gtrsim\Gamma_{\rm strong}/s_n$, which is **already 20–260× the transition energy at $s_n=10^{-3}$** and $10^{10}$–$10^{11}$× at $10^{-12}$. A state that wide is not a state, so any heat-only process cannot go through $^4$He$^*$. For mechanisms that do:

- **electromagnetic** (internal conversion, pair creation) falls short by ~11–20 orders;
- **direct multi-phonon** emission (Englman–Jortner energy-gap law, $6.4\times10^8$ phonons) gives rates $\sim10^{-4\times10^9}$ s$^{-1}$ for any plausible coupling;
- **coherent many-nucleus** coupling needs $\sim10^{15}$–$10^{33}$ phase-locked nuclei (vs $\sim10^3$ in coherent domains).

It is also **causally excluded**: in the compound-nucleus lifetime, light travels $<0.003$ Å, far less than the distance to the nearest neighbouring deuteron.

## 3.6 Other levers

Cold metallic deuterium reaches 1 W cm$^{-3}$ pycnonuclearly only at $\sim1.6\times10^4$ g cm$^{-3}$. Coherent resonant tunneling through an intermediate well adds nothing beyond sequential tunneling once energies are spread over more than the resonance width (≲$10^{-31}$ eV vs $\sim10^{-2}$ eV). Muon-catalysed d–t fusion, the one room-temperature route that works, is ~1.5× from scientific breakeven and ~9× from net electricity, a gap that depends on sticking and cycling measurements now being made at high density (MuFusE).

# 4. Proposed experiments

**E1: p+d gamma search at rest.** A 10 g Pd foil co-loaded with H and D (0.45/0.45), steady and cycled loading, a shielded HPGe/LaBr$_3$ detector with muon veto, run for 30 days, with H-only, D-only and unloaded controls. With assumed backgrounds this reaches $\sim10^{-26}$ (surface) and $4\times10^{-28}$ (underground) per p–d pair per s, extending the range bound to a neutron-free channel.

**E2: heavy-fermion screening with a temperature switch.** d(d,p)t at $E_d$ = 5–30 keV on a deuterium-implanted heavy-fermion compound (Ce- or Yb-based) and its non-f analogue, at 4 K and 300 K, with in-situ ERDA depth profiling. "Heavy-electron" screening predicts a large rise only below the coherence temperature; standard theory predicts no change. About 6 h per point at 10 μA.

**E3: same-target p+d vs d+d screening.** Alternating H$^+$/D$^+$ beams matched in stopping range on one deuterated target. This separates true screening (equal $U_e$), depth-profile artifacts (range-dependent) and a d+d-specific nuclear resonance ($U_e^{dd}>U_e^{pd}$). A 5σ answer needs ~2.6% p+d statistics, about 1.5 days per point at 1 mA.

# 5. Discussion and limitations

**Relation to prior work.** Leggett & Baym [1989] bounded barrier penetration for any many-body system at equilibrium; our static-screening conclusion agrees. The contribution here is to use the *measured* beam screening, model its unknown range, and confront it with the *null* neutron data, which gives a numerical bound on the range at rest and the "watts imply neutrons" result across model variants. Czerski, Heide & Huke [2006] extrapolated effective screening energies to cold-fusion energies and compared with positive claims. Their full text should be compared in detail before any novelty claim is made.

**Limitations.** (i) The short-range H$_2$ potential uses recalled Kolos–Wolniewicz values. They are supported by the binding-energy and Koonin–Nauenberg checks but were not re-read from the original table. (ii) Several literature inputs were verified only at abstract level (see VERIFICATION.md). (iii) The lattice model is a single radial pair; anisotropy, many-body exchange and defects beyond a spherical vacancy are not modelled. (iv) The screening profiles are phenomenological. (v) The heat-only analysis uses order-of-magnitude internal-conversion and pair-creation coefficients and the weak-coupling energy-gap law.

# 6. Conclusions

Within standard physics and the stated assumptions:

1. Room-temperature fusion in metals is ~114 orders of magnitude from 1 W cm$^{-3}$.
2. Every fuel needs pairs held at ~7–8 pm, costing ~170 eV per pair.
3. The anomalous screening seen in beam experiments cannot extend beyond ~0.01–0.3 Å at rest without having produced neutrons already excluded in 1990, and any configuration approaching watts would have produced them.
4. A heat-only channel cannot dispose of the energy of any process that forms excited $^4$He.

The remaining open questions are experimental and well posed (E1–E3).

**Data and code availability.** All notebooks, the solver (`cfsolve.py`), the claim-checking tool and figures: https://github.com/m1110/cold-fusion-gap

**Acknowledgements.** Analysis code and drafting were assisted by an AI model (Claude, Anthropic); all results are reproducible from the repository.

# References (to be completed and checked against primary sources)

- Aberdam D. et al., Phys. Rev. Lett. 65, 1196 (1990).
- Berlinguette C. P. et al., Nature 570, 45 (2019).
- Bosch H.-S. & Hale G. M., Nucl. Fusion 32, 611 (1992) (and erratum).
- Chen K.-Y. et al., Nature 644, 640 (2025).
- Ciuchi S. et al., Eur. Phys. J. C 72, 2193 (2012).
- Czerski K., Heide P. & Huke A., in Condensed Matter Nuclear Science (ICCF11), 228 (2006).
- Czerski K. et al., EPL 113, 22001 (2016).
- Englman R. & Jortner J., Mol. Phys. 18, 145 (1970).
- Huke A., Czerski K. & Heide P., arXiv:0805.4538 (2008).
- Jones S. E. et al., Nature 338, 737 (1989).
- Karahadian M. et al., Nat. Commun. 17, 8845 (2026).
- Kolos W. & Wolniewicz L., J. Chem. Phys. 43, 2429 (1965).
- Koonin S. E. & Nauenberg M., Nature 339, 690 (1989).
- Leggett A. J. & Baym G., Phys. Rev. Lett. 63, 191 (1989); Nature 340, 45 (1989).
- Raiola F. et al., Eur. Phys. J. A 13, 377 (2002); 19, 283 (2004).
- Tilley D. R., Weller H. R. & Hale G. M., Nucl. Phys. A 541, 1 (1992).
- Zhou J. et al., Chin. Phys. Lett. (2006), d(d,γ)⁴He branching at 20 keV.
