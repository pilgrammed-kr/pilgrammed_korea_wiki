#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import sys,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ('a','link','script','img'):self.links.append(a.get('href') or a.get('src') or '')
errors=[];pages=[p for p in root.rglob('*.html') if not p.name.startswith('google') and '_site' not in p.relative_to(root).parts]
for p in pages:
 parser=Links();parser.feed(p.read_text())
 for link in parser.links:
  u=urlsplit(link)
  if not link or u.scheme or u.netloc or link.startswith(('#','/')):continue
  target=(p.parent/unquote(u.path)).resolve()
  if target.is_dir():target=target/'index.html'
  if target.is_relative_to(root) and not target.exists():errors.append(str(p.relative_to(root))+' -> '+link)
if '--production' in sys.argv:
 ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
 try:
  urls=ET.parse(root/'sitemap.xml').findall('.//s:loc',ns)
  if len(urls)!=len(pages):errors.append('sitemap page count')
 except Exception as e:errors.append('sitemap: '+str(e))
print('HTML pages:',len(pages),'broken paths:',len(errors))
for e in errors[:20]:print(e)
sys.exit(bool(errors))
