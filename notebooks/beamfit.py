"""Thick-target d(d,p)t relative yields and screening enhancements (validated in notebook 13).

Energies are centre-of-mass keV. Yields are normalised to E_NORM = 6.5 keV as in Karahadian et al. (2026).
Stopping S ~ E^p; depth xi in units of the range at 6.5 keV.
"""
import numpy as np
from scipy import optimize
from cfsolve import PROFILES

E2, MU, HC, RN, B_G = 1440.0, 937.8e3, 197327.0, 5.0, 31.3970   # keV fm, keV, keV fm, fm, sqrt(keV)
E_NORM = 6.5

def f_shift(E, U):
    return np.exp(B_G/np.sqrt(E) - B_G/np.sqrt(E + U))

def sig(E, U=0.0):
    return np.exp(-B_G/np.sqrt(E))/E*f_shift(E, U)

def thick(E0, fenh=lambda E: 1.0, dens=lambda xi: 1.0, p=0.5):
    E = E0 - np.geomspace(1e-7*E0, E0 - 0.05, 6000)[::-1]
    xi = (E0**(1-p) - E**(1-p))/E_NORM**(1-p)
    return np.trapezoid(dens(xi)*np.exp(-B_G/np.sqrt(E))/E*fenh(E)/E**p, E)

def rel(Es, fenh=lambda E: 1.0, dens=lambda xi: 1.0, p=0.5):
    y = np.array([thick(e, fenh, dens, p) for e in list(Es) + [E_NORM]])
    return y[:-1]/y[-1]

def gamow(E, dV=None):
    V = lambda R: E2/R + (dV(R) if dV else 0.0)
    Rtp = optimize.brentq(lambda R: V(R) - E, RN, 1e8)
    R = np.geomspace(RN, Rtp, 4000)
    return 2*np.trapezoid(np.sqrt(2*MU*np.clip(V(R) - E, 0, None)), R)/HC

EG = np.geomspace(0.05, E_NORM, 70)
_G0 = None
def fenh_profile(dU, ell_fm, shape):
    """WKB enhancement exp(G_bare - G_screened) for V = e^2/R - dU g(R/ell), interpolated in log E."""
    global _G0
    if _G0 is None: _G0 = np.array([gamow(e) for e in EG])
    g = PROFILES[shape]
    lf = np.array([_G0[i] - gamow(e, lambda R: -dU*g(np.asarray(R)/ell_fm)) for i, e in enumerate(EG)])
    return lambda E: np.exp(np.interp(np.log(E), np.log(EG), lf))
