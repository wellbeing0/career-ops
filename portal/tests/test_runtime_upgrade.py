import unittest,pathlib,importlib.util,copy
p=pathlib.Path(__file__).resolve().parents[1]/'deploy/upgrade-career-runtime.py';s=importlib.util.spec_from_file_location('upgrade',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class RuntimeUpgradeTests(unittest.TestCase):
 def fixture(self):
  return {'agents':{'defaults':{'model':{'primary':'openai/gpt-6.1-sol'},'thinkingDefault':'high'},'entries':{'main':{},'career-steve':{'model':{'primary':'openai/gpt-5.6-sol'}},'career-brad':{'model':{'primary':'openai/gpt-5.6-sol','fallbacks':['openrouter/fictional']},'tools':{'deny':['*'],'elevated':{'enabled':False}},'memory':{'search':{'enabled':False}},'heartbeat':{'every':'0m'}}}},'gateway':{'auth':{'token':{'source':'store','provider':'default','id':'FICTIONAL_TOKEN'}}},'channels':{'telegram':{'enabled':True}}}
 def test_changes_only_brad_model_and_reasoning_preserving_security_fallback_and_other_agents(self):
  original=self.fixture();snapshot=copy.deepcopy(original);new=m.brad_config(original);self.assertEqual(original,snapshot)
  expected=copy.deepcopy(original);b=expected['agents']['entries']['career-brad'];b['model']['primary']='openai/gpt-6.1-sol';b['thinkingDefault']='medium';self.assertEqual(new,expected);self.assertEqual(m.brad_config(new),new)
 def test_changed_boundary_rejected(self):
  original=self.fixture();original['agents']['entries']['career-brad']['tools']['deny']=[];self.assertRaises(ValueError,m.brad_config,original)
