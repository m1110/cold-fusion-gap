# Preprint draft

- **`cold_fusion_gap_preprint.docx`: the distribution copy (Word).**
- `draft.md`: editable source (Markdown with LaTeX math).
- `build.sh`: rebuilds the .docx (math converted to portable text via `tex2unicode.py`) and `main.tex` (LaTeX, for arXiv; compile with `pdflatex main.tex`).

## Before submission (in order)

1. **Primary-source checks** (VERIFICATION.md lists each). Done: H₂ potential (now Pachucki 2010, primary), Pd U_e values, 2025 recalculation. Remaining: Bosch–Hale d+t coefficients and erratum, Pd U_e (250 vs 800 eV), t+t S-factor, Zhou 2006 branching, ⁴He level widths.
2. **Read Leggett & Baym (1989) and Czerski, Heide & Huke (2006) in full.** Decide what is actually new and adjust §5 and the abstract.
3. **Expert review**: a nuclear-reaction theorist (screening/S-factors) and a condensed-matter theorist (lattice model, heat-only section).
4. Replace the assumption-level numbers in E1–E3 with quotes from real detectors and beams, ideally after contact with the groups in EXPERIMENTS.md.
5. Choose arXiv category (nucl-th, cross-list cond-mat.mtrl-sci) and find an endorser if needed.
6. Add author names and affiliations, and figures (from `../figures/`: 03_along_band, 04_range_bound, 06_closer_lighter, 07_required_width).
