// Owner-authorized exact-address repair. No targeting changes or automatic job publication.
import fs from 'node:fs';import path from 'node:path';import * as yaml from 'js-yaml';
import {lock} from '../../web/src/lib/hosted/store.mjs';
import {randomUUID} from 'node:crypto';
import {isMainModule} from '../../lib/is-main-module.mjs';
const replacements=[
 {name:'Temporal',old:'https://job-boards.greenhouse.io/temporal',oldApi:'https://boards-api.greenhouse.io/v1/boards/temporal/jobs',url:'https://jobs.ashbyhq.com/temporal',api:'https://api.ashbyhq.com/posting-api/job-board/temporal?includeCompensation=true'},
 {name:'RunPod',old:'https://job-boards.greenhouse.io/runpod',oldApi:'https://boards-api.greenhouse.io/v1/boards/runpod/jobs',url:'https://jobs.ashbyhq.com/runpod',api:'https://api.ashbyhq.com/posting-api/job-board/runpod?includeCompensation=true'},
 {name:'Runway',old:'https://job-boards.greenhouse.io/runwayml',oldApi:'https://boards-api.greenhouse.io/v1/boards/runwayml/jobs',url:'https://jobs.ashbyhq.com/runway-ml',api:'https://api.ashbyhq.com/posting-api/job-board/runway-ml?includeCompensation=true'},
 {name:'OpenAI',old:'https://openai.com/careers',url:'https://openai.com/careers',api:'https://api.ashbyhq.com/posting-api/job-board/openai?includeCompensation=true'},
 {name:'Lindy',old:'https://jobs.ashbyhq.com/lindy',url:'https://careers.lindy.ai'},
 {name:'Weights & Biases',old:'https://jobs.lever.co/wandb',url:'https://coreweave.com/careers/weights-biases'},
];
export function repairSources(root){return lock(root,()=>{const file=path.join(root,'portals.yml');if(!fs.realpathSync(file).startsWith(fs.realpathSync(root)+path.sep))throw new Error('Source escapes root');const before=fs.readFileSync(file,'utf8'),p=yaml.load(before),changed=[];
for(const e of p.tracked_companies||[]){const r=replacements.find(r=>r.name===e.name&&r.old===e.careers_url);if(!r||e.enabled===false||(r.api&&e.api===r.api)||(e.api&&e.api!==r.oldApi))continue;e.careers_url=r.url;if(r.api)e.api=r.api;else delete e.api;changed.push(e.name);}
if(changed.length){const dir=path.join(root,'.hosted/filter-history');fs.mkdirSync(dir,{recursive:true,mode:0o700});const id=Date.now()+'-'+randomUUID();fs.writeFileSync(path.join(dir,id+'.json'),JSON.stringify({at:new Date().toISOString(),before,operation:'repair-source-addresses',principal:'owner-authorized'}),{mode:0o600,flag:'wx'});const tmp=file+'.'+randomUUID()+'.tmp';try{fs.writeFileSync(tmp,yaml.dump(p,{lineWidth:100,noRefs:true}),{mode:0o600});fs.renameSync(tmp,file);}finally{fs.rmSync(tmp,{force:true});}}
return {candidate:path.basename(root),changed,preserved:'filters and unrelated sources',manualSources:['Lindy','Weights & Biases','Hightouch'].filter(x=>p.tracked_companies?.some(e=>e.name===x&&e.enabled!==false))};});}
if(isMainModule(import.meta.url)){const roots=process.argv.slice(2);if(roots.length!==1||!/^\/var\/lib\/career-ops\/(brad|steve)$/.test(roots[0]))throw new Error('Fixed candidate root required');console.log(JSON.stringify(repairSources(roots[0])));}
