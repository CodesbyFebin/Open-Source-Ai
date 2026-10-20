"""Validate catalog/ data. Exit 1 on any error; warnings do not fail."""
import json, glob, os, sys, subprocess, datetime, collections

SPDX = {"MIT", "Apache-2.0", "AGPL-3.0", "GPL-3.0", "GPL-2.0", "LGPL-3.0", "BSD-2-Clause", "BSD-3-Clause", "MPL-2.0",
        "BUSL-1.1", "Elastic-2.0", "FSL-1.1-Apache-2.0", "FSL-1.1-MIT", "CC-BY-4.0", "ISC", "Unlicense"}


def parse_date(s):
    """Accept YYYY-MM-DD or ISO-8601 UTC timestamp ending in Z. Return date or None."""
    try:
        if len(s) == 10: return datetime.date.fromisoformat(s)
        if not s.endswith("Z"): return None
        return datetime.datetime.fromisoformat(s[:-1] + "+00:00").date()
    except (ValueError, TypeError):
        return None


def check(doc, cats, evidence, today, schema=None, gitlinks=0, has_gitmodules=False, recipes=()):
    err, warn = [], []
    if schema is not None:
        import jsonschema
        for e in jsonschema.Draft202012Validator(schema).iter_errors(doc):
            err.append(f"schema: {e.message} at {list(e.absolute_path)}")
        if err: return err, warn
    P = doc["projects"]; ids = {p["id"] for p in P}
    for key in ("id", "repo"):
        for v, n in collections.Counter(p[key].lower().rstrip("/") for p in P).items():
            if n > 1: err.append(f"duplicate {key}: {v}")
    for c, n in collections.Counter(cats).items():
        if n > 1: err.append(f"duplicate category {c}")
    lo = datetime.date(2024, 1, 1)
    hi = today + datetime.timedelta(days=1)  # curators may write dates in UTC+14 .. UTC-12
    bootstrap = not evidence
    if bootstrap: warn.append("no evidence collected yet (bootstrap)")
    for p in P:
        i, l = p["id"], p["license"]
        if p["category"] not in cats: err.append(f"{i}: unknown category {p['category']}")
        if l["state"] == "declared" and l["spdx"] not in SPDX: err.append(f"{i}: declared licence '{l['spdx']}' is not a known SPDX id; use needs-review")
        if l["spdx"] == "NOASSERTION": err.append(f"{i}: NOASSERTION is not a licence")
        if l["state"] == "needs-review" and not l.get("review_reason"): err.append(f"{i}: needs-review without review_reason")
        for k in (l["checked"], p["last_checked"]):
            d = parse_date(k)
            if d is None or not (lo <= d <= hi): err.append(f"{i}: invalid or implausible date {k!r}")
        if bootstrap: continue
        e = evidence.get(i)
        if e is None: err.append(f"{i}: missing evidence file"); continue
        if not str(e.get("source", "")).startswith("https://api.github.com/repos/"): err.append(f"{i}: evidence source missing/invalid")
        d = parse_date(e.get("retrieved_at") or "")
        if d is None: err.append(f"{i}: evidence retrieved_at missing/invalid")
        elif not (lo <= d <= hi): err.append(f"{i}: evidence date out of range {e['retrieved_at']}")
        if e.get("state") not in ("active", "archived", "unknown"): err.append(f"{i}: evidence state invalid {e.get('state')!r}")
        fs = (e.get("fetch_status") or {}).get("result", "ok")
        if fs != "ok" and not fs.startswith("partial"): warn.append(f"{i}: last lookup failed ({fs}); evidence may be stale")
        if e.get("state") == "unknown": warn.append(f"{i}: upstream state unknown")
        if e.get("canonical_repo") and e["canonical_repo"].lower() != p["repo"].lower(): err.append(f"{i}: repo moved to {e['canonical_repo']} – update projects.yaml")
        if e.get("state") == "archived": warn.append(f"{i}: upstream archived (labelled, kept)")
        gs = (e.get("license") or {}).get("github_spdx")
        if l["state"] == "declared" and gs and gs not in ("NOASSERTION", l["spdx"]): err.append(f"{i}: declared {l['spdx']} but GitHub detects {gs} – verify LICENSE")
    for f in sorted(set(evidence) - ids): err.append(f"orphan evidence {f}")
    if has_gitmodules: err.append(".gitmodules must not exist")
    if gitlinks: err.append(f"{gitlinks} gitlinks present")
    for name, r in recipes:
        if r["test"]["status"] not in ("tested", "unverified"): err.append(f"{name}: bad test status")
        for c in r["components"]:
            if c not in ids: err.append(f"{name}: component {c} not in catalog")
    return err, warn


def main():
    import yaml
    doc = yaml.safe_load(open("catalog/projects.yaml"))
    cats = [c["id"] for c in yaml.safe_load(open("catalog/categories.yaml"))["categories"]]
    ev = {os.path.basename(f)[:-5]: json.load(open(f)) for f in sorted(glob.glob("catalog/evidence/*.json"))}
    links = sum(1 for l in subprocess.run(["git", "ls-files", "-s"], capture_output=True, text=True).stdout.splitlines() if l.startswith("160000"))
    recipes = [(f, yaml.safe_load(open(f))) for f in sorted(glob.glob("recipes/*/recipe.yaml"))]
    today = datetime.datetime.now(datetime.timezone.utc).date()
    err, warn = check(doc, cats, ev, today, json.load(open("catalog/schema.json")), links, os.path.exists(".gitmodules"), recipes)
    for w in warn: print("WARN", w)
    for e in err: print("ERROR", e)
    print(f"{len(doc['projects'])} projects, {len(cats)} categories, {len(ev)} evidence files, {len(warn)} warnings, {len(err)} errors: {'FAIL' if err else 'OK'}")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
