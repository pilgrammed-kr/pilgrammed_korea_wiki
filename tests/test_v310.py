"""Release contract: real pages, connected recipes/drops, unchanged source and safe rebuilds."""
from pathlib import Path
from html.parser import HTMLParser
import unittest,re,json,hashlib,subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.canonical=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a':self.links.append(d.get('href'))
  if t=='link'and d.get('rel')=='canonical':self.canonical.append(d.get('href'))
def parse(path):
 s=(ROOT/path).read_text();p=Tags();p.feed(s);return s,p
class Release(unittest.TestCase):
 def test_routes_unique_and_real(self):
  routes=json.loads((ROOT/'assets/guide-routes.json').read_text());paths=[x['path']for x in routes]
  self.assertEqual(len(paths),len(set(paths)))
  for path in paths:self.assertTrue((ROOT/path).is_file(),path)
  self.assertEqual(sum(x['kind']=='items'for x in routes),676)
  self.assertEqual(sum(x['kind']=='bosses'for x in routes),47)
  self.assertEqual(sum(x['kind']=='quests'for x in routes),55)
 def test_every_original_document_has_url(self):
  s=(ROOT/'index.html').read_text();d=json.loads(re.search(r'<script[^>]*id="sourceData"[^>]*>(.*?)</script>',s,re.S)[1])
  routes={(x['kind'],x['name'])for x in json.loads((ROOT/'assets/guide-routes.json').read_text())}
  expected=set()
  for key,kind in [('current','items'),('removed','removed'),('unobtainable','unobtainable'),('types','arrows')]:expected.update((kind,x['name'])for x in d['atlasData'].get(key,[]))
  for key,kind in [('bosses','bosses'),('mobs','mobs'),('tech','techniques')]:expected.update((kind,x['name'])for x in d['b3Data'][key])
  for x in d['b3Data']['bosses']+d['b3Data']['mobs']:expected.update(('regions',n)for n in re.split(r',\s*',x.get('area',''))if n)
  for key,kind in [('guilds','guilds'),('mirrors','mirrors'),('achievements','achievements'),('mechanics','mechanics')]:expected.update((kind,x['name']if isinstance(x,dict)else x[0])for x in d['atlas416Extra'][key])
  expected.update(('quests',x['name'])for x in d['quests414Data']['quests']);expected.update(('npcs',x['name'])for x in d['npcs413Data']);expected.update(('upgrades',x['name'])for x in d['masteries412Data']);expected.update(('skills',n)for n in d['skillDetailV24Data'])
  for key,kind in [('statuses','status'),('ingredients','alchemy'),('baits','fishing')]:expected.update((kind,x['name'])for x in d['reference42Data'][key])
  expected.update(('fishing',x['name'])for x in d['reference42Data']['fishing']['rods'])
  self.assertEqual(len(expected),1279)
  self.assertFalse(expected-routes,expected-routes)
 def test_recipe_and_reverse_links(self):
  _,way=parse('items/wayfinder.html');_,onyx=parse('items/onyx.html')
  self.assertIn('../items/onyx.html',way.links);self.assertIn('../items/wayfinder.html',onyx.links)
  _,boss=parse('bosses/thief-king.html')
  self.assertIn('../items/thief-king-cloak.html',boss.links)
 def test_reward_unknown_and_known(self):
  s,_=parse('bosses/granny.html');self.assertIn('영혼 조각 ×',s)
  s,_=parse('bosses/purple-shark.html');self.assertIn('영혼 조각 ×',s)
  s,_=parse('bosses/thief-king.html');self.assertIn('영혼 ×',s)
 def test_home_and_metadata(self):
  s,p=parse('index.html');self.assertIn('encyclopedia/index.html',p.links)
  self.assertIn('개별 주소로 문서 열기',s)
  self.assertNotRegex(re.search(r'<title>(.*?)</title>',s,re.S)[1],r'V?3\.[01]\.')
  self.assertIn('필그램드 한국어 위키',re.search(r'<title>(.*?)</title>',s,re.S)[1])
  self.assertIn("'pilgrammed_v3_state'",s)
 def test_sitemap_exact_and_canonical(self):
  urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').iter()if x.tag.endswith('}loc')]
  self.assertEqual(len(urls),len(set(urls)))
  canon=[]
  for folder in ['items', 'bosses', 'quests', 'regions', 'npcs', 'techniques', 'guides', 'encyclopedia', 'removed', 'unobtainable', 'arrows', 'mobs', 'guilds', 'mirrors', 'achievements', 'skills', 'upgrades', 'status', 'alchemy', 'fishing', 'mechanics']:
   for p in (ROOT/folder).glob('*.html'):
    _,tags=parse(p.relative_to(ROOT));self.assertEqual(len(tags.canonical),1,str(p));canon+=tags.canonical
  for path in ['index.html','copyright.html']:
   _,tags=parse(path);self.assertEqual(len(tags.canonical),1);canon+=tags.canonical
  self.assertEqual(set(urls),set(canon))
 def test_rebuild_idempotent_and_data_unchanged(self):
  files=[ROOT/'index.html',ROOT/'sitemap.xml',ROOT/'assets/guide-routes.json',ROOT/'items/wayfinder.html',ROOT/'bosses/cata.html']
  before={p:hashlib.sha256(p.read_bytes()).hexdigest()for p in files}
  s=(ROOT/'index.html').read_text();payload=re.search(r'<script[^>]*id="sourceData"[^>]*>(.*?)</script>',s,re.S)[1]
  subprocess.run([sys.executable,str(ROOT/'make_sitemap.py'),'https://pilgrammed-kr.github.io/pilgrammed_korea_wiki/'],check=True,stdout=subprocess.DEVNULL)
  for p,digest in before.items():self.assertEqual(digest,hashlib.sha256(p.read_bytes()).hexdigest(),str(p))
  self.assertEqual(payload,re.search(r'<script[^>]*id="sourceData"[^>]*>(.*?)</script>',(ROOT/'index.html').read_text(),re.S)[1])
if __name__=='__main__':unittest.main()
