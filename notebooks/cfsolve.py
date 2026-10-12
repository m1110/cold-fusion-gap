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

# H2 Born-Oppenheimer total energies (hartree) vs R (bohr): Pachucki, Phys. Rev. A 82, 032509 (2010),
# arXiv:1007.0322, Table IV (verified from the primary source; agrees with Kolos & Wolniewicz 1965 to 1e-4 Ha).
KW_R = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.25, 1.3, 1.32, 1.34, 1.36, 1.38, 1.39, 1.4, 1.41, 1.42, 1.44, 1.46, 1.48, 1.5, 1.55, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 13, 14, 15, 16, 17, 18, 19, 20])
KW_E = np.array([7.127216731132, 2.197803295226, 0.619241659796, -0.120230341179, -0.526638758743, -0.769635429486, -0.922027461527, -1.020056666361, -1.083643239959, -1.124539719547, -1.150057367739, -1.164935243440, -1.169419627391, -1.172347149038, -1.173138736333, -1.173734874958, -1.174148498570, -1.174391683632, -1.174452917278, -1.174475714220, -1.174461370871, -1.174411141239, -1.174207836585, -1.173875042749, -1.173421418292, -1.172855079579, -1.170994919897, -1.168583373371, -1.162458726898, -1.155068737612, -1.146850697030, -1.138132957133, -1.129163836101, -1.120132116849, -1.111181765204, -1.102422606011, -1.093938129956, -1.085791237396, -1.078028484184, -1.070683233481, -1.063778008806, -1.057326268873, -1.051333772268, -1.045799661432, -1.040717365351, -1.036075395191, -1.031858084855, -1.028046308380, -1.024618188411, -1.021549795534, -1.018815827696, -1.016390252951, -1.012359959683, -1.009256516262, -1.006895223823, -1.005116006100, -1.003785658584, -1.002796816311, -1.002065057210, -1.001525251887, -1.001127880852, -1.000835707655, -1.000400548535, -1.000197914480, -1.000102106148, -1.000055604973, -1.000032171833, -1.000019781832, -1.000012856877, -1.000008755746, -1.000006189995, -1.000004505989, -1.000003356175, -1.000002545970, -1.000001529287, -1.000000960681, -1.000000625454, -1.000000419586, -1.000000288826, -1.000000203341, -1.000000146028, -1.000000106740])

def make_Eel(shift_short=0.0, c2_ua=None):
    """Electronic energy E_el(R) = E_BO(R) - 1/R, splined to the united-atom limit at R=0.
    shift_short adds a constant (hartree) for R <= 0.6 bohr; c2_ua sets the R^2 coefficient below 0.3."""
    Eel = KW_E - 1/KW_R + np.where(KW_R <= 0.6, shift_short, 0.0)
    if c2_ua is None:
        c2_ua = (Eel[0] - E_UA)/KW_R[0]**2
    Rpre = np.array([0.0, 0.05])
    Rs = np.concatenate([Rpre, KW_R])
    Es = np.concatenate([E_UA + c2_ua*Rpre**2, Eel])
    return CubicSpline(Rs, Es, bc_type=((1, 0.0), 'not-a-knot'))

def V_molecule(mstar=1.0, Eel=None):
    """D2-like molecule with electron mass m*: V_m(R) = m* V_1(m* R)."""
    Eel = Eel if Eel is not None else make_Eel()
    return lambda R: mstar*(1/(mstar*R) + Eel(np.minimum(mstar*R, 20.0)))

def V_lattice(d0_A=2.75, phonon_meV=37.0, lam_TF_A=0.574, confinement="harmonic", barrier_eV=0.23):
    """Two deuterons in neighbouring lattice sites: Thomas-Fermi screened Coulomb repulsion plus a
    restoring force on the separation set by the PdD optical-phonon energy.
    confinement="harmonic": grows without bound; "capped": the same curvature near d0 but levels off
    at barrier_eV (the site-to-site diffusion barrier), i.e. the lattice stops resisting beyond the saddle."""
    d0 = d0_A/BOHR_A; w = phonon_meV*1e-3/HARTREE_EV; lam = lam_TF_A/BOHR_A
    k = MU_DD*w**2
    if confinement == "harmonic":
        return lambda R: np.exp(-R/lam)/R + 0.5*k*(R - d0)**2
    Eb = barrier_eV/HARTREE_EV
    return lambda R: np.exp(-R/lam)/R + Eb*np.tanh(0.5*k*(R - d0)**2/Eb)

