# Source verification and prior-work check

**Method and limit:** arXiv and PubMed became reachable on 2026-10-12 and are read through `tools/fetch.py` (rate-limited, cached, logged). Google Scholar and PhilPapers are not used (their terms forbid automated access). OSTI, INSPIRE, Crossref and OpenAlex APIs remained blocked by network policy. Rows marked *primary* were checked against the full text. Every check below went through a web-search index (abstracts, metadata, snippets). Status levels:

- **Confirmed (abstract):** the value appears in an indexed abstract or official record.
- **Confirmed (secondary):** quoted by a later review or paper, not seen in the original.
- **Internal check:** not found in a source, but reproduced by independent computed quantities.
- **Unverified:** neither.

To upgrade any row, read the primary paper (DOIs given) or allow those domains in the environment's network settings.

## Key inputs

| Input | Value used | Status | Source / note |
|---|---|---|---|
| Koonin–Nauenberg D₂ fusion rate | 3×10⁻⁶⁴ s⁻¹ | Confirmed (abstract) | *Nature* 339, 690 (1989); preprint abstract |
| Koonin–Nauenberg p+d rate | ~10⁻⁵⁵ s⁻¹ | Confirmed (abstract) | same; our solver gives 10⁻⁵⁵·³ |
| Koonin–Nauenberg heavy electron | ×5–10 for claimed rates | Confirmed (abstract) | same |
| 2025 recalculation | 5.7×10⁻⁶⁴ s⁻¹ | **Confirmed (primary, full text)** | arXiv:2501.08338, eq. (305); also quotes K–N 3×10⁻⁶⁴ (eqs. 102, 299) |
| H₂ Born–Oppenheimer curve | **Pachucki 2010 Table IV, R = 0.1–20 bohr (82 points)** | **Confirmed (primary, full text)** | arXiv:1007.0322. The earlier recalled Kolos–Wolniewicz points (R = 0.4–1.4) match it to ≤10⁻⁴ Ha. Adopting the full table moved the D₂ rate from 10⁻⁶³·⁶⁰ to 10⁻⁶³·⁷⁰ and p+d from 10⁻⁵⁵·²⁰ to 10⁻⁵⁵·²⁸; binding energies now D₂ 4.5559 (expt 4.5562), HD 4.5133 (4.5139), H₂ 4.4774 (4.4781) eV |
| H₂ minimum | −1.1744759 Ha | Confirmed (abstract) | Pachucki 2010; Sims & Hagstrom 2006 |
| Neutron null limit, Pd & Ti at rest | < 2×10⁻²⁶ s⁻¹ per pair | **Confirmed (official record)** | Aberdam et al., *PRL* 65, 1196 (1990), 18 authors; OSTI record gives the exponent (the APS page renders it incorrectly) |
| Weaker limit | < 3.6×10⁻²³ s⁻¹ | Confirmed (abstract) | Badurek et al. 1989 |
| Jones et al. claim | ~10⁻²³ s⁻¹ (Ti) | Confirmed (secondary) | *Nature* 338 (1989), via reviews |
| Screening, Ta | 309±12 / **340±14 / 340±24** eV | Confirmed (abstract); values differ across reports | Raiola et al. 2002; later reviews quote 340 |
| Screening, **Pd** | **250±15 or 800±90 eV** | **Both confirmed in primary full text; they are different measurements** | 250±15 eV: arXiv:0804.3886 (deuterated Pd, citing Kasagi et al.); 800±90 eV: arXiv:cond-mat/0612306 (PdD). Range 165–575 eV used in notebooks 03–05; 800 eV re-run below |
| Screening, **Pd/Ti keV values** | Pd 0.8±0.2, **PdD 1.7±0.2**, Ti 0.3±0.2, TiD 0.9±0.2 keV | **Confirmed (primary, full text)** | Karahadian et al., Nat. Commun. 17, 8845 (2026), arXiv:2512.06212. Authors note U_e may lump several mechanisms. Analysed in notebooks 04b, 05b, 13. Fit method (thick target, normalised at E_cm = 6.5 keV, constant-U_e fit 6.5→2.5 keV; Ti >2.0 keV) confirmed from full text and reproduced in notebook 13. Fig. 2 digitised (notebook 14): the plotted model curves match a thin-target ratio, and a thick-target refit gives 1.08/1.86/0.85/1.16 keV, so U_e is model-dependent beyond ±0.2 keV |
| Sun & Tománek separations | 0.94 Å minimum, ~1.4 Å average | Reference confirmed (PRL 63, 59, 1989); values secondary | Analysed in notebook 04b |
| Screening, noble metals | Cu 43, Ag 23, Au 61 eV | Confirmed (secondary) | NASA GRC review (Pines et al. 2020) |
| D₂ gas screening | 25±5 eV | Confirmed (secondary) | LUNA overview, arXiv:0906.1097 |
| Adiabatic limit | ~27–28 eV | Confirmed (secondary) | several reviews |
| Bosch–Hale D+D S-factors and reactivities | as used | Confirmed via reproduction | our Gamow integral reproduces the BH reactivity to 1–2% (notebook 01) |
| Bosch–Hale **d+t** S-factor coefficients | A1 = 6.927e4, A2 = 7.454e8, B1 = 63.8 … | **Unverified** (recalled) | paper confirmed: *Nucl. Fusion* 32, 611 (1992) (**has an erratum**). Affects only the d+t row in notebooks 05–06 |
| p+p S(0) | 4.01×10⁻²⁵ MeV b | Confirmed (abstract) | Solar Fusion II (Adelberger et al. 2011) |
| p+d S(0) | 0.20 eV b (literature 0.16–0.24) | Confirmed (abstract), range | EFT and earlier evaluations |
| p+t S(0) | 0.95 eV b | Confirmed (abstract) | arXiv:1811.04779 |
| **t+t S(0)** | 150 keV b | **Unverified** | no zero-energy value found; NIF measured tt S at 2–5 keV (OSTI 1404861). Affects only the t+t row |
| PdD optical phonon | ~37 meV (H in Pd ~69 meV) | Confirmed (abstract) | inelastic neutron scattering studies |
| D-in-Pd diffusion barrier | 0.23 eV (varied 0.1–0.4) | **Unverified** for bulk D; surface-entry barrier 0.43 eV found | notebook 04 shows the result is *insensitive* to this |
| Pd displacement energy | 34±2 eV | Confirmed (abstract) | *Phys. Rev.* 153, 735 (1967) |
| Muon catalysis | ~150 fusions/μ; breakeven ~280 at 5 GeV/μ | Confirmed (secondary) | LANL experiments, recent reviews |
| ddμ fusion rate | 10⁸–10⁹ s⁻¹ (J=1) | Confirmed (secondary), order only | used only as a sanity note |

