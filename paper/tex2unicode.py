#!/usr/bin/env python3
"""Convert the $...$ math in draft.md to plain Unicode text so the Word version reads the same in every viewer
(Word, Google Docs, LibreOffice, previews). The LaTeX build keeps the original math."""
import re, sys

SUP = str.maketrans("0123456789+-=()n.", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ·")
SUB = str.maketrans("0123456789+-=()aehklmnoprstux", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕₖₗₘₙₒₚᵣₛₜᵤₓ")
SYMS = {r"\times": "×", r"\approx": " ≈ ", r"\simeq": "≃", r"\sim": "∼", r"\le": "≤", r"\ge": "≥", r"\lesssim": " ≲ ",
        r"\gtrsim": " ≳ ", r"\pm": "±", r"\to": "→", r"\Gamma": "Γ", r"\Delta": "Δ", r"\psi": "ψ", r"\pi": "π",
        r"\alpha": "α", r"\mu": "μ", r"\ell": "ℓ", r"\gamma": "γ", r"\varphi": "φ", r"\omega": "ω", r"\lambda": "λ",
        r"\,": " ", r"\;": " ", r"\quad": "   ", r"\qquad": "    ", r"\cdot": "·", r"\infty": "∞", r"\%": "%"}

def script(body, table):
    t = body.translate(table)
    return t if all(ch not in body for ch in "abcdfgijqvwyzABCDEFGHIJKLMNOPQRSTUVWXYZ") or table is SUP and body.translate(table) != body and re.fullmatch(r"[0-9+\-=().n]+", body) else None

def conv(tex):
    s = tex
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", s)
    for k in sorted(SYMS, key=len, reverse=True):
        s = s.replace(k, SYMS[k])
    esc = lambda b: b.replace("\\", "").replace("{", "").replace("}", "").replace(" ", "\\ ").replace("*", "\\*")
    def sup(m):
        b = m.group(1) or m.group(2)
        if re.fullmatch(r"[0-9+\-=().n]+", b): return b.translate(SUP)
        return "^" + esc(b) + "^"
    def sub(m):
        b = m.group(1) or m.group(2)
        if re.fullmatch(r"[0-9+\-=()]+", b): return b.translate(SUB)
        return "~" + esc(b) + "~"
    s = re.sub(r"\\rm\s*", "", s)
    s = re.sub(r"_\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|_(\S)", lambda m: sub(m) if "^" not in (m.group(1) or "") else "~" + esc(re.sub(r"\^\{?([^}]*)\}?", r"\1", m.group(1))) + "~", s)
    s = re.sub(r"\^\{([^}]*)\}|\^(\S)", sup, s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\\(?![ *])", "", s)
    return s

text = open(sys.argv[1]).read()
text = re.sub(r"\$\$(.+?)\$\$", lambda m: "\n\n" + conv(m.group(1)).strip() + "\n\n", text, flags=re.S)
text = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", lambda m: conv(m.group(1)), text)
sys.stdout.write(text)
