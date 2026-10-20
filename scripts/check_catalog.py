"""CI: catalog.json vs .gitmodules vs tracked gitlinks; duplicates; missing docs."""
import json,subprocess,configparser,sys,os,collections
err=[];c=json.load(open("catalog.json"))
cat_paths=[f"stacks/{x['id']}/{i[1]}" for x in c["categories"] for i in x["items"]]
cat_repos=[i[0].lower() for x in c["categories"] for i in x["items"]]
for name,lst in (("path",cat_paths),("repo",cat_repos)):
  for v,n in collections.Counter(lst).items():
    if n>1: err.append(f"duplicate {name}: {v}")
gm=configparser.ConfigParser();gm.read(".gitmodules")
gm_paths=[gm[s]["path"] for s in gm.sections()]
for v,n in collections.Counter(gm_paths).items():
  if n>1: err.append(f"duplicate .gitmodules path {v}")
links=[l.split("\t")[1] for l in subprocess.run(["git","ls-tree","-r","HEAD"],capture_output=True,text=True).stdout.splitlines() if l.startswith("160000")]
for a,an,b,bn in ((cat_paths,"catalog",gm_paths,".gitmodules"),(gm_paths,".gitmodules",links,"gitlinks"),(links,"gitlinks",cat_paths,"catalog")):
  for p in sorted(set(a)-set(b)): err.append(f"in {an} but missing from {bn}: {p}")
for x in c["categories"]:
  if not os.path.exists(f"docs/stacks/{x['id']}.md"): err.append(f"missing docs page {x['id']}")
  for i in x["items"]:
    if len(i)!=7 or not all(i): err.append(f"incomplete entry {i}")
print(f"catalog={len(cat_paths)} gitmodules={len(gm_paths)} gitlinks={len(links)}")
if err: print("\n".join(err));sys.exit(1)
print("OK")
