import pathlib,importlib.util,unittest
p=pathlib.Path(__file__).resolve().parents[1]/'deploy/lock-openclaw-http.py';s=importlib.util.spec_from_file_location('boundary',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class BoundaryTests(unittest.TestCase):
 def test_blocks_all_v1_and_retains_owner_proxy_idempotently(self):
  old='openclaw.steveleclair.info {\n\tencode zstd gzip\n\treverse_proxy 127.0.0.1:18789\n}\n';new=m.restricted_config(old)
  self.assertIn('@career_private_ai path /v1 /v1/*',new);self.assertIn('respond @career_private_ai 404',new);self.assertIn('reverse_proxy 127.0.0.1:18789',new);self.assertEqual(m.restricted_config(new),new)
 def test_refuses_unknown_configuration(self):
  self.assertRaises(ValueError,m.restricted_config,'other.example {\n reverse_proxy 18789\n}')
