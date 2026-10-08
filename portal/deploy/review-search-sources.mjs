// Exact, owner-approved repairs; no provider guessing or changes to search targeting.
import fs from 'node:fs';import path from 'node:path';import {randomUUID} from 'node:crypto';
import {createRequire} from 'node:module';import {pathToFileURL} from 'node:url';
export const code='/home/codex-deploy/apps/career-ops-editor/releases/20261007-experience-context-01';
export const repairs=[
 {name:'HubSpot',old:'https://job-boards.greenhouse.io/hubspot',oldApi:['https://boards-api.greenhouse.io/v1/boards/hubspot/jobs','https://boards-api.greenhouse.io/v1/boards/hubspot/jobs?content=true'],url:'https://www.hubspot.com/careers/jobs',coverage:'manual',reason:'Official careers page has openings; old Greenhouse endpoint returns 404. A replacement public feed was not verified.'},
 {name:'Hightouch',old:'https://job-boards.greenhouse.io/hightouch',oldApi:['https://boards-api.greenhouse.io/v1/boards/hightouch/jobs'],url:'https://hightouch.com/careers',coverage:'manual',reason:'Official custom career pages have openings. No feed verified against the official posting identities.'},
 {name:'Weights & Biases',old:'https://coreweave.com/careers/weights-biases',oldApi:[],url:'https://coreweave.com/careers/weights-biases',api:'https://boards-api.greenhouse.io/v1/boards/weights_and_biases/jobs?content=true',coverage:'automatic',reason:'Official W&B careers page directly requests this eight-posting Greenhouse feed.'},
];
export function repairDocument(p){
 const changed=[],already=[],skipped=[];
 for(const e of [...(p.tracked_companies||[]),...(p.job_boards||[])]){
  const r=repairs.find(r=>r.name===e.name);if(!r||e.enabled===false)continue;
  if(e.careers_url===r.url&&e.api===r.api&&e.hosted_review?.date==='2026-10-07'){already.push(e.name);continue;}
  if(e.careers_url!==r.old||(e.api&&!r.oldApi.includes(e.api))){skipped.push(e.name);continue;}
  e.careers_url=r.url;if(r.api)e.api=r.api;else delete e.api;
  e.hosted_review={date:'2026-10-07',coverage:r.coverage,reason:r.reason};changed.push(e.name);
 }
 return {changed,already,skipped};
}
export async function repairRoot(root,codeRoot=code,dryRun=false){
 const yaml=createRequire(path.join(codeRoot,'web/package.json'))('js-yaml');
 const {lock}=await import(pathToFileURL(path.join(codeRoot,'web/src/lib/hosted/store.mjs')));
 return lock(root,()=>{
  const file=path.join(root,'portals.yml');if(!fs.realpathSync(file).startsWith(fs.realpathSync(root)+path.sep))throw new Error('Source leaves candidate root');
  const before=fs.readFileSync(file,'utf8'),p=yaml.load(before),result=repairDocument(p);
  if(result.skipped.length)throw new Error('Reviewed source changed concurrently; no writes: '+result.skipped.join(', '));
  if(result.changed.length&&!dryRun){
   const dir=path.join(root,'.hosted/filter-history');fs.mkdirSync(dir,{recursive:true,mode:0o700});
   fs.writeFileSync(path.join(dir,Date.now()+'-'+randomUUID()+'.json'),JSON.stringify({at:new Date().toISOString(),before,operation:'review-source-addresses',principal:'owner-authorized'}),{mode:0o600,flag:'wx'});
   const tmp=file+'.'+randomUUID()+'.tmp';try{fs.writeFileSync(tmp,yaml.dump(p,{lineWidth:100,noRefs:true}),{mode:fs.statSync(file).mode&0o777});fs.renameSync(tmp,file);}finally{fs.rmSync(tmp,{force:true});}
  }
  return {candidate:path.basename(root),...result,dryRun,preserved:'targeting, unrelated sources, candidate facts and prior search receipts',manual:'HubSpot/Hightouch remain visible as unsupported in automated search coverage; use official links'};
 });
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(import.meta.filename)){
 const root=process.argv[2];if(![3,4].includes(process.argv.length)||(process.argv.length===4&&process.argv[3]!=='--check')||!/^\/var\/lib\/career-ops\/(brad|steve)$/.test(root))throw new Error('Fixed candidate root required');
 console.log(JSON.stringify(await repairRoot(root,code,process.argv[3]==='--check')));
}
