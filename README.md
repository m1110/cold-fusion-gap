# cold-fusion-gap

Quantitative notebooks asking one question: **how far is known physics from cold fusion, and where could something be missing?**

| Notebook | What it does |
|---|---|
| `notebooks/01_rate_gap.ipynb` | Rate gap (~10^52–53), required effective temperature (65 eV, from a numerical Gamow integral validated against Bosch–Hale to 1–2%), coherence scaling limits, exit-channel constraint, muon catalysis balance, literature check |
| `notebooks/02_screening_anomaly.ipynb` | The electron-screening anomaly in deuterated metals: data, how U_e is extracted, a simulated depth-profile artifact, Debye vs Thomas–Fermi consistency checks, a heavy-electron bridge to cold-fusion rates, the 2025–26 results, proposed decisive experiments |

## Headline findings

- Thermal D+D in a Pd lattice needs an effective kT of about **65 eV** for 1 W/cm³. Pd atoms are knocked out of the lattice at 34 eV.
- Metal targets show screening energies of **~200–600 eV** against a theoretical **~25 eV**. The Debye model fits the numbers, but its Debye sphere holds ~3×10⁻⁵ electrons, so the model is used far outside its validity.
- A simple near-surface deuterium-excess artifact fakes only ~10–90 eV at plausible levels. Faking 300 eV needs a near-surface density **3–4.5× the bulk**.
- **If** the anomalous screening acted on deuterons at rest at molecular scale, it would be equivalent to an electron ~10× heavier, enough for ~1 W/cm³. That closes most of the 10^53 gap. It still needs a mechanism that binds pairs at ~0.07 Å, and nothing in the lattice does that.
- The 2026 sub-keV plateau claim (>10¹⁸) is impossible to reach by **any** screening above 0.58 keV c.m. It points to a different mechanism or an instrumental floor and needs replication.

## Caveats

The literature check used web-search indexes. Google Scholar, PhilPapers, Crossref, arXiv and publisher sites couldn't be reached from the build environment. Each notebook ends with a source-status table that marks claims as confirmed, corrected, secondary or unverified.

## Run

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```