## Re-run: Pd at U_e = 800 eV (the high Pd value)

Same analysis as notebook 04 (lattice pair, beam-matched at 0.004 Å, effective rate):

| Screening shape | Null limit crossed at ℓ | Watts reached at ℓ | Max rate |
|---|---|---|---|
| exponential | 0.129 Å | 0.171 Å | 10⁻⁸·⁶ |
| Gaussian | 0.301 Å | never | 10⁻¹⁷·⁴ |
| step | never | never | 10⁻³³·⁰ |
| Yukawa | 0.012 Å | 0.016 Å | 10⁻⁵·⁴ |

**Conclusion (B) of notebook 04 survives:** at 800 eV, watts become reachable for two profile shapes, but **in both, the null limit is crossed at a shorter range first.** The range bound widens to 0.012–0.30 Å.

## Re-run: closer equilibrium D–D separations (Sun & Tománek)

Literature (via reviews; primary not yet read) reports that deuterons in heavily loaded Pd can sit in equilibrium as close as **0.94 Å** (average ~1.4 Å), closer than the 1.5–2.75 Å used in notebooks 03–08. Same analysis (exponential profile, beam-matched):

| D–D spacing | Bare rate | U_meas = 300 eV: null crossed / watts | 575 eV | 800 eV |
|---|---|---|---|---|
| 1.4 Å | 10⁻¹¹²·¹ | 0.122 Å / never | 0.108 / 0.137 Å | 0.096 / 0.122 Å |
| 0.94 Å | 10⁻¹⁰⁹·⁵ | 0.108 Å / never | 0.085 / 0.108 Å | 0.076 / 0.108 Å |

