# Proposed experiments

Designs and sensitivity calculations are in [`notebooks/06_status_and_experiments.ipynb`](notebooks/06_status_and_experiments.ipynb). Detector backgrounds, efficiencies and beam parameters are **stated assumptions**: replace them with real hardware numbers and re-run.

## Where things stand

| Assumption | Orders of magnitude short of 1 W/cm³ |
|---|---|
| d+d where deuterons actually sit in PdD, no new physics | **~114** |
| d+d in a D₂ molecule (Koonin–Nauenberg) | ~53 |
| d+d with measured screening, at the most the 1990 neutron limit allows | **~15** |
| p+d with measured screening, best case (50/50 H/D) | ~2.5, but it would emit ~10¹² gammas/s per watt |

**What any mechanism must achieve:** hold hydrogen-isotope pairs at **≤ 7–8 pm** (0.07–0.08 Å) at rest. That's ~9–10× tighter than a D₂ molecule and ~35× tighter than the PdD lattice. Every fuel except p+p converges there. Lighter fuels help only at long range.

## E1: Gamma search for p+d fusion at rest in H/D co-loaded Pd

- **Question:** does the beam-measured screening act on resting pairs far enough out to matter? p+d → ³He + 5.49 MeV γ has no neutron branch, so the 1990 neutron searches never tested it.
- **Setup:** 10 g Pd foil co-loaded with H and D (0.45/0.45), resistance-monitored, with steady and cycled loading. HPGe/LaBr₃ detector with shield and muon veto, run at the surface and underground. Efficiency calibrated with the p+d reaction on an accelerator.
- **Controls:** H-only, D-only (with ³He neutron counters), unloaded Pd, empty cell.
- **Sensitivity (30 days, assumed backgrounds):** about 1×10⁻²⁶ per p–d pair per s at the surface and **4×10⁻²⁸ underground**, ~50× below the 1990 d+d neutron limit. Excludes screening ranges ≳0.12–0.16 Å at rest for 300–575 eV screening.
- **Update for keV screening (notebook 15):** at 0.9–2.0 keV screening, E1 excludes ranges 1.25–1.97× shorter than any at which even a fully p–d-paired lattice would reach watts (all 14 variants with such a region). A null result therefore closes the preferential-pairing loophole of notebook 05b. Underground adds little at keV screening, so a 30-day **surface** run suffices.
- **Decision:** a 5.49 MeV line that scales as x_H·x_D and is absent in the controls means p+d fusion at rest, and its rate measures the screening range. No line extends the neutron-based bound to a neutron-free channel.

## E2: Beam screening in a deuterium-implanted heavy-fermion compound, with a temperature switch

- **Question:** is the screening anomaly a heavy-electron effect?
- **Setup:** a Ce- or Yb-based heavy-fermion target (e.g. CeCu₆, YbAl₃) with a non-f-electron analogue (LaCu₆, LuAl₃) as the control. Deuterium implanted by the beam itself, with the profile tracked in situ by ERDA. d(d,p)t at E_d = 5–30 keV; target cycled between 4 K (heavy-fermion state on) and 300 K (off).
- **Sensitivity:** ~6 h per point for 5% statistics at 10 μA. A heavy-electron effect (U_e ≳ 3 keV gives f ≳ 19 at 5 keV) would show within minutes.
- **Decision:** a ≫10× jump below the coherence temperature, only in the heavy-fermion target, supports heavy-electron screening. Equal results in both targets rule it out.

## E3: p+d and d+d screening on the same target, in the same run

- **Question:** is the anomaly real electron screening (same U_e for both), a depth-profile artifact (depends on where projectiles stop), or a d+d-specific nuclear resonance (U_e larger for d+d)?
- **Setup:** one deuterated Zr or Ta target. Alternating H⁺ and D⁺ beams matched in stopping range. LaBr₃ for the p+d γ, Si detectors for d(d,p)t, ERDA monitoring.
- **Statistics are the hard part:** 5% points give only 2.7σ separation. A 5σ answer needs ~2.6% p+d points: **~15 days per energy point at 100 μA, ~1.5 days at 1 mA.**
- **Decision:** U_dd ≈ U_pd means real screening. U_dd > U_pd means a nuclear effect specific to d+d. Results that track range-matching mean an artifact.

## Order

E2 is the fastest to a clear answer. E3 says what the anomaly *is*, but needs a high-current proton source. E1 is the most direct test of a cold-fusion-relevant effect at rest.
