import fs from 'node:fs';import path from 'node:path';
import {isNestedCheckout} from './lib/mjs-files.mjs';import {getCareerOpsRoot} from './path-resolver.mjs';import {isMainModule} from './lib/is-main-module.mjs';
// Caller serializes this read with hosted editing, publication and backups.
export function exportCandidate(root,candidate){
 if(!['brad','steve'].includes(candidate))throw new Error('Unknown candidate');
 const search=path.join(root,'.hosted/search');if(fs.existsSync(search))for(const id of fs.readdirSync(search)){const f=path.join(search,id,'publication.json');if(fs.existsSync(f)&&JSON.parse(fs.readFileSync(f,'utf8')).status==='pending')throw new Error('Unfinished search publication');}
 const files=[];
 function visit(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.name.startsWith('.')||['node_modules','backups','reboot-checkpoints'].includes(e.name))continue;const f=path.join(dir,e.name);if(path.relative(root,f)==='data/cache'||e.isSymbolicLink())continue;if(e.isDirectory()){if(isNestedCheckout(f))continue;visit(f);}else if(!/\.(?:env|pem|key)$/i.test(e.name)&&!/(?:secrets|credentials)/i.test(e.name))files.push({path:path.relative(root,f).split(path.sep).join('/'),data:fs.readFileSync(f).toString('base64')});}}
 visit(root);return {format:'career-ops-candidate-export-v1',candidate,authority:'VPS',at:new Date().toISOString(),files};
}
if(isMainModule(import.meta.url)){try{process.stdout.write(JSON.stringify(exportCandidate(getCareerOpsRoot(),process.argv[2])));}catch(error){console.error(error.message);process.exitCode=1;}}
