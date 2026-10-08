#!/usr/bin/env python3
"""Stage only the index/styles; retain byte-identical archives and existing static pages."""
import argparse,hashlib,importlib.util,json,pathlib,re,shutil,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from activate import verify
p=argparse.ArgumentParser();p.add_argument('--base',required=True,type=pathlib.Path);p.add_argument('--release',required=True);a=p.parse_args()
if not re.fullmatch(r'[a-z0-9-]{1,80}',a.release):raise SystemExit('Invalid release name')
base=a.base.resolve();source=(base/'current').resolve();manifest=verify(source)
if not source.is_relative_to(base/'releases'):raise SystemExit('Unexpected current release')
target=base/'releases'/a.release
if target.exists():raise SystemExit('Release exists; use a new name')
shutil.copytree(source,target)
spec=importlib.util.spec_from_file_location('home',pathlib.Path(__file__).parents[1]/'home.py');home=importlib.util.module_from_spec(spec);spec.loader.exec_module(home)
(target/'site/index.html').write_text(home.start_page());(target/'site/assets/home.css').write_text(home.CSS)
for f in (source/'site').rglob('*'):
 if f.is_file() and f.relative_to(source).as_posix()!='site/index.html' and f.read_bytes()!=(target/f.relative_to(source)).read_bytes():raise SystemExit('Existing served document changed')
manifest['home_source']=source.relative_to(base).as_posix();manifest['navigation_update']='Workflow re-entry start page; live workspace shortcuts; original archive files preserved'
manifest['files']=[{'path':f.relative_to(target).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':f.stat().st_size} for f in sorted((target/'site').rglob('*')) if f.is_file()]
(target/'manifest.json').write_text(json.dumps(manifest,indent=2));(target/'manifest.json').chmod(0o600);verify(target)
print(json.dumps({'staged':str(target),'source':str(source),'originalFilesPreserved':True}))
