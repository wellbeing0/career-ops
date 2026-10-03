// Isolated public-board preview. No application, model or shell-command capability.
import fs from 'node:fs';import path from 'node:path';import {spawn} from 'node:child_process';
import {jobDir,readJob,saveReceipt,rankOffers,cleanEnvironment,LIMITS} from '../web/src/lib/hosted/search.mjs';
import {lock} from '../web/src/lib/hosted/store.mjs';
const [root,candidate,id]=process.argv.slice(2);const code=path.resolve(import.meta.dirname,'..');const c={root,candidate,code},dir=jobDir(c,id);
const input=JSON.parse(fs.readFileSync(path.join(dir,'input.json'),'utf8'));
let receipt=readJob(c,id),halt=null;const children=new Set();const deadline=Date.now()+LIMITS.milliseconds;
async function checkpoint(){for(let i=0;i<100;i++){try{return lock(root,()=>saveReceipt(c,receipt));}catch(e){if(e.status!==503)throw e;await new Promise(r=>setTimeout(r,100));}}throw new Error('Workspace remained busy; search cannot save progress.');}
function stop(reason){halt=halt||reason;for(const child of children)child.kill('SIGTERM');}
const timer=setInterval(()=>{if(Date.now()>=deadline)stop('Time limit reached');if(fs.existsSync(path.join(dir,'cancel.json')))stop('Cancelled by visitor');},100);
process.on('SIGTERM',()=>stop('Service interrupted'));
async function board(b,index){
 const scratch=path.join(dir,'runtime',String(index));fs.mkdirSync(path.join(scratch,'config'),{recursive:true,mode:0o700});fs.mkdirSync(path.join(scratch,'data'),{mode:0o700});fs.writeFileSync(path.join(scratch,'config/profile.yml'),input.sources['config/profile.yml'],{mode:0o600});
 for(const [name,text] of Object.entries(input.dedup))fs.writeFileSync(path.join(scratch,name),text,{mode:0o600});
 fs.writeFileSync(path.join(scratch,'portals.yml'),JSON.stringify({...input.filters,tracked_companies:[b],job_boards:[]}));
 const result=await new Promise(resolve=>{let out='',overflow=false;const child=spawn(process.execPath,[path.join(code,'scan.mjs'),'--dry-run','--json','--quiet'],{cwd:scratch,env:cleanEnvironment(scratch,code),stdio:['ignore','pipe','ignore']});children.add(child);child.stdout.on('data',chunk=>{out+=chunk;if(out.length>2000000){overflow=true;child.kill('SIGTERM');}});child.on('error',()=>resolve({error:'Scanner could not start'}));child.on('close',exit=>{children.delete(child);try{const r=JSON.parse(out);if(!Array.isArray(r.offers))throw new Error();resolve({r,exit});}catch{resolve({error:overflow?'Board receipt exceeded resource limit':halt||'Board scanner did not return a valid receipt'});}});});
 if(result.r){const r=result.r;receipt.counts.found+=r.found||0;receipt.counts.filtered+=r.filtered||0;receipt.counts.duplicates+=r.duplicates||0;const errors=r.errors||[];receipt.sources.push({company:b.name,url:b.careers_url,status:errors.length||r.unverified_zero?.length?'failed':'completed',found:r.found||0,matches:r.added||0,filtered:r.filtered||0,duplicates:r.duplicates||0,filters:r.filter_counts||{},error:errors.map(e=>e.error).join('; ')|| (r.unverified_zero?.length?'No verified successful response':null),retrievedAt:new Date().toISOString()});const known=new Set(receipt.offers.map(o=>o.url));receipt.offers=rankOffers([...receipt.offers,...r.offers.filter(o=>!known.has(o.url)).map(o=>({...o,retrievedAt:new Date().toISOString()}))],input.targets);if(r.cap_hit||receipt.offers.length>=LIMITS.offers){receipt.offers=receipt.offers.slice(0,LIMITS.offers);stop('Result limit reached');}}
 else receipt.sources.push({company:b.name,url:b.careers_url,status:'failed',error:result.error,retrievedAt:new Date().toISOString()});
 await checkpoint();
}
try{
 // Wait for the parent to record PID before taking ownership of the receipt.
 for(let n=0;n<50;n++){receipt=readJob(c,id);if(receipt.pid===process.pid)break;await new Promise(r=>setTimeout(r,20));}
 receipt.status='running';await checkpoint();let next=0;
 await Promise.all(Array.from({length:LIMITS.concurrency},async()=>{while(next<input.boards.length&&!halt){const index=next++;await board(input.boards[index],index);}}));
 const failed=receipt.sources.some(s=>s.status!=='completed');const completed=receipt.sources.some(s=>s.status==='completed');
 receipt.status=halt==='Cancelled by visitor'?'cancelled':halt==='Service interrupted'?'interrupted':halt||input.boardCap?'partial':failed?(completed?'partial':'failed'):'completed';receipt.reason=halt||(input.boardCap?'Board limit reached':failed?'Some configured sources were unavailable or unsupported':null);receipt.finishedAt=new Date().toISOString();
 await checkpoint();
}catch{receipt.status='failed';receipt.reason='Search failed; retained results may be incomplete.';receipt.finishedAt=new Date().toISOString();try{await checkpoint();}catch{}}
finally{clearInterval(timer);for(const child of children)child.kill('SIGTERM');}
