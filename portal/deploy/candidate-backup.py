#!/usr/bin/env python3
"""Private snapshot and checksum-verified restore drill; never restores over live data."""
import argparse, hashlib, json, os, pathlib, tarfile, tempfile, datetime
p=argparse.ArgumentParser(); p.add_argument('root',type=pathlib.Path); p.add_argument('destination',type=pathlib.Path);p.add_argument('--drill',action='store_true');p.add_argument('--prune',action='store_true');a=p.parse_args()
os.umask(0o077);(a.root/'.hosted').mkdir(exist_ok=True,mode=0o700)
lock=a.root/'.hosted/edit.lock'
try:
 fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
except FileExistsError:raise SystemExit('Candidate busy; backup refused rather than capturing an inconsistent save')
os.write(fd,json.dumps({'pid':os.getpid()}).encode());os.close(fd)
import atexit
atexit.register(lambda:lock.unlink(missing_ok=True))
if (a.root/'.hosted/pending.json').exists() or (a.root/'.hosted/evaluations/pending.json').exists():raise SystemExit('Interrupted save requires recovery before backup')
for receipt in (a.root/'.hosted/search').glob('*/publication.json'):
 if json.loads(receipt.read_text()).get('status')=='pending':raise SystemExit('Interrupted search publication requires reconciliation before backup')
a.destination.mkdir(parents=True,exist_ok=True,mode=0o700)
files={str(f.relative_to(a.root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in a.root.rglob('*') if f.is_file() and not f.is_symlink() and f.name not in ['edit.lock','edit.lock.recovery'] and '.hosted/backups' not in str(f.relative_to(a.root)) and not (str(f.relative_to(a.root)).startswith('.hosted/search/') and 'runtime' in f.relative_to(a.root).parts) and not str(f.relative_to(a.root)).startswith('data/cache/')}
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');archive=a.destination/(stamp+'.tar.gz');manifest=a.destination/(stamp+'.json')
with tarfile.open(archive,'w:gz') as out:
 for name in sorted(files):out.add(a.root/name,arcname=name,recursive=False)
with tarfile.open(archive) as snapshot:
 for name,digest in files.items():
  if hashlib.sha256(snapshot.extractfile(name).read()).hexdigest()!=digest:
   archive.unlink();raise SystemExit('Source changed during snapshot; backup refused')
manifest.write_text(json.dumps({'authority':'VPS','files':files,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
if a.drill:
 with tempfile.TemporaryDirectory(prefix='career-restore-') as tmp:
  with tarfile.open(archive) as source: source.extractall(tmp,filter='data')
  for name,digest in files.items():
   if hashlib.sha256((pathlib.Path(tmp)/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Restore checksum mismatch')
pruning='disabled until owner acceptance'
if a.prune and (a.root/'.hosted/acceptance.json').is_file():
 snapshots=sorted(a.destination.glob('*.tar.gz'),reverse=True);daily={};weekly={}
 for snapshot in snapshots:
  date=datetime.datetime.strptime(snapshot.name.removesuffix('.tar.gz'),'%Y%m%dT%H%M%S%fZ').replace(tzinfo=datetime.timezone.utc)
  daily.setdefault(date.date(),snapshot);weekly.setdefault(date.isocalendar()[:2],snapshot)
 keep=set(list(daily.values())[:30]+list(weekly.values())[:12])
 for snapshot in snapshots:
  if snapshot not in keep:
   snapshot.unlink();snapshot.with_suffix('').with_suffix('.json').unlink(missing_ok=True)
 cutoff=datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=90)
 for folder in ['revisions','tracker-revisions']:
  for entry in (a.root/'.hosted'/folder).glob('*'):
   try:created=datetime.datetime.fromtimestamp(int(entry.name.split('-')[0])/1000,datetime.timezone.utc)
   except (ValueError,OverflowError):continue
   if created<cutoff and entry.is_file() and not entry.is_symlink():entry.unlink()
 pruning='30 daily / 12 weekly snapshots; revisions 90 days'
print(json.dumps({'snapshot':str(archive),'files':len(files),'restore_drill':a.drill,'pruning':pruning}))
