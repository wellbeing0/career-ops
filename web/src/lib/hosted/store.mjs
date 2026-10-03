import fs from 'node:fs';
import path from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import * as yaml from 'js-yaml';
export const digest = value => createHash('sha256').update(value).digest('hex');
export class StoreError extends Error { constructor(message, status=400) { super(message); this.status=status; } }
const FILES = ['cv.md','config/profile.yml','modes/_profile.md'];
const START='<!-- hosted-targeting:start -->',END='<!-- hosted-targeting:end -->';
const now = () => new Date().toISOString();
function atomic(file, content) { fs.mkdirSync(path.dirname(file),{recursive:true,mode:0o700}); const tmp=file+'.'+randomUUID()+'.tmp'; try {fs.writeFileSync(tmp,content,{mode:0o600});fs.renameSync(tmp,file);} finally {fs.rmSync(tmp,{force:true});} }
function revision(contents) { return digest(JSON.stringify(contents)); }
export function readSources(root) { return Object.fromEntries(FILES.map(name=>[name,fs.readFileSync(inside(root,name),'utf8')])); }
function mapping(text) { let value;try {value=yaml.load(text);}catch {throw new StoreError('Profile YAML is malformed; no changes made.',409);}if(!value||Array.isArray(value)||typeof value!=='object')throw new StoreError('Profile must be a YAML mapping.',409);return value; }
function inside(root,name) { if(!FILES.includes(name))throw new StoreError('This file cannot be edited.');const file=path.join(root,name);if(!fs.realpathSync(file).startsWith(fs.realpathSync(root)+path.sep))throw new StoreError('Source path escapes candidate root.',409);return file; }
export function lock(root,fn) {
 const dir=path.join(root,'.hosted');fs.mkdirSync(dir,{recursive:true,mode:0o700});
 const file=path.join(dir,'edit.lock');let fd;
 try{fd=fs.openSync(file,'wx',0o600);}catch(e){
  if(e.code!=='EEXIST')throw e;
  const guard=file+'.recovery';let guardFd;
  try{guardFd=fs.openSync(guard,'wx',0o600);}catch{throw new StoreError('Save lock is being checked; retry shortly.',503);}
  try{
   let stale=false;
   try{const owner=JSON.parse(fs.readFileSync(file,'utf8'));if(Number.isInteger(owner.pid)&&owner.pid>0){try{process.kill(owner.pid,0);}catch(error){stale=error.code==='ESRCH';}}}catch(error){if(error.code==='ENOENT')stale=true;}
   if(!stale)throw new StoreError('Another save is in progress; retry shortly.',503);
   fs.rmSync(file,{force:true});fd=fs.openSync(file,'wx',0o600);
  }finally{fs.closeSync(guardFd);fs.rmSync(guard,{force:true});}
 }
 try{fs.writeFileSync(fd,JSON.stringify({pid:process.pid,at:now()}));return fn(dir);}finally{fs.closeSync(fd);fs.rmSync(file,{force:true});}
}
function recover(root,dir) {const file=path.join(dir,'pending.json');if(!fs.existsSync(file))return;const tx=JSON.parse(fs.readFileSync(file));for(const [name,text] of Object.entries(tx.after)){inside(root,name);atomic(path.join(root,name),text);}audit(dir,tx);fs.rmSync(file);}
function audit(dir,tx) {const file=path.join(dir,'audit.jsonl');const entries=fs.existsSync(file)?fs.readFileSync(file,'utf8'):'';if(!entries.includes('"id":"'+tx.id+'"'))fs.appendFileSync(file,JSON.stringify({id:tx.id,at:tx.at,candidate:tx.candidate,principal:'shared-login',operation:tx.operation,before:tx.beforeRevision,after:tx.afterRevision})+'\n',{mode:0o600});}
export function targeting(profile) {return START+'\n## Current targeting — hosted structured profile\n\nSource: config/profile.yml; reviewed browser edits. Preserve source provenance in the narrative below.\n\n'+[
'Candidate: '+(profile.candidate?.full_name||''),
'Primary roles: '+(profile.target_roles?.primary||[]).join('; '),
'Base minimum: '+(profile.compensation?.minimum||''),
'Base target: '+(profile.compensation?.target_range||''),
'Currency: '+(profile.compensation?.currency||''),
'Location: '+(profile.candidate?.location||''),
'Remote/travel: '+(profile.compensation?.location_flexibility||''),
'Authorization: '+(profile.location?.visa_status||''),
'Citizenship: '+(profile.location?.citizenship||'Not supplied'),
'Sponsorship needed: '+String(profile.location?.needs_sponsorship??'Not supplied')
].join('\n\n')+'\n'+END;}
export function managedNarrative(profile,narrative) {if(narrative.includes(START)!==narrative.includes(END))throw new StoreError('Targeting block is incomplete; repair the narrative before saving.',409);const outside=narrative.replace(new RegExp(START+'[\\s\\S]*?'+END),'');return prepareNarrative(profile,outside.trimStart()).proposed;}
export function prepareNarrative(profile,narrative) {
 // Retain every original character in the private migration checkpoint; replace only recognized targeting sections.
 const sections=narrative.split(/(?=^## )/m);const retained=[];const removed=[];
 for(const section of sections){const heading=(section.split('\n')[0]||'').toLowerCase();if(/^## (?:target roles|your target roles|compensation|your comp targets|location and travel policy|location policy|your location policy|work authorization|north star)/.test(heading))removed.push(section);else retained.push(section);}
 return {proposed:targeting(profile)+'\n\n'+retained.join(''),removed};
}
export function readState(config) {return lock(config.root,dir=>{recover(config.root,dir);const contents=readSources(config.root);const profile=mapping(contents['config/profile.yml']);const trackerFile=path.join(config.root,'data/applications.md');const tracker=fs.readFileSync(trackerFile,'utf8');const states=yaml.load(fs.readFileSync(path.join(config.code,'templates/states.yml'),'utf8')).states.map(s=>s.label);return {candidate:config.candidate,contents,revision:revision(contents),profile,trackerRevision:digest(tracker),states,migrationNeeded:!contents['modes/_profile.md'].includes(START)};});}
function commit(config,dir,before,after,operation,operationId=null) {const id=operationId||Date.now()+'-'+randomUUID();const tx={id,at:now(),candidate:config.candidate,operation,beforeRevision:revision(before),afterRevision:revision(after),after};const history=path.join(dir,'revisions');fs.mkdirSync(history,{recursive:true,mode:0o700});atomic(path.join(history,id+'.json'),JSON.stringify({id,at:tx.at,operation,contents:before}));atomic(path.join(dir,'pending.json'),JSON.stringify(tx));for(const [name,text] of Object.entries(after)){if(before[name]!==text){inside(config.root,name);atomic(path.join(config.root,name),text);}}audit(dir,tx);fs.rmSync(path.join(dir,'pending.json'));return {ok:true,revision:tx.afterRevision,contents:after,profile:mapping(after['config/profile.yml'])};}
export function save(config,input,operationId=null) {if(operationId!==null&&!/^[0-9]+-[a-f0-9-]{36}$/.test(operationId))throw new StoreError('Invalid operation identifier.');return lock(config.root,dir=>{recover(config.root,dir);const before=readSources(config.root);if(input.revision!==revision(before))throw new StoreError('These files changed. Reload and compare; your unsaved text has been retained.',409);const after={...before};
 if(input.action==='cv'){if(typeof input.content!=='string'||Buffer.byteLength(input.content)>200000)throw new StoreError('CV must be text under 200KB.');after['cv.md']=input.content;}
 else if(input.action==='profile'){
  const p=mapping(before['config/profile.yml']);const fields=input.fields;if(!fields||typeof fields!=='object'||Array.isArray(fields))throw new StoreError('Profile fields required.');
  for(const k of ['name','email','phone','location','roles','minimum','target','currency','remote','authorization','citizenship'])if(typeof fields[k]!=='string'||fields[k].length>10000)throw new StoreError('Invalid '+k);
  if(!fields.name.trim()||!fields.roles.trim())throw new StoreError('Name and target roles are required.');
  p.candidate={...p.candidate,full_name:fields.name,email:fields.email,phone:fields.phone,location:fields.location};p.target_roles={...p.target_roles,primary:fields.roles.split('\n').map(s=>s.trim()).filter(Boolean)};
  p.compensation={...p.compensation,minimum:fields.minimum,target_range:fields.target,currency:fields.currency,location_flexibility:fields.remote};
  p.location={...p.location,visa_status:fields.authorization,citizenship:fields.citizenship,needs_sponsorship:fields.sponsorship===true};
  if(typeof input.narrative!=='string'||Buffer.byteLength(input.narrative)>200000)throw new StoreError('Narrative must be text under 200KB.');
  after['config/profile.yml']=yaml.dump(p,{lineWidth:100,noRefs:true});after['modes/_profile.md']=managedNarrative(p,input.narrative);
 }else if(input.action==='review-targeting') {if(input.confirm!==true)throw new StoreError('Review confirmation required.');if(before['modes/_profile.md'].includes(START))throw new StoreError('Targeting has already been reviewed.',409);after['modes/_profile.md']=prepareNarrative(mapping(before['config/profile.yml']),before['modes/_profile.md']).proposed;}
 else if(input.action==='restore'){if(!/^[0-9]+-[a-f0-9-]+$/.test(input.id||''))throw new StoreError('Invalid revision.');const backup=JSON.parse(fs.readFileSync(path.join(dir,'revisions',input.id+'.json'),'utf8'));Object.assign(after,backup.contents);mapping(after['config/profile.yml']);}
 else throw new StoreError('Operation disabled.');return commit(config,dir,before,after,input.action,operationId);});}
export function history(config,id) {return lock(config.root,dir=>{recover(config.root,dir);const folder=path.join(dir,'revisions');if(!fs.existsSync(folder))return [];if(id){if(!/^[0-9]+-[a-f0-9-]+$/.test(id))throw new StoreError('Invalid revision.');return JSON.parse(fs.readFileSync(path.join(folder,id+'.json'),'utf8'));}return fs.readdirSync(folder).filter(f=>f.endsWith('.json')).sort().reverse().map(f=>{const b=JSON.parse(fs.readFileSync(path.join(folder,f),'utf8'));return {id:b.id,at:b.at,operation:b.operation};});});}
export function updateTracker(config,input) {return lock(config.root,dir=>{recover(config.root,dir);const file=path.join(config.root,'data/applications.md');const before=fs.readFileSync(file,'utf8');if(digest(before)!==input.trackerRevision)throw new StoreError('Tracker changed. Reload before updating.',409);if(!/^\d+$/.test(String(input.n))||typeof input.status!=='string'||typeof input.note!=='string'||input.note.length>2000||/[|\r\n]/.test(input.note))throw new StoreError('Invalid tracker update.');
 const id=Date.now()+'-'+randomUUID();const backup=path.join(dir,'tracker-revisions');fs.mkdirSync(backup,{recursive:true,mode:0o700});atomic(path.join(backup,id+'.md'),before);
 const args=[path.join(config.code,'set-status.mjs'),'--row',String(input.n),input.status,'--source','web','--expected-revision',input.trackerRevision,'--json'];if(input.note.trim())args.push('--note',input.note.trim());
 try{execFileSync(process.execPath,args,{cwd:config.code,env:{...process.env,CAREER_OPS_ROOT:config.root,CAREER_OPS_TRACKER:file,CAREER_OPS_TRACKER_LOCK_TIMEOUT_MS:'5000'},timeout:15000,stdio:['ignore','pipe','pipe']});}catch(e){throw new StoreError('Tracker update refused; reload or retry. '+String(e.stdout||'').slice(-500),e.status===3?409:503);}
 const after=fs.readFileSync(file,'utf8');fs.appendFileSync(path.join(dir,'audit.jsonl'),JSON.stringify({id,at:now(),candidate:config.candidate,principal:'shared-login',operation:'tracker',before:digest(before),after:digest(after)})+'\n',{mode:0o600});return {ok:true};});}

export function savedAssistantOperation(config,id){return lock(config.root,dir=>{recover(config.root,dir);if(!/^[0-9]+-[a-f0-9-]{36}$/.test(id))throw new StoreError("Invalid operation identifier.");const file=path.join(dir,"revisions",id+".json");return fs.existsSync(file);});}
