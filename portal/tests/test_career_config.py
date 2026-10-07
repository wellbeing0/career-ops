import unittest,importlib.util,pathlib
p=pathlib.Path(__file__).resolve().parents[1]/'deploy/career-agent-config.py';s=importlib.util.spec_from_file_location('career_config',p);module=importlib.util.module_from_spec(s);s.loader.exec_module(module)
class CareerConfigTests(unittest.TestCase):
 def test_preserves_personal_auth_model_memory_and_routes(self):
  old={'agents':{'defaults':{'model':{'primary':'openai/fixture','fallbacks':['openrouter/fixture']}},'entries':{'main':{'workspace':'/fictional/main'}}},'memory':{'search':{'provider':'openai-compatible','remote':{'baseUrl':'https://openrouter.ai/api/v1'}}},'channels':{'telegram':{'enabled':True,'botToken':'fictional-token'}},'gateway':{'auth':{'mode':'token','token':'fictional-token'}}}
  new=module.career_config(old,'/fictional/career')
  for key in ['channels','memory']:self.assertEqual(new[key],old[key])
  self.assertEqual(new['gateway']['auth'],old['gateway']['auth']);self.assertEqual(new['agents']['entries']['main'],old['agents']['entries']['main']);self.assertEqual(new['agents']['defaults']['model'],old['agents']['defaults']['model'])
  self.assertIn({'agentId':'main','match':{'channel':'telegram','accountId':'*'}},new['bindings'])
  for c in ['brad','steve']:
   agent=new['agents']['entries']['career-'+c];self.assertEqual(agent['tools']['deny'],['*']);self.assertEqual(agent['model']['fallbacks'],old['agents']['defaults']['model']['fallbacks']);self.assertFalse(agent['memory']['search']['enabled']);self.assertEqual(agent['heartbeat']['every'],'0m')
 def test_unreviewed_fleet_or_primary_is_rejected(self):
  self.assertRaises(ValueError,module.career_config,{'agents':{'entries':{'other':{}}}},'/fictional')
  self.assertRaises(ValueError,module.career_config,{'agents':{'entries':{'main':{}},'defaults':{'model':{'primary':'openrouter/paid'}}}},'/fictional')

 def test_existing_reviewed_agents_preserve_selected_models(self):
  old={'agents':{'defaults':{'model':{'primary':'openai/fixture','fallbacks':['openrouter/fixture']}},'entries':{'main':{}}}}
  initialized=module.career_config(old,'/fictional/career');initialized['agents']['entries']['career-brad']['model']['primary']='openai/gpt-6.1-sol';initialized['agents']['entries']['career-brad']['thinkingDefault']='medium'
  new=module.career_config(initialized,'/fictional/career');self.assertEqual(new['agents']['entries'],initialized['agents']['entries'])
