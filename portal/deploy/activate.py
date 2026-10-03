#!/usr/bin/env python3
"""Verify an immutable snapshot completely before replacing its current symlink."""
import argparse,hashlib,json,os,pathlib

def verify(release):
 manifest=json.loads((release/'manifest.json').read_text());paths=set()
 for item in manifest['files']:
  rel=pathlib.PurePosixPath(item['path'])
  if rel.is_absolute() or '..' in rel.parts or rel.parts[0]!='site':raise ValueError('Invalid manifest path')
  p=release/rel
  if p.is_symlink() or not p.resolve().is_relative_to(release.resolve()):raise ValueError('Release symlink escape')
  if p.stat().st_size!=item['size'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Release hash mismatch: '+str(rel))
  if str(rel) in paths:raise ValueError('Duplicate manifest path')
  paths.add(str(rel))
 actual={p.relative_to(release).as_posix() for p in (release/'site').rglob('*') if p.is_file()}
 if actual!=paths:raise ValueError('Release contains unlisted or missing served files')
 if any(p.is_symlink() for p in (release/'site').rglob('*')):raise ValueError('Symlinks in served release')
 return manifest

def activate(base,release_name):
 if pathlib.Path(release_name).name!=release_name or release_name in {'.','..'}:raise ValueError('Invalid release name')
 base=base.resolve();release=base/'releases'/release_name;verify(release)
 current=base/'current'
 if current.exists() and not current.is_symlink():raise ValueError('current must be a symlink')
 previous=os.readlink(current) if current.is_symlink() else None
 temp=base/('.current-'+str(os.getpid()));temp.symlink_to('releases/'+release_name);os.replace(temp,current)
 return {'release':release_name,'previous':previous}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--release',required=True);a=p.parse_args();print(json.dumps(activate(pathlib.Path(a.base),a.release)))
