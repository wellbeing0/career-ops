#!/usr/bin/env python3
"""Package system code only. Candidate data is a separate, one-time migration."""
import argparse,pathlib,shutil,tarfile,json,hashlib,subprocess,re
p=argparse.ArgumentParser();p.add_argument('destination',type=pathlib.Path);p.add_argument('--release',required=True);a=p.parse_args();
if not re.fullmatch(r'[a-z0-9-]{1,80}',a.release):raise SystemExit('Invalid release identifier')
root=pathlib.Path(__file__).resolve().parents[2];out=a.destination/'code';out.mkdir(parents=True,exist_ok=True)
for f in root.glob('*.mjs'):shutil.copy2(f,out/f.name)
for name in ['package.json','tracker-aliases.json']:shutil.copy2(root/name,out/name)
for name in ['lib','templates','providers','portal','plugins']:shutil.copytree(root/name,out/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
w=out/'web';w.mkdir(exist_ok=True)
for name in ['src','public']:shutil.copytree(root/'web'/name,w/name,dirs_exist_ok=True)
for name in ['package.json','package-lock.json','next.config.mjs','tsconfig.json','postcss.config.mjs']:
 if (root/'web'/name).exists():shutil.copy2(root/'web'/name,w/name)
# Fixed public procedures only: never package candidate-owned mode customizations.
mode_files=['_shared.md','oferta.md','text.md','cover.md','email.md','interview/plan.md','interview/practice.md','interview/debrief.md']
for name in mode_files:
 target=out/'modes'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'modes'/name,target)
knowledge=out/'portal/knowledge';names=['project-overview.md','workspace-guide.md','search-pipeline-guide.md','assistant-capabilities.md']
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
if subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=root,text=True).strip():raise SystemExit('Commit reviewed changes before packaging deployment knowledge')
(knowledge/'manifest.json').write_text(json.dumps({'format':'career-project-knowledge-v1','release':a.release,'sourceCommit':commit,'sha256':{n:hashlib.sha256((knowledge/n).read_bytes()).hexdigest() for n in names}},indent=2)+'\n')
with tarfile.open(a.destination/'code.tar.gz','w:gz') as t:t.add(out,arcname='.')
print(a.destination/'code.tar.gz')