**"Watts imply neutrons" holds at both spacings;** the range bound tightens to ~0.08–0.12 Å. To add to notebook 04 and the paper.

## Prior work to engage (added after novelty search)

- **Leggett & Baym (1989):** in equilibrium, the d–d tunneling rate is bounded above by the Born–Oppenheimer value (secondary sources quote ~10⁻⁴⁷ s⁻¹ per pair). They also argued that strongly reduced short-range repulsion would imply enhanced binding of alpha particles to the metal, which is not observed (cf. our thermochemistry remark, notebook 08). **Their bound is theoretical and equilibrium-based; ours is empirical (measured U_e + null limit) and model-based. The paper must present them as complementary and explain why the measured beam anomaly does not contradict theirs** (beam measurements are not equilibrium at rest).
- **Parmenter & Lamb, PNAS (1989):** conduction-electron screening could give ~10⁻³⁰ s⁻¹ per pair, 7 orders below the Jones claim.
- **Sun & Tománek (1989):** equilibrium D–D separations down to 0.94 Å in Pd (row above).
- **Karahadian et al. (2026) Pd/PdD/Ti/TiD screening dataset**: fitting procedure reproduced in notebook 13; points digitised from Fig. 2 (notebook 14; digitisation, not tabulated data). Request the tabulated points and their yield model from the authors; a 2026 two-band screening model (Zenodo) and a 2025 lithium-screening study: newer data the paper should cite and, ideally, fit.

## Prior work: what is already known, and what may be new

| Prior work | What it established | Relation to this repo |
|---|---|---|
| **Leggett & Baym, *PRL* 63, 191 (1989)**; *Nature* 340, 45 (1989) | An exact upper bound on barrier penetration in any many-body system **in equilibrium**; screening in a solid at equilibrium can't give the claimed rates | Same conclusion for static screening, from general principles. Our work is **not** the first to bound solid-state screening. Their bound is equilibrium-only; ours uses measured U_e plus a model profile |
| **Czerski, Heide, Huke, ICCF11 proceedings (2006), "Electron screening constraints for the cold fusion"** | Dielectric theory of U_e (underestimates by ~2×). Rates extrapolated to cold-fusion energies with an effective U_e and compared with electrolysis data | Closest prior work. As far as the abstract shows, they used a **constant** U_e and compared with *positive* claims; we model the **range** and compare with the **null** neutron limit |
| Koonin–Nauenberg (1989); arXiv:2501.08338 (2025) | Molecular rates, heavy-electron requirement | We reproduce both, extend to all isotope pairs and the lattice |
| Huke et al. (2008); Lipoglavšek group | Artifacts and lattice effects in U_e extraction | Motivates experiment E3 |

**Candidate novel contributions** (to be checked against the full texts of Leggett–Baym and Czerski et al. 2006 before any claim):
1. A **two-sided** constraint: beam-measured U_e (short range) combined with 1990 null neutron limits (rest) bounds the **range** of anomalous screening at rest to ~0.01–0.3 Å, robust across 40+ model variants.
2. "**Watts imply neutrons**" for any screening-plus-confinement mechanism, holding across all profile shapes, lattice models and U_e up to 800 eV.
3. The **~7–8 pm universal spacing** target across hydrogen-isotope fuels, and the p+d analysis in mixed lattices.
4. The **E1–E3 designs**, in particular a neutron-free p+d gamma search at rest, and heavy-fermion screening with a temperature switch.

- **Muon production cost** (notebook 16): 5 GeV per muon is stated in arXiv:2511.20951 and arXiv:2605.26432 (both read in full; they cite Jändel 1989). Kelly et al. 2021 (J. Phys. Energy 3, 035003) give 2.5× lower, at abstract level, *including* waste-energy recovery. The 3.0 GeV active-target figure comes from an ARPA-E presentation (secondary). The X scenarios are from Yin et al. 2026 Table I. The Holmlid cheap-muon claim is disputed (Hansen & Engelen 2023, Energy Sustain. Soc.) and not used.
