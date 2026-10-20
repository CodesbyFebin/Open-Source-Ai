import io, json, urllib.error
import pytest
from collect import Client, collect

TS = "2026-10-20T00:00:00Z"
P = {"id": "demo", "repo": "https://github.com/acme/demo"}


class Resp:
    def __init__(self, body, etag=None):
        self.body, self.headers = json.dumps(body).encode(), {"ETag": etag} if etag else {}
    def read(self): return self.body
    def __enter__(self): return self
    def __exit__(self, *a): pass


def http_error(code, headers=None):
    return urllib.error.HTTPError("u", code, "x", headers or {}, io.BytesIO(b""))


class Seq(list):
    """Responses returned in order for one route."""


def fake(routes, calls=None):
    """routes: path-suffix -> body | Exception | list of those (consumed in order)."""
    def opener(req, timeout):
        if calls is not None: calls.append(req)
        for k, v in routes.items():
            if req.full_url.endswith(k):
                item = v.pop(0) if isinstance(v, Seq) else v
                if isinstance(item, Exception): raise item
                return Resp(item, "etag-1")
        raise http_error(404)
    return opener


REPO = {"html_url": "https://github.com/acme/demo", "archived": False, "default_branch": "main", "pushed_at": "2026-10-01T00:00:00Z",
        "license": {"spdx_id": "MIT"}, "stargazers_count": 5}
COMMITS = [{"commit": {"committer": {"date": "2026-10-01T00:00:00Z"}}}]
REL = {"tag_name": "v1", "published_at": "2026-09-01T00:00:00Z"}


def client(routes, **kw):
    return Client(opener=fake(routes, kw.pop("calls", None)), sleep=lambda s: None, **kw)


def test_active_repo():
    st, ev = collect(client({"/repos/acme/demo": REPO, "per_page=1": COMMITS, "/latest": REL}), P, None, TS)
    assert st == "new" and ev["state"] == "active" and not ev["moved"]
    assert ev["last_commit"] == "2026-10-01T00:00:00Z" and ev["latest_release"]["tag"] == "v1"
    assert ev["license"] == {"github_spdx": "MIT", "state": "detected", "source": "https://api.github.com/repos/acme/demo/license"}
    assert ev["fetch_status"]["result"] == "ok"


def test_moved_repo_detected():
    st, ev = collect(client({"/repos/acme/demo": dict(REPO, html_url="https://github.com/newco/demo"), "per_page=1": COMMITS}), P, None, TS)
    assert ev["moved"] is True and ev["canonical_repo"] == "https://github.com/newco/demo"


def test_archived_repo():
    _, ev = collect(client({"/repos/acme/demo": dict(REPO, archived=True), "per_page=1": COMMITS}), P, None, TS)
    assert ev["state"] == "archived"


@pytest.mark.parametrize("spdx,state", [(None, "not-detected"), ("NOASSERTION", "needs-review")])
def test_unknown_licence_never_becomes_a_name(spdx, state):
    repo = dict(REPO, license={"spdx_id": spdx} if spdx else None)
    _, ev = collect(client({"/repos/acme/demo": repo, "per_page=1": COMMITS}), P, None, TS)
    assert ev["license"]["state"] == state and ev["license"]["github_spdx"] == spdx


def test_rate_limited_reports_failure_and_keeps_old_evidence():
    old = {"id": "demo", "state": "active", "source": "s", "retrieved_at": "2026-10-01T00:00:00Z"}
    rl = http_error(403, {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "9999999999"})
    st, ev = collect(client({"/repos/acme/demo": rl}), P, old, TS)
    assert st == "failed" and ev["state"] == "active" and ev["retrieved_at"] == old["retrieved_at"]
    assert ev["fetch_status"] == {"at": TS, "result": "rate-limited"}


def test_short_rate_limit_waits_then_succeeds():
    waits = []
    rl = http_error(429, {"Retry-After": "3"})
    c = Client(opener=fake({"/repos/acme/demo": Seq([rl, REPO]), "per_page=1": COMMITS}), sleep=waits.append)
    st, ev = collect(c, P, None, TS)
    assert st == "new" and waits == [3]


def test_failed_new_project_is_unknown_not_success():
    st, ev = collect(client({"/repos/acme/demo": http_error(502)}), P, None, TS)
    assert st == "failed" and ev["state"] == "unknown" and ev["fetch_status"]["result"] == "error:502"


def test_not_found_is_not_treated_as_deleted_when_evidence_exists():
    old = {"id": "demo", "state": "active", "source": "s", "retrieved_at": "2026-10-01T00:00:00Z"}
    st, ev = collect(client({}), P, old, TS)
    assert st == "not-found" and ev["state"] == "active" and ev["fetch_status"]["result"] == "404"


def test_unchanged_ignores_volatile_fields():
    c = client({"/repos/acme/demo": Seq([REPO, REPO]), "per_page=1": Seq([COMMITS, COMMITS]), "/latest": Seq([REL, REL])})
    _, first = collect(c, P, None, TS)
    st, ev = collect(c, P, dict(first, stars=999), "2026-10-27T00:00:00Z")
    assert st == "unchanged"


def test_etag_304_uses_cache():
    calls = []
    c = client({"/repos/acme/demo": Seq([REPO, http_error(304)]), "per_page=1": Seq([COMMITS, COMMITS])}, calls=calls)
    collect(c, P, None, TS); st, ev = collect(c, P, None, TS)
    assert ev["state"] == "active"
    assert any(r.headers.get("If-none-match") == "etag-1" for r in calls)
