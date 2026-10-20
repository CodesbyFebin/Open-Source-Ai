import copy, datetime
from validate import check, parse_date

TODAY = datetime.date(2026, 10, 20)
PROJ = {"id": "demo", "name": "Demo", "repo": "https://github.com/acme/demo", "category": "memory", "description": "A demo project for tests",
        "tasks": ["memory"], "deployment": ["library"], "hardware": "cpu-ok", "languages": ["Python"],
        "license": {"spdx": "MIT", "label": "MIT", "state": "declared", "evidence_url": "https://github.com/acme/demo/blob/main/LICENSE", "checked": "2026-10-20"},
        "setup_url": "https://github.com/acme/demo", "last_checked": "2026-10-20"}
EV = {"id": "demo", "source": "https://api.github.com/repos/acme/demo", "retrieved_at": "2026-10-20T03:00:00Z", "state": "active",
      "canonical_repo": "https://github.com/acme/demo", "license": {"github_spdx": "MIT"}, "fetch_status": {"result": "ok"}}


def run(proj=None, ev=None, evidence=True):
    p = copy.deepcopy(proj or PROJ)
    e = {"demo": copy.deepcopy(ev or EV)} if evidence else {}
    return check({"projects": [p]}, ["memory"], e, TODAY)


def test_clean():
    assert run() == ([], [])


def test_duplicate_ids():
    err, _ = check({"projects": [PROJ, dict(PROJ, repo="https://github.com/x/y")]}, ["memory"], {}, TODAY)
    assert any("duplicate id" in e for e in err)


def test_missing_evidence():
    err, _ = check({"projects": [PROJ, dict(PROJ, id="other", repo="https://github.com/x/y")]}, ["memory"], {"demo": EV}, TODAY)
    assert "other: missing evidence file" in err


def test_invalid_evidence():
    err, _ = run(ev=dict(EV, source="http://evil", retrieved_at="yesterday", state="gone"))
    assert len([e for e in err if e.startswith("demo: evidence")]) == 3


def test_moved_repo_is_error():
    err, _ = run(ev=dict(EV, canonical_repo="https://github.com/newco/demo"))
    assert any("moved" in e for e in err)


def test_archived_is_warning_not_error():
    err, warn = run(ev=dict(EV, state="archived"))
    assert not err and any("archived" in w for w in warn)


def test_unknown_licence_rules():
    p = copy.deepcopy(PROJ); p["license"].update(spdx="Custom-1", state="declared")
    assert any("not a known SPDX" in e for e in run(p)[0])
    p["license"].update(spdx=None, state="needs-review")
    assert any("without review_reason" in e for e in run(p)[0])
    p["license"]["review_reason"] = "Custom terms in upstream LICENSE file"
    assert run(p)[0] == []


def test_licence_mismatch_with_github_is_error():
    assert any("GitHub detects" in e for e in run(ev=dict(EV, license={"github_spdx": "Apache-2.0"}))[0])


def test_failed_lookup_is_warning():
    _, warn = run(ev=dict(EV, fetch_status={"result": "rate-limited"}))
    assert any("lookup failed (rate-limited)" in w for w in warn)


def test_dates():
    assert parse_date("2026-10-20") == TODAY
    assert parse_date("2026-10-20T23:59:59Z") == TODAY
    assert parse_date("2026-10-20T23:59:59") is None  # no zone
    assert parse_date("2026-13-01") is None and parse_date("") is None
    p = copy.deepcopy(PROJ); p["last_checked"] = "2026-10-21"  # +1 day tolerance (time zones)
    assert run(p)[0] == []
    p["last_checked"] = "2026-10-23"
    assert any("implausible date" in e for e in run(p)[0])
    p["last_checked"] = "2019-01-01"
    assert any("implausible date" in e for e in run(p)[0])
