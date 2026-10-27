#!/usr/bin/env python3
"""Generate guides, canonical URLs and sitemap with Python's standard library."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit,quote
import sys,re,subprocess,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('사용법: python make_sitemap.py https://실제-배포-주소/')
base=sys.argv[1].rstrip('/')+'/'
u=urlsplit(base)
if u.scheme!='https' or not u.hostname or u.username or u.password or u.query or u.fragment:raise SystemExit('올바른 HTTPS 배포 URL이 필요합니다.')
subprocess.run([sys.executable,str(root/'tools/build_guides.py'),base],check=True)
paths=[root/'index.html',root/'copyright.html']
for directory in ['items', 'bosses', 'quests', 'regions', 'npcs', 'techniques', 'guides', 'encyclopedia', 'removed', 'unobtainable', 'arrows', 'mobs', 'guilds', 'mirrors', 'achievements', 'skills', 'upgrades', 'status', 'alchemy', 'fishing', 'mechanics']:paths+=sorted((root/directory).glob('*.html'))
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);xml=ET.Element('{'+ns+'}urlset')
for p in paths:
 rel=p.relative_to(root).as_posix();url=base if rel=='index.html'else base+quote(rel,safe='/');s=p.read_text()
 s=re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>','',s,flags=re.I)
 s=re.sub(r'<meta\b(?=[^>]*\bproperty=["\']og:url["\'])[^>]*>','',s,flags=re.I)
 s=s.replace('</head>','<link rel="canonical" href="'+escape(url,quote=True)+'"><meta property="og:url" content="'+escape(url,quote=True)+'"></head>',1)
 p.write_text(s)
 ET.SubElement(ET.SubElement(xml,'{'+ns+'}url'),'{'+ns+'}loc').text=url
ET.ElementTree(xml).write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'sitemap.xml\n')
print('canonical 및 sitemap:',len(paths),'페이지')
