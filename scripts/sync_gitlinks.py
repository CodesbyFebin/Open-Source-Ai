"""Ensure every catalog entry is a gitlink in the index (pinned to upstream HEAD, no clone needed)."""
import json,subprocess,os,sys
c=json.load(open("catalog.json"))
have={l.split("\t")[1]:l.split()[1] for l in subprocess.run(["git","ls-files","-s"],capture_output=True,text=True).stdout.splitlines() if l.startswith("160000")}
want={}
for cat in c["categories"]:
  for it in cat["items"]: want[f"stacks/{cat['id']}/{it[1]}"]=it[0]
for p in set(have)-set(want): subprocess.run(["git","rm","--cached","-q",p],check=True)
for p,r in want.items():
  os.makedirs(p,exist_ok=True)
  if p in have and "--update" not in sys.argv: continue
  sha=subprocess.run(["git","ls-remote",f"https://github.com/{r}","HEAD"],capture_output=True,text=True,timeout=90).stdout.split()[0]
  subprocess.run(["git","update-index","--add","--cacheinfo",f"160000,{sha},{p}"],check=True)
print("gitlinks:",len(want))
