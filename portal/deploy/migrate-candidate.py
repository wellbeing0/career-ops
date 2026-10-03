#!/usr/bin/env python3
import hashlib,json,pathlib,shutil,sys
source,destination=map(pathlib.Path,sys.argv[1:]); manifest=json.loads((source/'migration-manifest.json').read_text())
if (destination/'cv.md').exists():raise SystemExit('Refusing to overwrite an existing dataset')
for name,digest in manifest['files'].items():
 f=source/name
 if f.is_symlink() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise SystemExit('Migration checksum mismatch')
for name,digest in manifest['files'].items():
 out=destination/name;out.parent.mkdir(parents=True,exist_ok=True,mode=0o700);shutil.copyfile(source/name,out);out.chmod(0o600)
 if hashlib.sha256(out.read_bytes()).hexdigest()!=digest:raise SystemExit('Copied checksum mismatch')
(destination/'.hosted').mkdir(exist_ok=True,mode=0o700)
(destination/'.hosted/authority.json').write_text(json.dumps({'authority':'VPS','initial_manifest':manifest,'mac_role':'backup/export only'}))
print(json.dumps({'migration':'verified','files':len(manifest['files'])}))
