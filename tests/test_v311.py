from pathlib import Path
from html.parser import HTMLParser
import re,unittest
ROOT=Path(__file__).resolve().parents[1]
class Content(HTMLParser):
 def __init__(self):super().__init__();self.anchors=[];self.summaries=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a':self.anchors.append(d.get('href',''))
  if t=='summary':self.summaries+=1
class Cleanup(unittest.TestCase):
 def test_direct_document_navigation(self):
  s=(ROOT/'index.html').read_text();a=s.index('function openDoc(');b=s.index('\nfunction ',a+12)
  self.assertIn('location.assign(url)',s[a:b]);self.assertNotIn("view='detail'",s[a:b])
  a=s.index('function rows(');b=s.index('\nfunction ',a+12)
  self.assertIn('<a class="documentRow" href=',s[a:b]);self.assertNotIn('<button class="documentRow"',s[a:b])
 def test_home_is_compact(self):
  s=(ROOT/'index.html').read_text();a=s.index('function homeView(');b=s.index('\nfunction ',a+12);home=s[a:b]
  self.assertNotIn('searchGuideHub',home);self.assertNotIn('toolTeaser',home);self.assertNotIn('heroMeta',home);self.assertIn('cleanHomeIndex',home)
 def test_guides_removed_from_listing(self):
  p=Content();p.feed((ROOT/'guides/index.html').read_text());self.assertNotIn('wayfinder.html',p.anchors);self.assertNotIn('elite-guard.html',p.anchors);self.assertIn('junk-pits.html',p.anchors)
 def test_document_has_no_overlay(self):
  s=(ROOT/'items/wayfinder.html').read_text();self.assertIn('docBar',s);self.assertNotIn('aria-label="분야별 문서"',s);self.assertNotIn('<dialog',s);self.assertIn('document-records.js',s)
  self.assertRegex(s,r'<details class="sources"><summary>');self.assertNotRegex(s,r'<details class="sources"[^>]*open')
 def test_all_directory_five_groups(self):
  s=(ROOT/'encyclopedia/index.html').read_text();self.assertEqual(s.count('class="categoryGroup"'),5)
 def test_guides_are_actionable(self):
  s=re.sub(r'<[^>]+>','',(ROOT/'guides/beginner.html').read_text())
  for term in ['Copper 4개','도둑 5마리','Abraska','Sticky Situation','Kyle','막혔을 때']:self.assertIn(term,s)
  s=re.sub(r'<[^>]+>','',(ROOT/'guides/junk-pits.html').read_text())
  for term in ['Soul Level 8','Journeyman','Broken Lever Piece','Highway Son','Betsy','Ull','엘리베이터','대화가 안 뜨거나']:self.assertIn(term,s)
if __name__=='__main__':unittest.main()
