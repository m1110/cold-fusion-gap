# cold-fusion-gap

Quantitative notebooks asking one question: **how far is known physics from cold fusion, and where could something be missing?**

| Notebook | What it does |
|---|---|
| `notebooks/01_rate_gap.ipynb` | Rate gap (~10^52–53), required effective temperature (65 eV, from a numerical Gamow integral validated against Bosch–Hale to 1–2%), coherence scaling limits, exit-channel constraint, muon catalysis balance, literature check |
| `notebooks/03_bridge_and_bounds.ipynb` | Quantum solver for the d–d pair's ground state (`cfsolve.py`), validated against D₂ binding/zero-point energy and Koonin–Nauenberg; exact heavy-electron scan; lattice-pair model; extra-screening map bounded by beam data and 1990 neutron limits |
| `notebooks/04_robustness.ipynb` | Robustness of notebook 03 over 40 variants: screening shape (exponential, Gaussian, step, Yukawa), capped vs harmonic lattice, spacing, Thomas–Fermi length, phonon energy, attempt frequency, weaker null limit |
| `notebooks/04b_kev_screening_and_spacing.ipynb` | Claims A and B re-tested with keV screening (Karahadian et al. 2026: PdD 1.7 keV, TiD 0.9 keV) and closer D–D spacings (0.94, 1.4 Å): 72 variants |
| `notebooks/11_other_paths.ipynb` | Energetic deuterons in metals (lattice confinement fusion, beam-loaded PdD): energy return; survey of catalysis, ignition, aneutronic fuels, low-waste fission |
| `notebooks/05b_pd_window_kev.ipynb` | Neutron-free p+d in mixed H/D lattices at keV screening (0.9–2.0 keV): is there a window where p+d gives watts and d+d stays below the neutron limit? |
| `notebooks/12_waste_burning_budget.ipynb` | Fission-waste burning: TRU burn rate per GWth-year, fleet size and time to clear the stock, ADS driver share (spallation vs μCF), neutrons for ⁹⁹Tc/¹²⁹I |
| `notebooks/13_depth_artifact_and_shape_fit.ipynb` | Can a near-surface deuterium excess fake keV screening in Karahadian et al.'s thick-target fit? Screening shape fitted to the data and its effect on Claim A |
| `notebooks/14_digitised_beam_data_fits.ipynb` | Fits to the digitised Karahadian et al. Fig. 2 (`data/karahadian2026_fig2.csv`, `tools/digitize_karahadian_fig2.py`): yield-model dependence of U_e, depth artifact under the published model, screening-shape windows |
| `notebooks/15_e1_pairing_loophole.ipynb` | Experiment E1 (5.49 MeV gamma search) against the preferential p–d pairing loophole at keV screening |
| `notebooks/16_muon_cost_targets.ipynb` | Beam energy per muon needed for net electricity, a power plant and beating spallation; beam-heat recovery; production efficiency vs the pion rest-mass floor |
| `notebooks/05_fuels_density_resonance.ipynb` | Other levers: all hydrogen-isotope fuel pairs (molecule and lattice; second solver validation on p+d and H₂/HD binding), p+d with screening in mixed H/D lattices, pycnonuclear density scan, resonant tunneling via exact transfer matrix, proposed experiments |
| `notebooks/06_status_and_experiments.ipynb` | Distance to goal under each assumption; closer/lighter compression scan for all fuels; three experiment designs with computed sensitivities (summary in [`EXPERIMENTS.md`](EXPERIMENTS.md)) |
| `notebooks/07_heat_only_channel.ipynb` | Upper bound on fusion energy going directly to lattice heat: required width vs neutron suppression, electromagnetic channels, multi-phonon energy-gap law, coherent many-nucleus coupling, causality |
| `notebooks/08_vacancy_clusters.ipynb` | Deuterium clusters (N = 2–6) in a Pd vacancy; pair held at fixed spacing and the energy cost |
| `notebooks/09_muon_catalysis_economics.ipynb` | Muon-catalyzed fusion energy balance, calibrated to measured data; levers to net electricity |
| `notebooks/10_muon_hybrid_blanket.ipynb` | μCF as a neutron source for a subcritical fission blanket, compared with spallation; tritium self-sufficiency |
| `notebooks/02_screening_anomaly.ipynb` | The electron-screening anomaly in deuterated metals: data, how U_e is extracted, a simulated depth-profile artifact, Debye vs Thomas–Fermi consistency checks, a heavy-electron bridge to cold-fusion rates, the 2025–26 results, proposed decisive experiments |

