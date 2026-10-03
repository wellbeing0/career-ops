#!/usr/bin/env python3
"""Package system code only. Candidate data is a separate, one-time migration."""
import argparse,pathlib,shutil,tarfile
p=argparse.ArgumentParser();p.add_argument('destination',type=pathlib.Path);a=p.parse_args();root=pathlib.Path(__file__).resolve().parents[2];out=a.destination/'code';out.mkdir(parents=True,exist_ok=True)
for f in root.glob('*.mjs'):shutil.copy2(f,out/f.name)
for name in ['package.json','tracker-aliases.json']:shutil.copy2(root/name,out/name)
for name in ['lib','templates','providers','portal','plugins']:shutil.copytree(root/name,out/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
w=out/'web';w.mkdir(exist_ok=True)
for name in ['src','public']:shutil.copytree(root/'web'/name,w/name,dirs_exist_ok=True)
for name in ['package.json','package-lock.json','next.config.mjs','tsconfig.json','postcss.config.mjs']:
 if (root/'web'/name).exists():shutil.copy2(root/'web'/name,w/name)
with tarfile.open(a.destination/'code.tar.gz','w:gz') as t:t.add(out,arcname='.')
print(a.destination/'code.tar.gz')
