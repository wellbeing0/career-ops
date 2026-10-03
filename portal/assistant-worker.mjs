// Detached, candidate-bound conversation worker. No shell/model tools are exposed.
import {readConversation} from '../web/src/lib/hosted/assistant.mjs';
import {executeAssistant} from '../web/src/lib/hosted/assistant-runner.mjs';
const [candidate,root,code,id,key]=process.argv.slice(2);if(!['brad','steve'].includes(candidate)||!root?.startsWith('/')||!code?.startsWith('/'))process.exit(1);
const c={candidate,root,code};for(let n=0;n<100;n++){if(readConversation(c,id).run?.pid===process.pid)break;await new Promise(r=>setTimeout(r,20));}
await executeAssistant(c,id,key);
