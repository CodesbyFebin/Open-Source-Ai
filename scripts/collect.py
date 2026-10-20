"""Refresh evidence for every catalog project from the GitHub REST API.

Writes catalog/evidence/<id>.json (collected facts only; projects.yaml is never touched).
- ETag conditional requests cached in .cache/etags.json
- bounded concurrency (4), 20 s timeouts, retries with exponential backoff
- rate-limit aware: waits up to 5 min for reset, otherwise reports "rate-limited"
- a failed lookup is NEVER reported as success and never marks a project deleted:
  previous facts are kept and `fetch_status` records the failure.
Exit code 1 if every lookup failed (nothing trustworthy to propose).
"""
import json, os, sys, time, datetime, urllib.request, urllib.error, concurrent.futures as cf

API = "https://api.github.com"
VOLATILE = ("retrieved_at", "stars", "fetch_status")


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class Client:
    def __init__(self, token=None, etags=None, sleep=time.sleep, opener=urllib.request.urlopen, max_wait=300):
        self.token, self.etags, self.sleep, self.open, self.max_wait = token, etags if etags is not None else {}, sleep, opener, max_wait

    def get(self, path):
        """Return (status, body). status: 200, 404, 451, 'rate-limited', or 'error:<code>'."""
        url = API + path
        last = "error:unknown"
        for attempt in range(4):
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "open-source-ai-collector"})
            if self.token: req.add_header("Authorization", f"Bearer {self.token}")
            if url in self.etags: req.add_header("If-None-Match", self.etags[url]["etag"])
            try:
                with self.open(req, timeout=20) as r:
                    body = json.loads(r.read() or b"null")
                    if r.headers.get("ETag"): self.etags[url] = {"etag": r.headers["ETag"], "body": body}
                    return 200, body
            except urllib.error.HTTPError as e:
                if e.code == 304 and url in self.etags: return 200, self.etags[url]["body"]
                if e.code in (403, 429) and (e.headers.get("X-RateLimit-Remaining") == "0" or e.headers.get("Retry-After")):
                    reset = e.headers.get("Retry-After")
                    wait = int(reset) if reset else int(e.headers.get("X-RateLimit-Reset", 0)) - int(time.time())
                    if wait > self.max_wait: return "rate-limited", None
                    self.sleep(max(1, wait)); last = "rate-limited"; continue
                if e.code in (404, 451): return e.code, None
                last = f"error:{e.code}"
                if e.code >= 500: self.sleep(2 ** attempt); continue
                return last, None
            except Exception as e:  # timeouts, DNS, bad JSON
                last = f"error:{type(e).__name__}"; self.sleep(2 ** attempt)
        return last, None


def collect(client, p, old, ts):
    """Return (status, evidence). status in new|updated|unchanged|failed|not-found."""
    owner_repo = p["repo"].split("github.com/")[1]
    src = f"{API}/repos/{owner_repo}"
    code, repo = client.get(f"/repos/{owner_repo}")
    if code != 200 or not isinstance(repo, dict):
        status = "not-found" if code in (404, 451) else "failed"
        attempt = {"at": ts, "result": str(code)}
        if old:
            ev = dict(old); ev["fetch_status"] = attempt
            return status, ev
        return status, {"id": p["id"], "source": src, "retrieved_at": ts, "state": "unknown", "fetch_status": attempt}
    c_code, commits = client.get(f"/repos/{owner_repo}/commits?per_page=1")
    r_code, rel = client.get(f"/repos/{owner_repo}/releases/latest")
    lic = repo.get("license") or {}
    spdx = lic.get("spdx_id")
    canonical = repo.get("html_url")
    ev = {
        "id": p["id"], "source": src, "retrieved_at": ts,
        "canonical_repo": canonical,
        "moved": bool(canonical) and canonical.lower() != p["repo"].lower(),
        "state": "archived" if repo.get("archived") else "active",
        "default_branch": repo.get("default_branch"),
        "last_commit": commits[0]["commit"]["committer"]["date"] if c_code == 200 and isinstance(commits, list) and commits else None,
        "pushed_at": repo.get("pushed_at"),
        "latest_release": {"tag": rel.get("tag_name"), "published_at": rel.get("published_at")} if r_code == 200 and isinstance(rel, dict) and rel.get("tag_name") else None,
        "license": {"github_spdx": spdx,
                    "state": "not-detected" if not spdx else ("needs-review" if spdx == "NOASSERTION" else "detected"),
                    "source": f"{src}/license"},
        "stars": repo.get("stargazers_count"),
        "fetch_status": {"at": ts, "result": "ok" if c_code == 200 else f"partial (commits: {c_code})"},
    }
    if old and {k: v for k, v in old.items() if k not in VOLATILE} == {k: v for k, v in ev.items() if k not in VOLATILE}:
        return "unchanged", old
    return ("updated" if old else "new"), ev


def main():
    import yaml
    os.makedirs(".cache", exist_ok=True); os.makedirs("catalog/evidence", exist_ok=True)
    cache = ".cache/etags.json"
    client = Client(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"), json.load(open(cache)) if os.path.exists(cache) else {})
    ts = now_utc()
    projects = yaml.safe_load(open("catalog/projects.yaml"))["projects"]
    def one(p):
        path = f"catalog/evidence/{p['id']}.json"
        old = json.load(open(path)) if os.path.exists(path) else None
        return p["id"], path, old, *collect(client, p, old, ts)
    S = {k: [] for k in ("new", "updated", "unchanged", "failed", "not-found", "archived", "moved", "license-needs-review")}
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for pid, path, old, status, ev in ex.map(one, projects):
            S[status].append(pid)
            if ev is not old:
                with open(path, "w") as f: json.dump(ev, f, indent=2, sort_keys=True); f.write("\n")
            if ev.get("state") == "archived": S["archived"].append(pid)
            if ev.get("moved"): S["moved"].append(pid)
            if (ev.get("license") or {}).get("state") in ("needs-review", "not-detected"): S["license-needs-review"].append(pid)
    json.dump(client.etags, open(cache, "w"))
    bad = len(S["failed"]) + len(S["not-found"])
    out = "\n".join([f"## Catalog evidence refresh – {ts}", "",
                     f"**{bad} of {len(projects)} lookups failed or not found** – those projects keep their previous evidence and are flagged; review before merging." if bad else "All lookups succeeded.", ""]
                    + [f"- **{k}** ({len(v)}): {', '.join(sorted(v)) or '–'}" for k, v in S.items()]) + "\n"
    print(out)
    if os.environ.get("GITHUB_STEP_SUMMARY"): open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(out)
    open(".cache/summary.md", "w").write(out)
    if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"failed={bad}\n")
    return 1 if bad == len(projects) else 0


if __name__ == "__main__":
    sys.exit(main())
