#!/usr/bin/env python3
"""Create a navigation-only release from the current VPS snapshot; never read/import Mac data."""
import pathlib,shutil,json,hashlib,argparse,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent));from activate import verify,activate
p=argparse.ArgumentParser();p.add_argument('--base',required=True,type=pathlib.Path);p.add_argument('--release',required=True);a=p.parse_args()
base=a.base.resolve();source=(base/'current').resolve();manifest=verify(source)
if pathlib.Path(a.release).name!=a.release:raise SystemExit('Invalid release name')
target=base/'releases'/a.release
if target.exists():raise SystemExit('Release already exists; use a new name')
shutil.copytree(source,target)
for c in ['brad','steve']:
 name=c.title();f=target/'site'/c/'index.html';s=f.read_text();s=s.replace(name+'’s career workspace',name+'’s document library')
 s=s.replace('</h1>','</h1><p><a class="edit-link" href="/'+c+'/workspace">Edit profile, CV and tracker</a></p>',1);f.write_text(s)
 f=target/'site/index.html';s=f.read_text();s=s.replace('<a href="/'+c+'/">Open '+name+'’s workspace</a>','<a class="edit-link" href="/'+c+'/workspace">Edit '+name+'’s profile, CV and tracker</a><p><a href="/'+c+'/">View '+name+'’s documents</a></p>');f.write_text(s)
for f in [target/'site/index.html']+list((target/'site').glob('*/index.html'))+list((target/'site').glob('*/view/**/*.html')):
 s=f.read_text().replace('Viewing only · Sources stay on the Mac.','Historical document library · Current profiles, CVs and trackers are edited on the VPS.').replace('Viewing only. Job-search drafts require review before use.','Document library. Use the edit buttons to update your live workspace. Job-search drafts require review before use.').replace('Editing, scanning and AI document generation on the VPS are planned as a separate phase; the experimental career-ops web interface is not exposed here.','Use the edit buttons for current profiles, CVs and trackers. These document-library copies are dated snapshots. Scanning and AI document generation are planned for a later phase.');f.write_text(s)
css=target/'site/assets/portal.css';css.write_text(css.read_text()+'\n.edit-link{display:inline-block;background:#174b70;color:#fff;padding:14px 18px;border-radius:10px;font-weight:700;text-decoration:none;min-height:44px;box-sizing:border-box}\n')
# Original document bytes must be unchanged.
for c in ['brad','steve']:
 for old in (source/'site'/c/'files').rglob('*'):
  if old.is_file():assert old.read_bytes()==(target/old.relative_to(source)).read_bytes()
manifest['navigation_update']='Live editing links added; original snapshot dates and document bytes preserved'
manifest['files']=[{'path':str(f.relative_to(target)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':f.stat().st_size} for f in sorted((target/'site').rglob('*')) if f.is_file()]
(target/'manifest.json').write_text(json.dumps(manifest,indent=2));(target/'manifest.json').chmod(0o600)
verify(target);print(json.dumps(activate(base,a.release)))
