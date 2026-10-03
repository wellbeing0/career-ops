#!/usr/bin/env python3
"""Copy only the published snapshot; fix live navigation/theme without importing candidate data."""
import argparse,pathlib,shutil,json,hashlib,importlib.util,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from activate import verify,activate
p=argparse.ArgumentParser();p.add_argument('--base',required=True,type=pathlib.Path);p.add_argument('--release',required=True);p.add_argument('--activate',action='store_true');a=p.parse_args()
base=a.base.resolve();source=(base/'current').resolve();manifest=verify(source)
if not source.is_relative_to(base/'releases') or pathlib.Path(a.release).name!=a.release:raise SystemExit('Unexpected release path')
target=base/'releases'/a.release
if target.exists():raise SystemExit('Release exists; use a new name')
shutil.copytree(source,target)
for f in (target/'site').rglob('*.html'):
 if 'files' in f.relative_to(target/'site').parts:continue
 text=f.read_text()
 for c in ['brad','steve']:
  name=c.title();live='/'+c+'/workspace?view=documents'
  text=text.replace('href="/'+c+'/">'+c.title()+'</a>','href="'+live+'">'+c.title()+'</a>')
  text=text.replace('href="/'+c+'/">View '+name+'’s documents','href="'+live+'">View '+name+'’s documents')
  if f==target/'site'/c/'index.html':
   text=text.replace(name+'’s document library',name+'’s archived document library')
   text=text.replace('</h1>','</h1><p><a class="edit-link" href="'+live+'">View current documents and searches</a></p>',1)
 text=text.replace('Use the edit buttons for current profiles, CVs and trackers. These document-library copies are dated snapshots. Scanning and AI document generation are planned for a later phase.','Use the workspace for live searches, profiles, CVs and documents. Dated archive copies remain available from Documents. AI assistance is planned for the next phase.')
 f.write_text(text)
spec=importlib.util.spec_from_file_location('builder',pathlib.Path(__file__).parents[1]/'build.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
(target/'site/assets/portal.css').write_text(builder.CSS+'\n.edit-link{display:inline-block;background:#174b70;color:#fff;padding:14px 18px;border-radius:10px;font-weight:700;text-decoration:none;min-height:44px;box-sizing:border-box}\n')
for c in ['brad','steve']:
 for f in (source/'site'/c/'files').rglob('*'):
  if f.is_file() and f.read_bytes()!=(target/f.relative_to(source)).read_bytes():raise SystemExit('Original document changed')
manifest['navigation_update']='Live Documents links, archive labels and system light/dark theme; snapshot date and originals preserved'
manifest['files']=[{'path':str(f.relative_to(target)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':f.stat().st_size} for f in sorted((target/'site').rglob('*')) if f.is_file()]
(target/'manifest.json').write_text(json.dumps(manifest,indent=2));(target/'manifest.json').chmod(0o600);verify(target)
print(json.dumps(activate(base,a.release) if a.activate else {'staged':str(target),'source':str(source)}))
