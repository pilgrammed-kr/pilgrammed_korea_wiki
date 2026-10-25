#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import sys, urllib.parse, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
html=list(root.rglob('*.html'))
errors=[]
for p in html:
 s=BeautifulSoup(p.read_text('utf-8'),'html.parser')
 for a in s.select('a[href]'):
  u=a.get('href','').strip()
  if not u or u.startswith(('#','mailto:','tel:','javascript:','data:')): continue
  q=urllib.parse.urlsplit(u)
  if q.scheme or q.netloc: continue
  if u.startswith('/'): continue # absolute path depends on deployment prefix; inspect during browser test
  target=(p.parent/urllib.parse.unquote(q.path)).resolve()
  if not target.is_relative_to(root.resolve()): continue
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.relative_to(root)} -> {u}')
if '--production' in sys.argv:
 sm=root/'sitemap.xml'
 if not sm.exists():errors.append('missing sitemap.xml')
 else:
  try:
   ns={'x':'http://www.sitemaps.org/schemas/sitemap/0.9'}
   t=ET.parse(sm)
   locs=[v.text for v in t.findall('.//x:loc',ns)]
   if len(locs)!=len(html):errors.append(f'sitemap count mismatch {len(locs)} vs {len(html)}')
   if any(not (u or '').startswith('https://') for u in locs):errors.append('non-HTTPS sitemap url')
  except Exception as e: errors.append('invalid sitemap '+str(e))
print('HTML pages:',len(html),'broken relative links:',len(errors))
for e in errors[:40]:print('ERROR',e)
sys.exit(1 if errors else 0)
