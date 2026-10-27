from pathlib import Path
import unittest,re,json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
class Release(unittest.TestCase):
 def test_source_and_storage(self):
  s=(ROOT/'index.html').read_text();d=json.loads(re.search(r'<script id="sourceData" type="application/json">(.*?)</script>',s,re.S)[1])
  self.assertEqual(len(d['atlasData']['current']),676);self.assertIn("storageKey='pilgrammed_v3_state'",s);self.assertNotIn('preview_state',s);self.assertIn('location.assign(path)',s);self.assertIn('V3.1.2',s);self.assertNotIn('한국어 공략과 획득처',s)
 def test_pending_and_removed(self):
  for n in ['beginner','junk-pits']:
   s=(ROOT/'guides'/f'{n}.html').read_text();main=re.search(r'<main>(.*?)</main>',s,re.S)[1];self.assertIn('준비 중입니다.',main);self.assertNotIn('<section>',main)
  for n in ['wayfinder','elite-guard']:self.assertFalse((ROOT/'guides'/f'{n}.html').exists())
  for p in ['items/wayfinder.html','techniques/elite-guard.html']:self.assertTrue((ROOT/p).is_file())
 def test_every_catalog_route(self):
  routes=json.loads((ROOT/'assets/guide-routes.json').read_text());self.assertEqual(len(routes),1335)
  for x in routes:self.assertTrue((ROOT/x['path']).is_file(),x['path'])
 def test_rebuild(self):
  files=[ROOT/'index.html',ROOT/'guides/beginner.html',ROOT/'guides/junk-pits.html',ROOT/'items/wayfinder.html',ROOT/'sitemap.xml']
  before={p:hashlib.sha256(p.read_bytes()).hexdigest()for p in files}
  subprocess.run([sys.executable,str(ROOT/'make_sitemap.py'),'https://pilgrammed-kr.github.io/pilgrammed_korea_wiki/'],check=True,stdout=subprocess.DEVNULL)
  for p in files:self.assertEqual(before[p],hashlib.sha256(p.read_bytes()).hexdigest(),str(p))
if __name__=='__main__':unittest.main()
