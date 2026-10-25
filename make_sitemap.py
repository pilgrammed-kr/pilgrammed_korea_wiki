#!/usr/bin/env python3
"""python make_sitemap.py https://USER.github.io/pilgrammed_korea_wiki/"""
from pathlib import Path
import urllib.parse,sys,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
if len(sys.argv)!=2:raise SystemExit('사용법: python make_sitemap.py https://실제-HTTPS-배포주소/')
base=sys.argv[1].rstrip('/')+'/'
u=urllib.parse.urlparse(base)
if u.scheme!='https' or not u.hostname or u.hostname.endswith(('.example','.invalid','.test','localhost')) or u.username or u.password or u.query or u.fragment:
 raise SystemExit('실제 공개 HTTPS URL을 입력하세요. 예시/테스트 주소는 사용할 수 없습니다.')
root=Path(__file__).resolve().parent
pages=[root/'index.html',root/'copyright.html',root/'items/index.html']+sorted(p for p in (root/'items').glob('*.html') if p.name!='index.html')
urls=[]
for p in pages:
 rel=p.relative_to(root).as_posix();url=urllib.parse.urljoin(base,urllib.parse.quote(rel,safe='/'))
 soup=BeautifulSoup(p.read_text('utf-8'),'html.parser');head=soup.head
 for x in head.select('link[rel~=canonical]'):x.decompose()
 link=soup.new_tag('link',rel='canonical',href=url);head.append(link)
 for x in head.select('meta[property="og:url"]'):x.decompose()
 meta=soup.new_tag('meta');meta.attrs={'property':'og:url','content':url};head.append(meta)
 p.write_text(str(soup),encoding='utf-8')
 urls.append(url)
ns='http://www.sitemaps.org/schemas/sitemap/0.9'; ET.register_namespace('',ns)
xml=ET.Element('{%s}urlset'%ns)
for url in urls:ET.SubElement(ET.SubElement(xml,'{%s}url'%ns),'{%s}loc'%ns).text=url
ET.ElementTree(xml).write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+urllib.parse.urljoin(base,'sitemap.xml')+'\n',encoding='utf-8')
print('완료:',len(urls),'canonical URL과 sitemap')
