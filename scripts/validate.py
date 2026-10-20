"""Validate catalog/ data. Exit 1 on any error. Warnings are printed but do not fail."""
import json, glob, os, sys, subprocess, datetime, collections, yaml, jsonschema

SPDX = {"MIT", "Apache-2.0", "AGPL-3.0", "GPL-3.0", "GPL-2.0", "LGPL-3.0", "BSD-2-Clause", "BSD-3-Clause", "MPL-2.0",
        "BUSL-1.1", "Elastic-2.0", "FSL-1.1-Apache-2.0", "FSL-1.1-MIT", "CC-BY-4.0", "ISC", "Unlicense"}
err, warn = [], []
cats = [c["id"] for c in yaml.safe_load(open("catalog/categories.yaml"))["categories"]]
doc = yaml.safe_load(open("catalog/projects.yaml"))
try:
    jsonschema.validate(doc, json.load(open("catalog/schema.json")))
except jsonschema.ValidationError as e:
    err.append(f"schema: {e.message} at {list(e.absolute_path)}")
P = doc["projects"]
for key in ("id", "repo"):
    for v, n in collections.Counter(p[key].lower() for p in P).items():
        if n > 1: err.append(f"duplicate {key}: {v}")
for c, n in collections.Counter(cats).items():
    if n > 1: err.append(f"duplicate category {c}")
today = datetime.date.today().isoformat()
ev_files = {os.path.basename(f)[:-5] for f in glob.glob("catalog/evidence/*.json")}
bootstrap = not ev_files
if bootstrap: warn.append("no evidence collected yet (bootstrap) – run the refresh workflow")
for p in P:
    i = p["id"]
    if p["category"] not in cats: err.append(f"{i}: unknown category {p['category']}")
    if not any(p["category"] == c for c in cats): pass
    l = p["license"]
    if l["state"] == "declared" and l["spdx"] not in SPDX: err.append(f"{i}: declared licence '{l['spdx']}' is not a known SPDX id; use state needs-review")
    if l["state"] != "declared" and l["spdx"] == "NOASSERTION": err.append(f"{i}: NOASSERTION is not a licence")
    for k in (l["checked"], p["last_checked"]):
        if not ("2024-01-01" <= k <= today): err.append(f"{i}: implausible date {k}")
    if not bootstrap:
        if i not in ev_files: err.append(f"{i}: missing evidence file catalog/evidence/{i}.json")
        else:
            e = json.load(open(f"catalog/evidence/{i}.json"))
            if not e.get("source", "").startswith("https://api.github.com/") or not e.get("retrieved_at"): err.append(f"{i}: evidence lacks source/retrieved_at")
            elif e["retrieved_at"][:10] > today: err.append(f"{i}: evidence from the future")
            if e.get("canonical_repo") and e["canonical_repo"].lower() != p["repo"].lower(): warn.append(f"{i}: repo moved to {e['canonical_repo']}")
            if e.get("state") == "archived": warn.append(f"{i}: upstream archived")
            gs = (e.get("license") or {}).get("github_spdx")
            if l["state"] == "declared" and gs and gs not in ("NOASSERTION", l["spdx"]): warn.append(f"{i}: declared {l['spdx']} but GitHub detects {gs}")
for f in ev_files - {p["id"] for p in P}: err.append(f"orphan evidence file {f}.json")
if os.path.exists(".gitmodules"): err.append(".gitmodules must not exist (catalog-first repo)")
links = [l for l in subprocess.run(["git", "ls-files", "-s"], capture_output=True, text=True).stdout.splitlines() if l.startswith("160000")]
if links: err.append(f"{len(links)} gitlinks present")
for f in glob.glob("recipes/*/recipe.yaml"):
    r = yaml.safe_load(open(f))
    if r["test"]["status"] not in ("tested", "unverified"): err.append(f"{f}: bad test status")
    for c in r["components"]:
        if c not in {p["id"] for p in P}: err.append(f"{f}: component {c} not in catalog")
for w_ in warn: print("WARN", w_)
for e_ in err: print("ERROR", e_)
print(f"{len(P)} projects, {len(cats)} categories, {len(ev_files)} evidence files: {'FAIL' if err else 'OK'}")
sys.exit(1 if err else 0)
