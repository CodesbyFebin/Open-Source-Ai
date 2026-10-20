"""Write every upstream URL from catalog/projects.yaml (repo, licence evidence, setup) to _links/upstream.md for lychee."""
import os, yaml
P = yaml.safe_load(open("catalog/projects.yaml"))["projects"]
urls = sorted({u.split("#")[0] for p in P for u in (p["repo"], p["license"]["evidence_url"], p["setup_url"])})
os.makedirs("_links", exist_ok=True)
with open("_links/upstream.md", "w") as f:
    f.write("# Upstream URLs\n\n" + "\n".join(f"- <{u}>" for u in urls) + "\n")
print(f"{len(urls)} unique upstream URLs from {len(P)} projects")