PROFILES = {
    "exponential": lambda x: np.exp(-x),
    "gaussian":    lambda x: np.exp(-x**2),
    "step":        lambda x: 1/(1 + np.exp(np.clip((x - 1)/0.1, -700, 700))),
    "yukawa":      lambda x: -np.expm1(-x)/np.where(x > 0, x, 1e-300),   # (1-e^-x)/x: long-range -q/R tail
}

MASS_ME = {"p": 1836.15267343, "d": MD_ME, "t": 5496.92153573}

def reduced_mass(a, b):
    return MASS_ME[a]*MASS_ME[b]/(MASS_ME[a] + MASS_ME[b])

def V_lattice_pair(a="d", b="d", d0_A=2.75, phonon_meV=None, lam_TF_A=0.574):
    """Lattice pair of two hydrogen isotopes in neighbouring sites. Each site has its own force constant
    k_i = m_i w_i^2 (w_i: that isotope's optical-phonon energy); the relative-coordinate stiffness keeps the
    R^2 part of 1/2 k1 x1^2 + 1/2 k2 x2^2 (centre-of-mass cross term dropped)."""
    ph = {"p": 69.0, "d": 37.0, "t": 37.0*np.sqrt(MD_ME/MASS_ME["t"])}
    if phonon_meV: ph.update(phonon_meV)
    m1, m2 = MASS_ME[a], MASS_ME[b]; M = m1 + m2
    k1 = m1*(ph[a]*1e-3/HARTREE_EV)**2; k2 = m2*(ph[b]*1e-3/HARTREE_EV)**2
    krel = (k1*m2**2 + k2*m1**2)/M**2
    d0 = d0_A/BOHR_A; lam = lam_TF_A/BOHR_A
    return lambda R: np.exp(-R/lam)/R + 0.5*krel*(R - d0)**2

def extra_screening(dU_eV, ell_A, shape="exponential"):
    """Additional screening near the pair: dV(R) = -dU g(R/ell), g(0)=1."""
    dU = dU_eV/HARTREE_EV; ell = ell_A/BOHR_A; g = PROFILES[shape]
    return lambda R: -dU*g(R/ell)

def beam_matched_dU(U_meas_eV, ell_A, shape="exponential", R_tp_A=0.004):
    """Contact strength needed for the profile to equal U_meas at the beam turning point."""
    return U_meas_eV/PROFILES[shape](np.array(R_tp_A/ell_A))

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

def solve(Vfun, Rmax, r0=1e-5, h=5e-5, tol=1e-13, Rmin_well=None, mu=None, S_keVb=None):
    """Ground s-state of the d-d relative motion in Vfun(R).
    Returns dict: E (hartree), psi0sq (bohr^-3), rate (s^-1), r, u (normalized), V."""
    MU = MU_DD if mu is None else mu
    s = np.arange(np.log(r0), np.log(Rmax), h); r = np.exp(s); V = Vfun(r)
    a = 1/(2*MU)                              # half the nuclear Bohr radius scale in u ~ r(1 + r/2a)
    u01 = r[:2]*(1 + r[:2]/(2*a)); w0, w1 = u01*np.exp(-s[:2]/2)

    def shoot(E):
        f = 1 - h*h*(r**2*2*MU*(V - E) + 0.25)/12
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
    return dict(E=E, psi0sq=psi0sq, log10_rate=np.log10(A_cm3s(S_keVb if S_keVb is not None else S_KEVB, MU)) + 2*lpsi0/np.log(10) - 3*np.log10(BOHR_CM),
                r=rr, u=u/np.sqrt(norm), V=V[:j])

S_KEVB = 53.701 + 55.576      # Bosch-Hale S(0) for both D+D branches, keV*barn
def A_cm3s(S_keVb=S_KEVB, mu=MU_DD):
    alpha = 1/137.035999; c = 2.99792458e10; mu_c2_keV = mu*510.99895
    return S_keVb*1e-24*c/(np.pi*alpha*mu_c2_keV)
