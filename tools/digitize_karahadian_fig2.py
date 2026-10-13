"""Digitise Fig. 2 of Karahadian et al., Nat. Commun. 17, 8845 (2026), arXiv:2512.06212.

The figure is embedded as a 6720x5040 raster with an alpha mask. We composite it on white, calibrate
the axes from the plot frame (x: 0-6.5 keV, linear; y: 1e-4 to 1, log), and locate each square marker
and its error-bar caps by exact colour at the nominal beam energies. Output: data/karahadian2026_fig2.csv.
This is a digitisation of a published figure, not the authors' tabulated data. Usage:
    python tools/digitize_karahadian_fig2.py <path to arxiv_2512.06212.pdf> <workdir>
"""
import csv, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

X0, X1, Y0, Y1 = 804, 6451, 171, 4426            # frame: x = 0 and 6.5 keV; y = 1 and 1e-4
E_NOM = [0.25, 0.5] + [1.0 + 0.5*i for i in range(12)]
SERIES = {  # panel image, alpha mask, label, RGB
    "PdD": ("img-000.png", "img-001.png", (139, 0, 0)),
    "Pd":  ("img-000.png", "img-001.png", (105, 105, 105)),
    "TiD": ("img-002.png", "img-003.png", (0, 0, 128)),
    "Ti":  ("img-002.png", "img-003.png", (128, 128, 128)),
}
xpix = lambda E: X0 + E/6.5*(X1 - X0)
yval = lambda py: 10**(-4*(py - Y0)/(Y1 - Y0))

def composite(work, a, b):
    rgb = np.asarray(Image.open(work/a).convert("RGB")).astype(float)
    al = np.asarray(Image.open(work/b)).astype(float)[..., None]/255
    return (rgb*al + 255*(1 - al)).astype(int)

def find(img, col, E, half=80, tol=6):
    """Marker = block of >=60 rows at least 95 px wide (squares are 101 px; the curve adds <=50 px).
    Error-bar ends = centres of the cap blocks (5-25 rows, >=95 px wide) nearest above and below."""
    xc = int(round(xpix(E)))
    m = (np.abs(img[:, xc-half:xc+half] - np.array(col)).max(2) <= tol)
    m[:Y0+5] = False; m[Y1-5:] = False
    if E == 3.5:                                   # the legend markers sit in this column above y = 0.25
        m[:int(Y0 + (Y1 - Y0)*np.log10(1/0.25)/4)] = False
    rows = np.where(m.sum(1) >= 95)[0]
    if len(rows) == 0: return None
    blocks = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
    marks = [b for b in blocks if len(b) >= 60]
    if not marks: return None
    blk = max(marks, key=len)
    yc = 0.5*(blk[0] + blk[-1]); n = len(blk)
    caps = [b for b in blocks if 5 <= len(b) <= 25]
    above = [0.5*(b[0] + b[-1]) for b in caps if b[-1] < blk[0]]
    below = [0.5*(b[0] + b[-1]) for b in caps if b[0] > blk[-1]]
    top = max(above) if above else blk[0]; bot = min(below) if below else blk[-1]
    cols = np.where(m[blk].sum(0) > 0.5*n)[0]
    xm = xc - half + 0.5*(cols[0] + cols[-1])
    flag = "ok" if 95 <= n <= 108 else ("occluded" if n < 95 else "merged")
    return dict(E_nom=E, E_fig=(xm - X0)/(X1 - X0)*6.5, y=yval(yc), y_hi=yval(top), y_lo=yval(bot),
                marker_px=n, flag=flag, caps=f"{'U' if above else '-'}{'L' if below else '-'}", px=(xm, yc, top, bot))

def main(pdf, work):
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdfimages", "-png", "-f", "4", "-l", "4", pdf, str(work/"img")], check=True)
    out, overlays = [], {}
    for name, (a, b, col) in SERIES.items():
        img = composite(work, a, b); overlays.setdefault(a, img.copy())
        for E in E_NOM:
            r = find(img, col, E)
            if r is None: continue
            out.append(dict(sample=name, **{k: v for k, v in r.items() if k != "px"}))
            xm, yc, top, bot = map(int, r["px"]); ov = overlays[a]
            ov[top:bot, xm-2:xm+3] = (0, 200, 0); ov[int(yc)-3:int(yc)+4, xm-60:xm+61] = (0, 200, 0)
    for a, ov in overlays.items():
        Image.fromarray(ov.astype(np.uint8)).resize((1120, 840)).save(work/f"overlay_{a}")
    dst = Path(__file__).resolve().parents[1]/"data"/"karahadian2026_fig2.csv"
    with open(dst, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample", "E_cm_keV_nominal", "E_cm_keV_from_figure", "rel_yield", "rel_yield_upper", "rel_yield_lower", "marker_flag", "caps_found"])
        for r in out:
            w.writerow([r["sample"], r["E_nom"], f"{r['E_fig']:.3f}", f"{r['y']:.4g}", f"{r['y_hi']:.4g}", f"{r['y_lo']:.4g}", r["flag"], r["caps"]])
    print(f"wrote {len(out)} points to {dst}")
    for r in out:
        print(f"{r['sample']:4s} E={r['E_nom']:4.2f} (fig {r['E_fig']:.2f})  y={r['y']:.3e}  [{r['y_lo']:.2e}, {r['y_hi']:.2e}]  marker {r['marker_px']} px {r['flag']} caps {r['caps']}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
