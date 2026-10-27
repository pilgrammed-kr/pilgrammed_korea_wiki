from pathlib import Path
from html import escape as E
import re,json
ROOT=Path(__file__).resolve().parents[1]
routes=json.loads((ROOT/'assets/guide-routes.json').read_text())
routeids={('tech'if x['kind']=='techniques'else'locations'if x['kind']=='regions'else x['kind'])+'|'+x['name']:x['path']for x in routes}
p=ROOT/'index.html';s=p.read_text()
s=re.sub(r'const STATIC_ROUTES=.*?;\n(?=function openDoc)', '',s)
a=s.index('function openDoc(id)');b=s.index('\n',a)
s=s[:a]+"const STATIC_ROUTES="+json.dumps(routeids,ensure_ascii=False)+";\nfunction openDoc(id){const e=byId.get(id);if(!e)return;const path=STATIC_ROUTES[id];if(!path)return;state.recent=[id,...state.recent.filter(x=>x!==id)].slice(0,30);save();location.assign(path)}"+s[b:]
compact='<nav class="quickGuides" aria-label="진행 공략"><span>공략</span><a href="guides/beginner.html">초보자 <small>준비 중</small></a><a href="guides/junk-pits.html">정크 피트 <small>준비 중</small></a><a href="guides/souls.html">영혼·영혼 조각</a><a href="guides/index.html" class="allGuides">전체 보기 →</a></nav>'
s=re.sub(r'<section class="searchGuideHub".*?</section>',lambda m:compact,s,flags=re.S)
s=re.sub(r'<nav class="quickGuides".*?</nav>',lambda m:compact,s,flags=re.S)
s=s.replace('V3.1.0','V3.1.2').replace('v3.1.0','v3.1.2')
css='<link rel="stylesheet" href="assets/refine-v312-app.css">'
if css not in s:s=s.replace('</head>',css+'</head>')
p.write_text(s)
for p in ROOT.rglob('*.html'):
 if p==ROOT/'index.html'or p.name.startswith('google')or any(x in p.parts for x in ['.git','_site']):continue
 s=p.read_text();rel=p.relative_to(ROOT)
 if len(rel.parts)!=2 and p.name!='copyright.html':continue
 if len(rel.parts)==2:
  back='index.html'if p.name!='index.html'else'../index.html'
  s=re.sub(r'<header\b[^>]*>.*?</header>','<header><a href="'+back+'">← 목록</a><a href="../index.html">필그램드 한국어 위키</a></header>',s,count=1,flags=re.S)
 css='<link rel="stylesheet" href="'+('../'if len(rel.parts)==2 else'')+'assets/refine-v312-article.css">'
 if css not in s:s=s.replace('</head>',css+'</head>')
 s=s.replace('V3.1.0','V3.1.2');p.write_text(s)
for key,title in [('beginner','초보자 공략'),('junk-pits','정크 피트 공략')]:
 p=ROOT/'guides'/f'{key}.html';s=p.read_text()
 s=re.sub(r'<main>.*?</main>','<main><p class="eyebrow">PILGRAMMED / 공략</p><h1>'+title+'</h1><p class="lead">준비 중입니다.</p><p>내용을 정리한 뒤 공개하겠습니다.</p><p><a href="index.html">공략 목록으로 돌아가기 →</a></p></main>',s,flags=re.S)
 s=re.sub(r'<title>.*?</title>','<title>'+title+' · 준비 중 | 필그램드 한국어 위키</title>',s,flags=re.S)
 s=re.sub(r'(<meta[^>]*(?:name="description"|property="og:description")[^>]*content=")[^"]*',lambda m:m[1]+title+'을 준비 중입니다.',s)
 s=re.sub(r'(<meta[^>]*property="og:title"[^>]*content=")[^"]*',lambda m:m[1]+title+' · 준비 중',s)
 s=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S);p.write_text(s)
for p in [ROOT/'guides/index.html',ROOT/'index.html']:
 s=p.read_text()
 s=re.sub(r'<li>\s*<a href="(?:guides/)?(?:wayfinder|elite-guard)\.html">.*?</a>\s*</li>','',s,flags=re.S)
 s=re.sub(r'<a href="(?:guides/)?(?:wayfinder|elite-guard)\.html">.*?</a>','',s,flags=re.S)
 for key,title in [('beginner','초보자'),('junk-pits','정크 피트')]:
  s=re.sub(r'(<a href="(?:guides/)?'+key+r'\.html">).*?(</a>)',lambda m:m[1]+title+' <small>준비 중</small>'+m[2],s)
 p.write_text(s)
for key in ['wayfinder','elite-guard']:(ROOT/'guides'/f'{key}.html').unlink(missing_ok=True)
p=ROOT/'sw.js';s=p.read_text().replace('3.1.0','3.1.2').replace('v310','v312');p.write_text(s)
print('V3.1.2 refinement applied')
