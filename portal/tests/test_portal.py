import importlib.util,json,pathlib,tempfile,unittest,sys
BASE=pathlib.Path(__file__).resolve().parents[1]
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
builder=module('builder',BASE/'build.py');deploy=module('deploy',BASE/'deploy/activate.py')
class PortalTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=pathlib.Path(self.tmp.name)
  for c in ['steve','brad']:
   r=self.p/c;r.mkdir();(r/'cv.md').write_text('# '+c+'\n\n<script>alert(1)</script>\n[bad](javascript:alert)\n[safe](https://example.com)');(r/'data').mkdir();(r/'data/applications.md').write_text('# Tracker');(r/'output').mkdir();(r/'output/migration-backup').mkdir();(r/'output/migration-backup/old.md').write_text('privatebackup');(r/'.env').write_text('PASSWORD=secret');(r/'output/raw-browser.json').write_text('{}')
 def tearDown(self):self.tmp.cleanup()
 def build(self):return builder.build({c:str(self.p/c) for c in ['steve','brad']},self.p/'release')
 def test_separation_sources_and_exclusions(self):
  before=(self.p/'brad/cv.md').read_bytes();m=self.build();self.assertEqual(m['candidates']['brad']['document_count'],2);self.assertEqual(before,(self.p/'release/site/brad/files/cv.md').read_bytes());self.assertEqual(before,(self.p/'brad/cv.md').read_bytes());self.assertNotIn('steve', (self.p/'release/site/brad/files/cv.md').read_text());self.assertFalse((self.p/'release/site/brad/files/.env').exists());self.assertFalse((self.p/'release/site/brad/files/output/migration-backup').exists())
 def test_untrusted_markdown(self):
  self.build();s=(self.p/'release/site/brad/view/cv.md.html').read_text();self.assertNotIn('<script>',s);self.assertNotIn('href="javascript:',s);self.assertIn('&lt;script&gt;',s);self.assertIn('href="https://example.com"',s)
 def test_secret_content_fails_before_export(self):
  (self.p/'brad/cv.md').write_text('api_key: sk-proj-ABCDEFGHIJKLMNOP');self.assertRaises(ValueError,self.build);self.assertFalse((self.p/'release').exists())
 def test_symlink_escape_fails(self):
  (self.p/'outside.md').write_text('outside');(self.p/'brad/escape.md').symlink_to(self.p/'outside.md');self.assertRaises(ValueError,self.build)
 def test_tampering_preserves_activation(self):
  self.build();base=self.p/'app';(base/'releases').mkdir(parents=True);(self.p/'release').rename(base/'releases/r1');deploy.activate(base,'r1');self.assertEqual((base/'current').readlink(),pathlib.Path('releases/r1'));(base/'releases/r1/site/brad/files/cv.md').write_text('tampered');self.assertRaises(ValueError,deploy.activate,base,'r1');self.assertEqual((base/'current').readlink(),pathlib.Path('releases/r1'))
 def test_manifest_rejects_unlisted(self):
  self.build();(self.p/'release/site/surprise.txt').write_text('extra');self.assertRaises(ValueError,deploy.verify,self.p/'release')
 def test_release_is_immutable(self):
  self.build();self.assertRaises(ValueError,self.build)
if __name__=='__main__':unittest.main()
