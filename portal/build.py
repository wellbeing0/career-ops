#!/usr/bin/env python3
"""Private, read-only snapshot builder. User data is never written into the checkout."""
import argparse, csv, datetime, hashlib, html, json, os, pathlib, re, shutil
from urllib.parse import quote, urlsplit

TEXT={'.md','.txt','.yml','.yaml','.tsv','.csv'}
DOWNLOAD=TEXT|{'.html','.pdf','.docx','.doc','.rtf'}
AREAS={'config','modes','data','reports','output','documents','interview-prep','writing-samples'}
ROOT_FILES={'cv.md','article-digest.md','voice-dna.md','portals.yml'}
EXCLUDED={'migration-backup','migration-checks','data-folder-migration','reboot-checkpoints','backup','backups','merged','tracker-additions','node_modules','__pycache__'}
SECRET=re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-proj-|sk-ant-api\w*-)[A-Za-z0-9_-]{12,}|(?im:^\s*(?:api_key|access_token|client_secret|password)\s*[:=]\s*[\"\']?[A-Za-z0-9_+/=-]{12,})')
CSS=''':root{color-scheme:light;--bg:#f7f6f3;--fg:#1f1c19;--surface:#fff;--border:#dfddd8;--muted:#5e5851;--link:#15569a;--notice:#fff4d7;--pre:#f2f1ed}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui}main{max-width:1120px;margin:auto;padding:32px 22px}h1{font-size:36px;line-height:1.2}h2{font-size:24px}h3{font-size:19px}a{color:var(--link);text-underline-offset:3px}nav{display:flex;flex-wrap:wrap;gap:18px;margin:14px 0}.card,.document{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px;margin:18px 0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}.cards .card{margin:0}.muted{color:var(--muted);font-size:14px}.notice{background:var(--notice);padding:14px 18px;border-radius:8px}.files{list-style:none;padding:0}.files li{padding:12px 0;border-bottom:1px solid var(--border)}.files span{display:block}table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow:auto}td,th{border:1px solid var(--border);padding:9px;vertical-align:top}pre{background:var(--pre);padding:16px;overflow:auto;font-size:13px;white-space:pre-wrap;overflow-wrap:anywhere}code{font-size:13px}iframe{width:100%;height:85vh;border:1px solid var(--border);background:var(--surface)}details{margin:18px 0}summary{cursor:pointer;font-weight:600}li{margin:5px 0}footer{margin-top:36px}.document{overflow-wrap:anywhere}@media(max-width:600px){main{padding:20px 12px}.document,.card{padding:17px}h1{font-size:29px}}@media print{nav,.notice,footer{display:none}body{background:var(--surface)}main{padding:0}.document{border:none}}@media(prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#0a0a0a;--fg:#fafafa;--surface:#161616;--border:#262626;--muted:#a1a1aa;--link:#8fc5f5;--notice:#2b2518;--pre:#111111}}@media print{:root{color-scheme:light;--bg:white;--fg:black;--surface:white;--muted:#444;--link:#15569a;--border:#ddd;--pre:#eee}}'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(t):return datetime.datetime.fromtimestamp(t,datetime.timezone.utc).astimezone(__import__('zoneinfo').ZoneInfo('America/Detroit')).strftime('%b %d, %Y %I:%M %p ET')
def esc(s):return html.escape(str(s),quote=True)
def page(title,body):return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>'+esc(title)+'</title><link rel="stylesheet" href="/assets/portal.css"></head><body><main><nav><a href="/">Career Ops</a><a href="/brad/workspace?view=documents">Brad</a><a href="/steve/workspace?view=documents">Steve</a></nav>'+body+'<footer class="muted">Private shared workspace · Historical document library · Current profiles, CVs and trackers are edited on the VPS. Published documents may contain contact information and personal job-search notes.</footer></main></body></html>'

def selected(root):
 included=[];omitted=[]
 for f in sorted(root.rglob('*')):
  rel=f.relative_to(root)
  if f.is_symlink() and not f.resolve().is_relative_to(root):raise ValueError('Candidate symlink escapes its root: '+str(rel))
  if not f.is_file():continue
  parts=rel.parts; reason=None
  if f.is_symlink():reason='symlink not published'
  elif any(p.startswith('.') or p in EXCLUDED for p in parts):reason='private runtime or archive'
  elif any('migration' in p.lower() or 'backup' in p.lower() or 'receipt' in p.lower() for p in parts):reason='migration, backup or receipt'
  elif f.suffix.lower() not in DOWNLOAD:reason='not a reading document'
  elif len(parts)==1 and f.name not in ROOT_FILES and f.suffix.lower() not in {'.pdf','.docx','.doc','.rtf'}:reason='outside selected user documents'
  elif len(parts)>1 and parts[0] not in AREAS:reason='outside selected user areas'
  if reason:omitted.append({'path':rel.as_posix(),'reason':reason});continue
  if f.suffix.lower() in TEXT|{'.html'}:
   text=f.read_text(encoding='utf-8',errors='strict')
   if SECRET.search(text):raise ValueError('Possible credential content in selected document: '+rel.as_posix())
  included.append(f)
 return included,omitted

def group(rel):
 p=rel.parts
 if p[0]=='config' or p[0]=='modes' or rel.name in {'cv.md','voice-dna.md','article-digest.md'}:return 'Profile and master CV'
 if p[0]=='reports':return 'Job evaluations'
 if 'samples-' in rel.as_posix():return 'Sample applications and resumes'
 if 'survey-' in rel.as_posix() or 'search-' in rel.as_posix() or rel.name in {'pipeline.md','scan-history.tsv','scan-runs.tsv','portals.yml','portal-health.tsv'}:return 'Search results and pipeline'
 if p[0]=='interview-prep':return 'Interview preparation'
 if p[0]=='documents' or rel.suffix.lower() in {'.pdf','.docx','.doc','.rtf'} or rel.name.startswith('cv-'):return 'Resume documents and supporting sources'
 return 'Tracker and job-search notes'

def render(text,rel,slug,known):
 def inline(s):
  # Escape every source before adding our own narrowly allowed markup.
  s=esc(s)
  def link(m):
   label,url=m.groups();url=html.unescape(url)
   parsed=urlsplit(url)
   if parsed.scheme in {'http','https','mailto'}:return '<a href="'+esc(url)+'" rel="noopener noreferrer">'+label+'</a>'
   if parsed.scheme or url.startswith('/') or url.startswith('//'):return label
   target=os.path.normpath(str(rel.parent/parsed.path)).replace(os.sep,'/')
   if target not in known:return label
   return '<a href="/'+slug+'/view/'+quote(target,safe='/')+'.html">'+label+'</a>'
  s=re.sub(r'(?<!!)\[([^\]]+)\]\(([^\s)]+)\)',link,s)
  s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
  s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
  return s
 lines=text.splitlines();blocks=[];code=[];fenced=False;inlist=False;table=False
 for line in lines:
  if line.startswith('```'):
   if inlist:blocks.append('</ul>');inlist=False
   if table:blocks.append('</tbody></table>');table=False
   if fenced:blocks.append('<pre><code>'+esc('\n'.join(code))+'</code></pre>');code=[]
   fenced=not fenced;continue
  if fenced:code.append(line);continue
  if line.startswith('|') and line.rstrip().endswith('|'):
   cells=line.strip().strip('|').split('|')
   if all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in cells):continue
   if inlist:blocks.append('</ul>');inlist=False
   if not table:blocks.append('<table><tbody>');table=True
   blocks.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in cells)+'</tr>');continue
  if table:blocks.append('</tbody></table>');table=False
  if re.match(r'^\s*[-*] ',line):
   if not inlist:blocks.append('<ul>');inlist=True
   blocks.append('<li>'+inline(re.sub(r'^\s*[-*] ','',line))+'</li>');continue
  if inlist:blocks.append('</ul>');inlist=False
  if not line.strip():continue
  heading=re.match(r'^(#{1,6})\s+(.+)',line)
  if heading:blocks.append('<h'+str(min(len(heading[1])+1,6))+'>'+inline(heading[2])+'</h'+str(min(len(heading[1])+1,6))+'>')
  else:blocks.append('<p>'+inline(line)+'</p>')
 if inlist:blocks.append('</ul>')
 if table:blocks.append('</tbody></table>')
 if code:blocks.append('<pre>'+esc('\n'.join(code))+'</pre>')
 return ''.join(blocks)

def build(candidates,dest):
 dest=dest.resolve()
 if dest.exists():raise ValueError('Release destination must not exist (immutable snapshots).')
 roots={slug:pathlib.Path(root).resolve(strict=True) for slug,root in candidates.items()}
 for slug,root in roots.items():
  if not re.fullmatch('[a-z][a-z0-9-]{0,40}',slug):raise ValueError('Invalid candidate slug')
  if dest.is_relative_to(root) or root.is_relative_to(dest):raise ValueError('Release and candidate source paths must be separate.')
 # Preflight every source before writing any private release.
 chosen={s:selected(p) for s,p in roots.items()};dest.mkdir(parents=True)
 site=dest/'site';(site/'assets').mkdir(parents=True);(site/'assets/portal.css').write_text(CSS+'\n.edit-link{display:inline-block;background:#174b70;color:#fff;padding:14px 18px;border-radius:10px;font-weight:700;text-decoration:none;min-height:44px;box-sizing:border-box}\n')
 now=stamp(datetime.datetime.now().timestamp());manifest={'snapshot_at':now,'files':[],'candidates':{}}
 for slug,root in roots.items():
  files,omitted=chosen[slug];known={f.relative_to(root).as_posix() for f in files};items={};name=slug.title();manifest['candidates'][slug]={'document_count':len(files),'omitted':omitted}
  for f in files:
   rel=f.relative_to(root);key=rel.as_posix();digest=sha(f);target=site/slug/'files'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
   if sha(target)!=digest or sha(f)!=digest:raise ValueError('Source changed during export: '+key)
   view=site/slug/'view'/(key+'.html');view.parent.mkdir(parents=True,exist_ok=True)
   original='/'+slug+'/files/'+quote(key,safe='/');changed=stamp(f.stat().st_mtime)
   title=f.stem.replace('-',' ').replace('_',' ')
   title=title[:160]
   prefix='<h1>'+esc(title)+'</h1><p class="muted">'+esc(name+' · '+key+' · source updated '+changed)+'</p><p><a href="'+original+'" download>Download original '+esc(f.suffix.upper())+'</a> · <a href="/'+slug+'/">Back to '+name+'</a></p><div class="notice">Source document preserved as provided. CV/application samples are drafts; confirm dates, facts and wording before sending. Search results and evaluations may be historical.</div>'
   if f.suffix.lower() in TEXT:
    text=target.read_text();body=render(text,rel,slug,known) if f.suffix.lower()=='.md' else '<pre>'+esc(text)+'</pre>'
    content=prefix+'<article class="document">'+body+'</article>'
   elif f.suffix.lower()=='.html':content=prefix+'<iframe sandbox title="Original document preview" src="'+original+'"></iframe>'
   else:content=prefix+'<div class="card"><p>This document is available in its original format.</p><a href="'+original+'">Open '+esc(f.suffix.upper())+' document</a></div>'
   view.write_text(page(name+' · '+title,content))
   items.setdefault(group(rel),[]).append('<li><a href="/'+slug+'/view/'+quote(key,safe='/')+'.html">'+esc(title)+'</a><span class="muted">'+esc(key+' · '+f.suffix.upper().lstrip('.')+' · '+changed)+'</span></li>')
 import importlib.util
 spec=importlib.util.spec_from_file_location('career_home',pathlib.Path(__file__).with_name('home.py'));landing=importlib.util.module_from_spec(spec);spec.loader.exec_module(landing)
 (site/'assets/home.css').write_text(landing.CSS)
 (site/'index.html').write_text(landing.start_page())
 for f in sorted(site.rglob('*')):
  if f.is_file():manifest['files'].append({'path':f.relative_to(dest).as_posix(),'sha256':sha(f),'size':f.stat().st_size})
 (dest/'manifest.json').write_text(json.dumps(manifest,indent=2))
 return manifest

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--candidate',action='append',required=True,metavar='NAME=PATH');p.add_argument('--output',required=True);a=p.parse_args()
 candidates=dict(v.split('=',1) for v in a.candidate)
 m=build(candidates,pathlib.Path(a.output));print(json.dumps({'snapshot_at':m['snapshot_at'],'documents':{s:v['document_count'] for s,v in m['candidates'].items()},'published_files':len(m['files'])}))
