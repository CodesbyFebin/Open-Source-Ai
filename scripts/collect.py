"""Refresh evidence for every catalog project from the GitHub REST API.

Writes catalog/evidence/<id>.json. Only collected facts live there; human-authored
fields in projects.yaml are never touched. Uses ETag conditional requests cached in
.cache/etags.json, bounded concurrency, timeouts, retries with backoff and rate-limit
awareness. A failed request never marks a project deleted or unlicensed: previous
evidence is kept and the failure is reported.
"""
import json, os, sys, time, datetime, urllib.request, urllib.error, concurrent.futures as cf
import yaml

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
CACHE = ".cache/etags.json"
os.makedirs(".cache", exist_ok=True); os.makedirs("catalog/evidence", exist_ok=True)
etags = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def get(path):
    url = API + path
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "open-source-ai-collector"})
        if TOKEN: req.add_header("Authorization", f"Bearer {TOKEN}")
        if url in etags: req.add_header("If-None-Match", etags[url]["etag"])
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                body = json.loads(r.read() or b"null")
                if r.headers.get("ETag"): etags[url] = {"etag": r.headers["ETag"], "body": body}
                return 200, body
        except urllib.error.HTTPError as e:
            if e.code == 304: return 200, etags[url]["body"]
            if e.code in (403, 429) and e.headers.get("X-RateLimit-Remaining") == "0":
                wait = max(1, int(e.headers.get("X-RateLimit-Reset", time.time() + 60)) - int(time.time()))
                if wait > 300: return e.code, None
                time.sleep(wait); continue
            if e.code in (404, 451): return e.code, None
            if e.code >= 500: time.sleep(2 ** attempt); continue
            return e.code, None
        except Exception:
            time.sleep(2 ** attempt)
    return -1, None

def collect(p):
    owner_repo = p["repo"].split("github.com/")[1]
    path = f"catalog/evidence/{p['id']}.json"
    old = json.load(open(path)) if os.path.exists(path) else None
    code, repo = get(f"/repos/{owner_repo}")
    if code != 200 or not repo:
        status = "unavailable" if code in (404, 451) and old is None else "fetch-failed"
        if old:  # keep previous facts, record the failure separately
            old["last_attempt"] = {"at": NOW, "http_status": code}
            return p["id"], "failed", old
        return p["id"], status, {"id": p["id"], "source": f"{API}/repos/{owner_repo}", "retrieved_at": NOW, "state": "unknown", "last_attempt": {"at": NOW, "http_status": code}}
    _, commits = get(f"/repos/{owner_repo}/commits?per_page=1")
    _, rel = get(f"/repos/{owner_repo}/releases/latest")
    lic = repo.get("license") or {}
    spdx = lic.get("spdx_id")
    ev = {
        "id": p["id"],
        "source": f"{API}/repos/{owner_repo}",
        "retrieved_at": NOW,
        "canonical_repo": repo.get("html_url"),
        "state": "archived" if repo.get("archived") else "active",
        "default_branch": repo.get("default_branch"),
        "last_commit": (commits[0]["commit"]["committer"]["date"] if isinstance(commits, list) and commits else None),
        "pushed_at": repo.get("pushed_at"),
        "latest_release": ({"tag": rel.get("tag_name"), "published_at": rel.get("published_at")} if isinstance(rel, dict) and rel.get("tag_name") else None),
        "license": {
            "github_spdx": spdx,
            "state": "not-detected" if not spdx else ("needs-review" if spdx == "NOASSERTION" else "detected"),
            "source": f"{API}/repos/{owner_repo}/license",
        },
        "stars": repo.get("stargazers_count"),
    }
    if old:
        same = {k: v for k, v in old.items() if k not in ("retrieved_at", "last_attempt", "stars")} == {k: v for k, v in ev.items() if k not in ("retrieved_at", "stars")}
        if same:
            return p["id"], "unchanged", old
    return p["id"], ("updated" if old else "new"), ev

projects = yaml.safe_load(open("catalog/projects.yaml"))["projects"]
summary = {"new": [], "updated": [], "unchanged": [], "failed": [], "unavailable": [], "fetch-failed": [], "archived": [], "license-needs-review": []}
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for pid, status, ev in ex.map(collect, projects):
        summary[status].append(pid)
        if status != "unchanged":
            json.dump(ev, open(f"catalog/evidence/{pid}.json", "w"), indent=2, sort_keys=True); open(f"catalog/evidence/{pid}.json", "a").write("\n")
        if ev.get("state") == "archived": summary["archived"].append(pid)
        if ev.get("license", {}).get("state") in ("needs-review", "not-detected"): summary["license-needs-review"].append(pid)
json.dump(etags, open(CACHE, "w"))
lines = ["## Catalog evidence refresh", f"Run at {NOW}", ""] + [f"- **{k}** ({len(v)}): {', '.join(sorted(v)) or '–'}" for k, v in summary.items()]
out = "\n".join(lines) + "\n"
print(out)
if os.environ.get("GITHUB_STEP_SUMMARY"): open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(out)
open(".cache/summary.md", "w").write(out)
