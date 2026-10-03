import {hostedConfig} from '@/lib/hosted/policy.mjs';
import {assistantState,newConversation,sendAssistant,cancelAssistant,saveAssistantResponse} from '@/lib/hosted/assistant.mjs';
import {StoreError} from '@/lib/hosted/store.mjs';
export const runtime='nodejs';export const dynamic='force-dynamic';
function config(){const c=hostedConfig();if(!c)throw new StoreError('Hosted assistant is disabled.',403);return c;}
function error(e:unknown){return Response.json({error:e instanceof StoreError?e.message:'Assistant could not complete this request. Your saved work is retained.'},{status:e instanceof StoreError?e.status:500});}
export async function GET(req:Request){try{return Response.json(assistantState(config(),new URL(req.url).searchParams.get('id')),{headers:{'Cache-Control':'private, no-store'}});}catch(e){return error(e);}}
export async function POST(req:Request){try{const text=await req.text();if(Buffer.byteLength(text)>20000)throw new StoreError('Message is too large.',413);const input=JSON.parse(text),c=config();const result=input.action==='new'?newConversation(c):input.action==='send'?sendAssistant(c,input):input.action==='cancel'?cancelAssistant(c,input.id):input.action==='save-response'?saveAssistantResponse(c,input):null;if(!result)throw new StoreError('Unknown assistant operation.');return Response.json(result,{headers:{'Cache-Control':'private, no-store'}});}catch(e){return error(e);}}
