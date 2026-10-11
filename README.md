# cold-fusion-gap

Quantitative notebooks asking one question: **how far is known physics from cold fusion, and where could something be missing?**

| Notebook | What it does |
|---|---|
| `notebooks/01_rate_gap.ipynb` | Rate gap (~10^52–53), required effective temperature (65 eV, from a numerical Gamow integral validated against Bosch–Hale to 1–2%), coherence scaling limits, exit-channel constraint, muon catalysis balance, literature check |
| `notebooks/03_bridge_and_bounds.ipynb` | Quantum solver for the d–d pair's ground state (`cfsolve.py`), validated against D₂ binding/zero-point energy and Koonin–Nauenberg; exact heavy-electron scan; lattice-pair model; extra-screening map bounded by beam data and 1990 neutron limits |
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

## Caveats

The literature check used web-search indexes. Google Scholar, PhilPapers, Crossref, arXiv and publisher sites couldn't be reached from the build environment. Each notebook ends with a source-status table that marks claims as confirmed, corrected, secondary or unverified.

## Run

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```
