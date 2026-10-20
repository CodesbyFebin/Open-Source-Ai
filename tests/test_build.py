import hashlib, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ["README.md", "CREDITS.md", "mkdocs.yml", "docs/index.md", "docs/freshness.md", "docs/assets/catalog.json"]


def digest():
    files = OUT + sorted(str(p.relative_to(ROOT)) for p in (ROOT / "docs/stacks").glob("*.md"))
    return {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files}


def test_build_is_deterministic():
    subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, check=True)
    a = digest()
    subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, check=True)
    assert digest() == a


def test_archived_projects_are_labelled_not_removed():
    import json
    data = json.loads((ROOT / "docs/assets/catalog.json").read_text())
    for p in data["projects"]:
        if p["status"] == "archived":
            page = (ROOT / f"docs/stacks/{p['category']}.md").read_text()
            assert "archived upstream" in page and p["name"] in page
