import copy, importlib.util, pathlib, unittest
p=pathlib.Path(__file__).resolve().parents[1]/'deploy/align-steve-runtime.py'
s=importlib.util.spec_from_file_location('align',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class SteveAlignmentTests(unittest.TestCase):
    def fixture(self):
        return {'agents':{'entries':{'main':{'personal':'unchanged'},'career-brad':{'model':{'primary':'openai/gpt-6.1-sol'},'thinkingDefault':'medium'},'career-steve':{'model':{'primary':'openai/gpt-5.6-sol','fallbacks':['openrouter/fictional']},'tools':{'deny':['*'],'elevated':{'enabled':False}},'memory':{'search':{'enabled':False}},'heartbeat':{'every':'0m'}}}},'gateway':{'auth':'fictional-reference'},'skills':{'workshop':{'autonomous':{'mode':'propose'}}}}
    def test_exact_scope_and_idempotency(self):
        original=self.fixture(); before=copy.deepcopy(original); expected=copy.deepcopy(original)
        expected['agents']['entries']['career-steve']['model']['primary']='openai/gpt-6.1-sol'
        expected['agents']['entries']['career-steve']['thinkingDefault']='medium'
        self.assertEqual(m.aligned_config(original),expected); self.assertEqual(original,before)
        self.assertEqual(m.aligned_config(expected),expected)
    def test_changed_security_rejected(self):
        original=self.fixture(); original['agents']['entries']['career-steve']['tools']['deny']=[]
        self.assertRaises(ValueError,m.aligned_config,original)