## Headline findings

- Thermal D+D in a Pd lattice needs an effective kT of about **65 eV** for 1 W/cm³. Pd atoms are knocked out of the lattice at 34 eV.
- Metal targets show screening energies of **~200–600 eV** against a theoretical **~25 eV**. The Debye model fits the numbers, but its Debye sphere holds ~3×10⁻⁵ electrons, so the model is used far outside its validity.
- A simple near-surface deuterium-excess artifact fakes only ~10–90 eV at plausible levels. Faking 300 eV needs a near-surface density **3–4.5× the bulk**.
- **If** the anomalous screening acted on deuterons at rest at molecular scale, it would be equivalent to an electron ~10× heavier, enough for ~1 W/cm³. That closes most of the 10^53 gap. It still needs a mechanism that binds pairs at ~0.07 Å, and nothing in the lattice does that.
- The 2026 sub-keV plateau claim (>10¹⁸) is impossible to reach by **any** screening above 0.58 keV c.m. It points to a different mechanism or an instrumental floor and needs replication.

- **Notebook 03:** the solver reproduces D₂ binding to 0.0004 eV and Koonin–Nauenberg's rate (2.5 vs 3 ×10⁻⁶⁴ s⁻¹). Watt-level rates need an electron ~9× heavier (notebook 02 guessed 10×).
- A deuteron pair at real PdD lattice spacing fuses at ~10⁻¹²⁴ s⁻¹, ~60 orders below a D₂ molecule. **The lattice is the bottleneck, not the screening strength.**
- If the beam-measured screening extended far enough at rest, it would bind deuterons into a new state 0.07–0.24 Å apart. Wherever that approaches watt-level rates, it would also exceed the 1990 neutron limit (<2×10⁻²⁶ s⁻¹) by ~15 orders. **So at rest the screening can't extend beyond ~0.13–0.16 Å** (for 300–575 eV). Only a heat-only, neutron-free channel escapes that bound.

- **Notebook 04:** across 40 variants, no model reaches watts before crossing the neutron limit. The four that reach 1 W/cm³ all cross the null limit at a shorter range first. **Watts imply neutrons for any screening-plus-confinement mechanism.** The allowed screening range at rest is 0.018–0.315 Å (median 0.137 Å) and is set mainly by the profile shape and the Thomas–Fermi length. Lattice stiffness, phonon energy and attempt frequency barely matter.

- **Notebook 05:** p+d is the fastest pair (+8 orders over d+d in a molecule, matching Koonin–Nauenberg; +17 in the lattice) and emits no neutrons. But even with the screening anomaly it peaks at ~10⁻¹²·³ s⁻¹, short of watts, and it emits 5.5 MeV gammas. d+t is *slower* than d+d at rest. Cold metallic deuterium reaches 1 W/cm³ only at ~1.6×10⁴ g/cm³ (~10⁵× PdD). Resonant tunneling adds nothing beyond the sequential kinetics already used. **Every lever that moves orders of magnitude does so by shrinking or lightening the pair.**

- **Notebook 06:** ~114 orders short with no new physics; ~15 at the most the neutron data allow; ~2.5 for the best (gamma-loud) p+d case. Every fuel except p+p reaches watts at a pair spacing of **~7–8 pm**, so closer is the lever and lighter only a modifier. Three experiments are designed in [`EXPERIMENTS.md`](EXPERIMENTS.md).

- **Notebook 07:** the heat-only channel is closed for any process through excited ⁴He. Even 10⁻³ neutron suppression needs a decay width larger than the 23.85 MeV transition energy. EM, multi-phonon and coherent routes fall short by ~11, ~10⁹ and ≥12 orders, and coherent transfer is causality-limited.
- **Notebook 08:** vacancy clusters push deuterons apart (2.8–3.8 Å). Holding a pair at the 7.3 pm watt spacing costs ~170 eV.
- **Notebook 09:** muon-catalyzed fusion is ~1.5× from scientific breakeven and ~9× from net electricity, the one gap of engineering size.

