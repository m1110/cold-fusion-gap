#!/usr/bin/env python3
"""Polite, cached fetching of literature for source verification.

Rules it enforces:
  * official endpoints only (arXiv, PubMed/NCBI E-utilities, Crossref, OpenAlex, OSTI, INSPIRE, Semantic Scholar);
    Google Scholar and PhilPapers are refused (their terms forbid automated access);
  * robots.txt is honoured;
  * at most one request per host every few seconds (arXiv asks for >= 3 s), with retry/backoff on 429/503
    that honours Retry-After;
  * every response is cached on disk, so a URL is fetched once per machine;
  * a per-run request cap (default 30);
  * a descriptive User-Agent with a contact email (env CFG_CONTACT_EMAIL), which also puts Crossref and
    OpenAlex requests in their "polite pool";
  * every request is logged to .cache/fetch/log.csv.

Usage:
  CFG_CONTACT_EMAIL=you@example.org python tools/fetch.py arxiv 1007.0322          # abstract page
  python tools/fetch.py arxiv-pdf 1007.0322 [--text]                                # PDF (optionally text via pdftotext)
  python tools/fetch.py doi 10.1103/PhysRevLett.65.1196                             # Crossref metadata
  python tools/fetch.py openalex "Kolos Wolniewicz 1965 hydrogen molecule"          # search
  python tools/fetch.py pubmed 10042199                                             # PubMed record
  python tools/fetch.py url https://...                                             # any allowed host
"""
import csv, fcntl, hashlib, json, os, subprocess, sys, time, urllib.parse, urllib.request, urllib.robotparser
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache", "fetch")
ALLOWED = {
    "arxiv.org": 3.0, "export.arxiv.org": 3.0,
    "pubmed.ncbi.nlm.nih.gov": 3.0, "eutils.ncbi.nlm.nih.gov": 0.5,
    "api.crossref.org": 1.0, "api.openalex.org": 1.0,
    "www.osti.gov": 3.0, "inspirehep.net": 3.0, "api.semanticscholar.org": 3.0,
}
REFUSED = {"scholar.google.com": "Google Scholar forbids automated access; use OpenAlex or Semantic Scholar",
           "philpapers.org": "PhilPapers restricts automated access; search manually"}
MAX_REQUESTS = int(os.environ.get("CFG_MAX_REQUESTS", "30"))
CONTACT = os.environ.get("CFG_CONTACT_EMAIL", "")
UA = f"cold-fusion-gap-verification/1.0 (research source checks; https://github.com/m1110/cold-fusion-gap" + \
     (f"; mailto:{CONTACT})" if CONTACT else ")")

_count = 0


def _wait_turn(host):
    """Per-host spacing shared across processes: a locked JSON file of last-request times."""
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, "last_request.json"), "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        try:
            last = json.loads(f.read() or "{}")
        except ValueError:
            last = {}
        wait = ALLOWED[host] - (time.time() - last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        last[host] = time.time()
        f.seek(0); f.truncate(); f.write(json.dumps(last))
        fcntl.flock(f, fcntl.LOCK_UN)
_robots = {}


def _log(url, status, cached):
    os.makedirs(ROOT, exist_ok=True)
    new = not os.path.exists(os.path.join(ROOT, "log.csv"))
    with open(os.path.join(ROOT, "log.csv"), "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["utc", "url", "status", "cached"])
        w.writerow([datetime.now(timezone.utc).isoformat(timespec="seconds"), url, status, cached])


def _robots_ok(url):
    p = urllib.parse.urlparse(url)
    if p.netloc not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            req = urllib.request.Request(f"{p.scheme}://{p.netloc}/robots.txt", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                rp.parse(r.read().decode("utf-8", "replace").splitlines())
        except Exception:
            rp = None                       # no robots.txt reachable: fall back to rate limiting only
        _robots[p.netloc] = rp
    rp = _robots[p.netloc]
    return True if rp is None else rp.can_fetch(UA, url)


def fetch(url, binary=False):
    """Return the body of url (bytes if binary else str), from cache when available."""
    global _count
    host = urllib.parse.urlparse(url).netloc
    if host in REFUSED:
        raise SystemExit(f"refused: {host}: {REFUSED[host]}")
    if host not in ALLOWED:
        raise SystemExit(f"refused: {host} is not an official literature endpoint in ALLOWED")
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    path = os.path.join(ROOT, key)
    if os.path.exists(path):
        _log(url, "cache", True)
        data = open(path, "rb").read()
        return data if binary else data.decode("utf-8", "replace")
    if _count >= MAX_REQUESTS:
        raise SystemExit(f"request cap reached ({MAX_REQUESTS}); raise CFG_MAX_REQUESTS deliberately if needed")
    if not _robots_ok(url):
        raise SystemExit(f"robots.txt disallows {url}")
    for attempt in range(4):
        _wait_turn(host); _count += 1
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            os.makedirs(ROOT, exist_ok=True)
            open(path, "wb").write(data)
            _log(url, 200, False)
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            _log(url, e.code, False)
            if e.code in (429, 503) and attempt < 3:
                time.sleep(float(e.headers.get("Retry-After", 10*(attempt + 1))))
                continue
            raise SystemExit(f"HTTP {e.code} for {url}")
        except urllib.error.URLError as e:
            _log(url, f"error: {e.reason}", False)
            raise SystemExit(f"cannot reach {host}: {e.reason} (is it allowed in the environment's network settings?)")


def main():
    if len(sys.argv) < 3:
        print(__doc__); return
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == "arxiv":
        print(fetch(f"https://arxiv.org/abs/{arg}"))
    elif cmd == "arxiv-pdf":
        data = fetch(f"https://arxiv.org/pdf/{arg}", binary=True)
        out = os.path.join(ROOT, f"arxiv_{arg.replace('/', '_')}.pdf"); open(out, "wb").write(data)
        if "--text" in sys.argv:
            print(subprocess.run(["pdftotext", "-layout", out, "-"], capture_output=True, text=True).stdout)
        else:
            print(out)
    elif cmd == "doi":
        mail = f"?mailto={urllib.parse.quote(CONTACT)}" if CONTACT else ""
        print(json.dumps(json.loads(fetch(f"https://api.crossref.org/works/{urllib.parse.quote(arg)}{mail}"))["message"], indent=1)[:4000])
    elif cmd == "openalex":
        q = urllib.parse.urlencode({"search": arg, "per-page": 5, **({"mailto": CONTACT} if CONTACT else {})})
        for w in json.loads(fetch(f"https://api.openalex.org/works?{q}"))["results"]:
            print(w.get("publication_year"), "|", w.get("display_name"), "|", w.get("doi"))
    elif cmd == "pubmed":
        print(fetch(f"https://pubmed.ncbi.nlm.nih.gov/{arg}/"))
    elif cmd == "url":
        print(fetch(arg))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
