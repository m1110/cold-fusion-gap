"""Ground-state d-d fusion rates for a deuteron pair in an arbitrary radial potential.

Rate = A |psi(0)|^2 with A = S(0) c / (pi alpha mu c^2) (Coulomb-barrier-removed reactivity),
psi from a log-grid Numerov integration of the s-wave relative-motion equation.
Atomic units throughout (hbar = m_e = e = 1) unless a name says otherwise.
"""
import numpy as np
from scipy.interpolate import CubicSpline
try:
    from numba import njit
except ImportError:                       # pure-python fallback (slower)
    def njit(f=None, **kw):
        return f if f is not None else (lambda g: g)

HARTREE_EV = 27.211386
BOHR_CM    = 0.529177210903e-8
BOHR_A     = 0.529177210903
MD_ME      = 3670.48296788            # deuteron / electron mass
MU_DD      = MD_ME/2                  # d-d reduced mass (m_e)
E_UA       = -2.903724                # He ground state: united-atom limit of H2

# H2 Born-Oppenheimer total energies (hartree) vs R (bohr), as recalled from
# Kolos & Wolniewicz (1965). R=1.4 matches the modern value -1.1744759 (Pachucki 2010).
KW_R = np.array([0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 3.0, 4.0, 5.0, 6.0])
KW_E = np.array([-0.1202, -0.7696, -1.0200, -1.1245, -1.1649, -1.17447, -1.16858,
                 -1.15507, -1.13813, -1.10044, -1.05732, -1.01637, -1.00381, -1.00083])

def make_Eel(shift_short=0.0, c2_ua=None):
    """Electronic energy E_el(R) = E_BO(R) - 1/R, splined to the united-atom limit at R=0.
    shift_short adds a constant (hartree) for R <= 0.6 bohr; c2_ua sets the R^2 coefficient below 0.3."""
    Eel = KW_E - 1/KW_R + np.where(KW_R <= 0.6, shift_short, 0.0)
    if c2_ua is None:
        c2_ua = (Eel[0] - E_UA)/KW_R[0]**2
    Rpre = np.array([0.0, 0.1, 0.2, 0.3]); Rtail = np.array([8.0, 10.0, 15.0])
    Rs = np.concatenate([Rpre, KW_R, Rtail])
    Es = np.concatenate([E_UA + c2_ua*Rpre**2, Eel, -1 - 1/Rtail - 6.5/Rtail**6])
    return CubicSpline(Rs, Es, bc_type=((1, 0.0), 'not-a-knot'))

def V_molecule(mstar=1.0, Eel=None):
    """D2-like molecule with electron mass m*: V_m(R) = m* V_1(m* R)."""
    Eel = Eel if Eel is not None else make_Eel()
    return lambda R: mstar*(1/(mstar*R) + Eel(np.minimum(mstar*R, 15.0)))

def V_lattice(d0_A=2.75, phonon_meV=37.0, lam_TF_A=0.574):
    """Two deuterons in neighbouring lattice sites: Thomas-Fermi screened Coulomb repulsion plus
    an isotropic harmonic restoring force on the separation (each site at the PdD optical-phonon energy)."""
    d0 = d0_A/BOHR_A; w = phonon_meV*1e-3/HARTREE_EV; lam = lam_TF_A/BOHR_A
    return lambda R: np.exp(-R/lam)/R + 0.5*MU_DD*w**2*(R - d0)**2

def extra_screening(dU_eV, ell_A):
    """Additional screening near the pair: dV(R) = -dU exp(-R/ell)."""
    dU = dU_eV/HARTREE_EV; ell = ell_A/BOHR_A
    return lambda R: -dU*np.exp(-R/ell)

class Collapse(RuntimeError):
    pass

@njit(cache=True)
def _numerov(f, w0, w1):
    n = f.shape[0]
    w = np.empty(n); off = np.zeros(n)
    w[0] = w0; w[1] = w1; cur = 0.0
    for i in range(1, n-1):
        w[i+1] = ((12.0 - 10.0*f[i])*w[i] - f[i-1]*w[i-1])/f[i+1]
        off[i+1] = cur
        if abs(w[i+1]) > 1e100:
            w[i] *= 1e-100; w[i+1] *= 1e-100
            cur += 230.25850929940458; off[i] = cur; off[i+1] = cur
    return w, off

def solve(Vfun, Rmax, r0=1e-5, h=5e-5, tol=1e-13, Rmin_well=None):
    """Ground s-state of the d-d relative motion in Vfun(R).
    Returns dict: E (hartree), psi0sq (bohr^-3), rate (s^-1), r, u (normalized), V."""
    s = np.arange(np.log(r0), np.log(Rmax), h); r = np.exp(s); V = Vfun(r)
    a = 1/(2*MU_DD)                              # half the nuclear Bohr radius scale in u ~ r(1 + r/2a)
    u01 = r[:2]*(1 + r[:2]/(2*a)); w0, w1 = u01*np.exp(-s[:2]/2)

    def shoot(E):
        f = 1 - h*h*(r**2*2*MU_DD*(V - E) + 0.25)/12
        return _numerov(f, w0, w1)
    def nodes(E):
        w, _ = shoot(E)
        allowed = np.where(V < E)[0]
        if len(allowed) == 0: return 0
        j = allowed[-1]
        n = int(np.sum(w[1:j+1]*w[:j] < 0))
        tail = w[j:]
        return n + int(np.any(tail[1:]*tail[:-1] < 0))

    mask = r > (Rmin_well if Rmin_well is not None else 0.0)
    lo = V[mask].min()
    if nodes(lo) > 0:
        raise Collapse("bound state below the outer well: extra screening binds the pair at short range")
    hi = lo; step = max(1e-4, 0.01*(np.median(np.abs(V)) if np.isfinite(V).all() else 1))
    k = 0
    while nodes(hi) == 0:
        hi += step; step *= 1.5; k += 1
        if k > 200: raise RuntimeError("no bound state bracket")
    for _ in range(300):
        mid = 0.5*(lo + hi)
        if nodes(mid) == 0: lo = mid
        else: hi = mid
        if hi - lo < tol*max(1.0, abs(mid)): break
    E = 0.5*(lo + hi)
    w, off = shoot(E)
    logu = np.log(np.abs(w) + 1e-300) + off + s/2
    jpk = int(np.argmax(np.where(V < E, logu, -np.inf)))
    outer = np.where((r > r[jpk]) & (V > E))[0]
    j = outer[0] + int(np.argmin(logu[outer[0]:])) if len(outer) else len(r)
    ref = logu[jpk]
    u = np.sign(w[:j])*np.exp(logu[:j] - ref); rr = r[:j]
    norm = np.trapezoid(u**2, rr)
    lpsi0 = (logu[0] - ref) - np.log(rr[0]) - np.log(1 + rr[0]/(2*a)) - 0.5*np.log(4*np.pi*norm)
    psi0sq = np.exp(2*lpsi0)
    return dict(E=E, psi0sq=psi0sq, log10_rate=np.log10(A_cm3s()) + 2*lpsi0/np.log(10) - 3*np.log10(BOHR_CM),
                r=rr, u=u/np.sqrt(norm), V=V[:j])

S_KEVB = 53.701 + 55.576      # Bosch-Hale S(0) for both D+D branches, keV*barn
def A_cm3s(S_keVb=S_KEVB):
    alpha = 1/137.035999; c = 2.99792458e10; mu_c2_keV = MU_DD*510.99895
    return S_keVb*1e-24*c/(np.pi*alpha*mu_c2_keV)