- **Notebook 10:** a subcritical blanket gives μCF net electricity with today's numbers, but today μCF yields ~30 neutrons per GeV, the same as spallation. It only beats existing accelerator-driven systems once muons cost ≲4–8 GeV or catalyse ≳100–175 fusions each.

- **Notebook 04b:** with keV screening and closer spacings (72 variants), 33 reach watts and all cross the neutron limit first (smallest margin 1.29× in range). The overall range bound is 0.003–0.31 Å; for keV screening with a long-tailed profile it collapses to the beam turning point.
- **Notebook 11:** energetic deuterons in metals return at most ~3×10⁻⁵ of their energy (4.5 orders below breakeven), with or without 1.7 keV screening. Hot fusion (NIF gain ~4) and muon catalysis are the paths with gaps of ~10× or less. Fission can't be made free of fission products; transmutation shortens the hazard to ~300 years.

- **Notebook 05b:** no p+d window in any of 24 variants up to 2 keV screening. Keeping coexisting d+d below the neutron limit leaves p+d at least 2.8 orders short of watts.
- **Notebook 12:** fissioning 0.394 t of transuranics gives 1 GWth-year. ~235 GWth of burners just keeps pace with today's LWR fleet, and a spallation driver costs ~17% of output at k = 0.95. μCF only helps once its levers are reached (3–6%).
- **Notebook 13:** under Karahadian et al.'s fitting procedure, no near-surface deuterium excess fakes more than 0.28–0.44 keV, so PdD still needs ≥1.15 keV of genuine enhancement. Fitting the screening shape to the data leaves Claim A unchanged.

- **Notebook 14:** the published model curves are thin-target ratios. A thick-target refit of the digitised points gives *higher* screening (PdD 1.86 keV, Pd 1.08 keV). Under the published model, no depth profile can fake any positive U_e.
- **Notebook 15:** a null E1 result closes the p–d pairing loophole for all keV screening variants, and a 30-day surface run suffices.
- **Notebook 16:** net electricity with today's cycle needs muons at ~0.6 GeV (9× cheaper). With the sticking and cycling levers, η 0.5/0.6 and beam-heat recovery, a ~2 GeV muon source reaches gain 1.37. As a neutron source, μCF already ties spallation.

## Verification, experiments, papers

- [`VERIFICATION.md`](VERIFICATION.md): status of every input (confirmed / secondary / unverified), a Pd U_e = 800 eV re-run, and the prior-work comparison (Leggett & Baym 1989; Czerski et al. 2006).
- [`EXPERIMENTS.md`](EXPERIMENTS.md): designs E1–E3.
- [`paper/`](paper/): preprint, **`cold_fusion_gap_preprint.docx`** (distribution copy), source, LaTeX and pre-submission checklist.
- [`notes/muon_hybrid/`](notes/muon_hybrid/): technical note **`muon_hybrid_note.docx`** on closing the muon-catalysed fusion gap.
- [`notes/other_paths/`](notes/other_paths/): technical note **`other_paths_note.docx`**: energetic deuterons in metals, ignition status, low-waste options.

## Tools

- `tools/claim_check.py`: check a claimed result against these bounds. Example:
  `python tools/claim_check.py --power 1 --metal Pd --mass 1 --loading 0.9 --fuel dd --neutrons 1`
  reports the implied rate per pair, its distance from standard physics, the pair spacing it requires (and the energy to hold it), the expected neutron/tritium/gamma output, and conflicts with the 1990 null limit and notebook 07.
- `tools/fetch.py`: polite literature fetching for source checks (official endpoints only, robots.txt, per-host spacing shared across processes, on-disk cache, request cap, logged). Set `CFG_CONTACT_EMAIL` to identify requests. Example: `python tools/fetch.py arxiv-pdf 1007.0322 --text`.
- `tests/`: `python -m pytest tests` (solver reproduces Koonin–Nauenberg; checker flags a 1 W d+d claim).

## Caveats

The literature check used web-search indexes. Google Scholar, PhilPapers, Crossref, arXiv and publisher sites couldn't be reached from the build environment. Each notebook ends with a source-status table that marks claims as confirmed, corrected, secondary or unverified.

## Run

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```
