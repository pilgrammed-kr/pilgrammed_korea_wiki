#!/usr/bin/env python3
"""Build readable static pages from the unchanged embedded wiki data. Stdlib only."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import quote, urlsplit
import re, json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
BASE=(sys.argv[1] if len(sys.argv)>1 else 'https://pilgrammed-kr.github.io/pilgrammed_korea_wiki/').rstrip('/')+'/'
if urlsplit(BASE).scheme!='https':raise SystemExit('HTTPS 배포 주소가 필요합니다.')
source=(ROOT/'index.html').read_text()
m=re.search(r'<script\b(?=[^>]*\bid=["\']sourceData["\'])[^>]*>(.*?)</script>',source,re.S)
D=json.loads(m[1]); items=D['atlasData']['current']; bosses=D['b3Data']['bosses']; quests=D['quests414Data']['quests']; npcs=D['npcs413Data']; tech=D['b3Data']['tech']
E=lambda x:escape(str(x),quote=True)
def slug(n):
 s=re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
 return s or hashlib.sha256(n.encode()).hexdigest()[:12]
class Heading(HTMLParser):
 def __init__(self):super().__init__();self.on=False;self.title=''
 def handle_starttag(self,t,a):
  if t=='h1':self.on=True
 def handle_endtag(self,t):
  if t=='h1':self.on=False
 def handle_data(self,d):
  if self.on:self.title+=d
old={}
for p in (ROOT/'items').glob('*.html'):
 if p.name=='index.html':continue
 parser=Heading();parser.feed(p.read_text());old[parser.title.strip()]=p.relative_to(ROOT).as_posix()
ALIASES={'Wayfinder':'웨이파인더','Elite Guard':'엘리트 가드','Thief King':'도둑왕','Granny':'그래니','Purple Shark':'퍼플 샤크','Cata':'카타','Old Fart':'올드 파트','Democan':'데모칸','Misgiving':'미싱기브','Millennium Chimera':'밀레니엄 키메라','Magma Turtle':'마그마 터틀','Ice King':'아이스 킹','Nazar':'나자르','Junk Pits':'정크 피트','Lichenshire':'리켄셔','Vermeil Village':'시작 마을','Forest':'숲','Elite Barracks':'엘리트 병영'}
def label(x):
 n=x['name'] if isinstance(x,dict) else x
 ko=(x.get('ko_name') or x.get('ko')) if isinstance(x,dict) else None
 ko=ko or ALIASES.get(n)
 return (str(ko)+' · '+n) if ko and ko!=n else n
routes={}; groups={}
def register(kind,rows):
 used=set()
 for x in rows:
  n=x['name'];path=old.get(n) if kind=='items' else None
  path=path or kind+'/'+slug(n)+'.html'
  if path in used:path=kind+'/'+slug(n)+'-'+hashlib.sha256(n.encode()).hexdigest()[:8]+'.html'
  used.add(path);routes[(kind,n)]=path
 groups[kind]=rows
register('items',items);register('bosses',bosses);register('quests',quests);register('npcs',npcs);register('techniques',tech)
register('removed',D['atlasData'].get('removed',[]));register('unobtainable',D['atlasData'].get('unobtainable',[]));register('arrows',D['atlasData'].get('types',[]))
register('mobs',D['b3Data']['mobs']);register('guilds',D['atlas416Extra']['guilds'])
register('mirrors',[{'name':n,'location':ko}for n,ko in D['atlas416Extra']['mirrors']])
register('achievements',[{'name':n,'condition':condition}for n,condition in D['atlas416Extra']['achievements']])
register('skills',[{'name':n,**x}for n,x in D['skillDetailV24Data'].items()]);register('upgrades',D['masteries412Data'])
register('status',D['reference42Data']['statuses']);register('alchemy',D['reference42Data']['ingredients'])
register('fishing',D['reference42Data']['baits']+D['reference42Data']['fishing']['rods'])
register('mechanics',[{'name':n,'ko':ko,**D['systemGuideV21Data'].get(n,{})}for n,ko in D['atlas416Extra']['mechanics']])
regions={}
def region(n):
 n=re.sub(r'\s*\([^)]*\)', '', n).strip()
 if n and len(n)<100:regions.setdefault(n,{'name':n,'enemies':[],'items':[],'quests':[],'npcs':[]})
 return regions.get(n)
for x in bosses+D['b3Data']['mobs']:
 for n in re.split(r'\s*(?:→|,|/|·)\s*',x.get('area','')):
  r=region(n)
  if r:r['enemies'].append(x)
for kind,rows,field in [('items',items,'region'),('quests',quests,'region'),('npcs',npcs,'location')]:
 for x in rows:
  for n in re.split(r'\s*(?:→|,|/|·)\s*',x.get(field,'')):
   r=region(n)
   if r:r[kind].append(x)
regions={n:r for n,r in regions.items() if not re.search(r'[가-힣]',n) and len(n)<=48 and (r['enemies'] or len(r['items'])+len(r['quests'])+len(r['npcs'])>=2)}
# Preserve every original in-app location record, including compound/conditional labels.
for enemy in bosses+D['b3Data']['mobs']:
 for n in re.split(r',\s*',enemy.get('area','')):
  if not n:continue
  r=regions.setdefault(n,{'name':n,'enemies':[],'items':[],'quests':[],'npcs':[]})
  if enemy not in r['enemies']:r['enemies'].append(enemy)
register('regions',list(regions.values()))
# Use only exact, unambiguous references; short names remain plain text.
refs={}
for kind in ['items','bosses','quests','npcs','techniques','regions']+[k for k in groups if k not in ['items','bosses','quests','npcs','techniques','regions']]:
 for x in groups[kind]:refs.setdefault(x['name'],routes[(kind,x['name'])])
pattern=re.compile('|'.join(re.escape(n) for n in sorted(refs,key=len,reverse=True)if len(n)>3))
def text(v,prefix='../'):
 s=str(v);out=[];pos=0
 for match in pattern.finditer(s):
  a,b=match.span()
  if (a and re.match(r'[A-Za-z0-9_]',s[a-1])) or (b<len(s) and re.match(r'[A-Za-z0-9_]',s[b])):continue
  out.extend([E(s[pos:a]),f'<a href="{prefix}{E(refs[match[0]])}">{E(match[0])}</a>']);pos=b
 return ''.join(out)+E(s[pos:])
def para(v):return '<p>'+text(v)+'</p>' if v not in (None,'') else ''
def listing(v,ordered=False):
 if not v:return ''
 tag='ol' if ordered else 'ul'
 return '<'+tag+'>'+''.join('<li>'+text(x)+'</li>'for x in v)+'</'+tag+'>'
def section(title,body):return '<section><h2>'+E(title)+'</h2>'+body+'</section>' if body else ''
def cards(kind,rows):
 return '<ul class="cards">'+''.join('<li><a href="../'+E(routes[(kind,x['name'])])+'">'+E(label(x))+'</a></li>'for x in rows)+'</ul>'
def table(rows):return '<div class="tableWrap"><table><tbody>'+''.join('<tr><th scope="row">'+text(k)+'</th><td>'+text(v)+'</td></tr>'for k,v in rows if v is not None and v!='')+'</tbody></table></div>'
def evidence(x,extra=None):
 sources=[]
 for k in ['source','official_source','obtainment_source','stat_source','recipe_source']:
  if isinstance(x.get(k),str):sources.append(x[k])
 for row in x.get('sources',[]):
  if isinstance(row,dict) and row.get('url'):sources.append(row['url'])
  elif isinstance(row,str) and re.fullmatch(r'[A-Za-z0-9_]+',row):sources.append('https://pilgrammed.miraheze.org/wiki/'+row)
 if extra and isinstance(extra,dict)and extra.get('source'):sources.append(extra['source'])
 sources=list(dict.fromkeys(u for u in sources if isinstance(u,str)and urlsplit(u).scheme=='https'))
 date=x.get('official_checked_date') or x.get('checked_date')
 dates=[r.get('date')for r in x.get('sources',[])if isinstance(r,dict)and r.get('date')]
 if not date and dates:date=max(dates)
 body='<p>자료 기준: '+E(date or '항목별 원문 참고')+' · 기존 위키 자료를 재구성했습니다. 이번 개편에서 게임 내 이동·수치를 새로 검증한 것은 아닙니다.</p>'
 body+=para(x.get('official_verification_note')or x.get('recipe_note')or '')
 body+='<ul>'+''.join('<li><a href="'+E(u)+'" rel="noopener noreferrer">'+E(unescape(urlsplit(u).path.rsplit('/',1)[-1]).replace('_',' '))+' 원문 ↗</a></li>'for u in sources)+'</ul>'
 return section('출처와 확인 범위',body)
CSS='''*{box-sizing:border-box}body{margin:0;background:#10151e;color:#e8ecf3;font:16px/1.8 system-ui,-apple-system,"Noto Sans KR",sans-serif}a{color:#a9d2ff;text-underline-offset:4px}a:hover{color:#fff}a:focus-visible,input:focus-visible{outline:3px solid #dfbd77;outline-offset:3px}header,main,footer{width:min(100% - 40px,960px);margin:auto}header{padding:25px 0;border-bottom:1px solid #344153}header>a{font-weight:700;text-decoration:none}nav{display:flex;flex-wrap:wrap;gap:10px 22px;font-size:14px;margin-top:12px}main{padding:32px 0 64px}h1{font-size:clamp(26px,5vw,42px);line-height:1.3;margin:14px 0 20px;overflow-wrap:anywhere}h2{font-size:23px;line-height:1.4;margin:0 0 18px}h3{font-size:18px}section{margin:35px 0;padding-top:24px;border-top:1px solid #344153}p,li,td{overflow-wrap:anywhere}li{margin:7px 0}ul,ol{padding-left:24px}.eyebrow,.muted,footer{color:#a6b5c8;font-size:13px}.lead{font-size:18px;color:#c7d6e8;max-width:760px}.note{background:#1c2a3d;border-left:3px solid #a5c7f1;padding:15px 18px;border-radius:0 9px 9px 0}.cards{padding:0;list-style:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.cards li{margin:0}.cards a{display:block;background:#182230;border:1px solid #344153;border-radius:9px;padding:13px 16px;text-decoration:none;height:100%}.tableWrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:12px;border-bottom:1px solid #344153;text-align:left;vertical-align:top}th{width:32%;color:#bacce1}input{width:100%;padding:14px;background:#182230;border:1px solid #566b85;border-radius:8px;color:#fff;font:inherit}.badge.heart{background:#493e25;color:#f4d995}.badge{display:inline-block;padding:3px 10px;background:#243c57;border-radius:5px;color:#c2e2ff;font-size:14px}footer{padding:25px 0;border-top:1px solid #344153}@media(max-width:600px){body{font-size:15px}.cards{grid-template-columns:1fr}header,main,footer{width:calc(100% - 32px)}th,td{padding:9px}nav{gap:8px 16px}}'''
(ROOT/'assets/guide.css').write_text(CSS)
NAV=[('encyclopedia','전체 문서'),('guides','한국어 공략'),('items','아이템'),('bosses','보스'),('regions','지역'),('quests','퀘스트'),('npcs','NPC'),('techniques','테크닉')]
LABELS={**dict(NAV),'removed':'삭제된 아이템','unobtainable':'획득 불가 아이템','arrows':'화살 유형','mobs':'일반 몬스터','guilds':'길드','mirrors':'거울','achievements':'업적','skills':'스킬','upgrades':'어빌리티','status':'상태 효과','alchemy':'연금술 재료','fishing':'낚시 도구·미끼','mechanics':'게임 시스템'}
written=[]
def page(path,title,desc,body,kind='공략',search=False):
 url=BASE+quote(path,safe='/'); links=''.join('<a href="../'+k+'/index.html">'+v+'</a>'for k,v in NAV)
 script='''<script>const q=document.getElementById('filter');q?.addEventListener('input',()=>{const t=q.value.toLocaleLowerCase();document.querySelectorAll('.cards li').forEach(x=>x.hidden=!x.textContent.toLocaleLowerCase().includes(t))});</script>'''if search else ''
 data={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'필그램드 한국어 위키','item':BASE},{'@type':'ListItem','position':2,'name':title,'item':url}]}
 html='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' | 필그램드 한국어 위키</title><meta name="description" content="'+E(desc)+'"><link rel="canonical" href="'+E(url)+'"><meta property="og:title" content="'+E(title)+' | 필그램드 한국어 위키"><meta property="og:description" content="'+E(desc)+'"><meta property="og:type" content="article"><meta property="og:url" content="'+E(url)+'"><link rel="stylesheet" href="../assets/guide.css"><script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script></head><body><header><a href="../index.html">필그램드 한국어 위키</a><nav aria-label="분야별 문서">'+links+'</nav></header><main><p class="eyebrow">PILGRAMMED / '+E(kind)+'</p><h1>'+E(title)+'</h1><p class="lead">'+E(desc)+'</p>'+body+'</main><footer>비공식 팬 위키 · 게임 업데이트에 따라 정보가 달라질 수 있습니다. <a href="../copyright.html">출처·이용 안내</a> · 문서 구조 V3.1.0</footer>'+script+'</body></html>'
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html);written.append(path)
# Item URLs remain exactly the same. New static layout adds bidirectional links.
for item_kind in ['items','removed','unobtainable','arrows']:
 for x in groups[item_kind]:
  n=x['name'];body=section('획득처와 해금 조건',para(x.get('method'))+table([('지역',x.get('region')),('NPC',x.get('npc')),('가격',x.get('price'))])+para(x.get('obtainment_note')))
  body+=section('능력치',table(list(x.get('stats',{}).items())))+section('효과와 주의 사항',para(x.get('effect'))+para(x.get('note'))+para(x.get('build')))
  body+=section('제작 재료',listing([str(r.get('name'))+' ×'+str(r.get('count')) for r in x.get('recipe_parts',[])])+para(x.get('recipe_note')))
  droppers=[b for b in bosses if any(n in row.get('items',[]) for row in b.get('drop_table',{}).get('rows',[]))]
  body+=section('관련 보스',cards('bosses',droppers)if droppers else '')
  body+=section('이 재료를 사용하는 장비',cards('items',[i for i in items if any(r.get('name')==n for r in i.get('recipe_parts',[]))]))if any(any(r.get('name')==n for r in i.get('recipe_parts',[]))for i in items)else ''
  body+=section('낚시 위치',para(x.get('fishing_locations')))if isinstance(x.get('fishing_locations'),str)else ''
  if item_kind!='items':body='<p class="note">'+E(LABELS[item_kind])+' · 현행 일반 획득 아이템과 구분합니다.</p>'+body
  body+=evidence(x)
  page(routes[item_kind,n],label(x)+' 획득처·능력치',f"필그램드 {label(x)}의 획득 방법, {x.get('category','아이템')} 능력치와 제작 재료를 정리했습니다.",body,'아이템')
for enemy_kind in ['bosses','mobs']:
 for x in groups[enemy_kind]:
  n=x['name'];g=x.get('location_guide',{});c=D['combat416Data'].get(n,{})
  reward=D['souls417Data'].get('bosses',{}).get(n,{})
  soul=(('영혼' if reward.get('kind')=='heart'else'영혼 조각')+' ×'+str(reward.get('count',1))) if reward.get('kind')in ['heart','fragment']else ''
  body=('<p class="badge '+('heart'if reward.get('kind')=='heart'else'fragment')+'">'+E(soul)+'</p>'if soul else '')
  body+=section('위치와 출현 조건',para(g.get('start')or x.get('area'))+listing(g.get('requirements',[]))+listing(g.get('steps',[]),True)+para(g.get('note'))+para(g.get('review_note')))
  body+=section('기본 능력치',table([(k,x.get(v))for k,v in [('체력','hp'),('공격력','damage'),('방어력','defense'),('속성','element'),('골드','gold'),('경험치','xp'),('받는 피해 비율 (%)','damage_taken_pct'),('피해 감소율 (%)','damage_reduction_pct')]])+para(x.get('damage_taken_conflict')))
  body+=section('상태별 방어·피해 감소', ''.join(table([({'state':'상태','condition':'조건','defense_text':'방어력','reduction_text':'피해 감소','note':'주의','damage_taken_pct':'받는 피해 비율 (%)','damage_reduction_pct':'피해 감소율 (%)'}.get(k,k),v)for k,v in r.items()if k!='source'])for r in x.get('defense_profiles',[])))
  body+=section('보스 공략',para(c.get('overview'))+listing(c.get('phases',[]))+listing(c.get('tips',[])))
  body+=section('공격 패턴', ''.join('<h3>'+E(p.get('name',''))+'</h3>'+para(p.get('detail'))for p in c.get('patterns',[])))
  body+=section('막기·패링·회피', ''.join(table([(p.get('name','공격'),'막기 '+str(p.get('block','미기재'))+' / 패링 '+str(p.get('parry','미기재'))+' / 회피 '+str(p.get('dodge','미기재'))),('주의',p.get('note'))])for p in c.get('attacks',[])))
  rows=[]
  for r in x.get('drop_table',{}).get('rows',[]):
   chance=str(r['chance'])+'%'if r.get('chance')is not None else'확률 미기재'
   details='수량 '+str(r.get('quantity','미기재'))+' · '+chance
   if len(r.get('items',[]))>1:details+=' · 묶음 표기이며 개별 확률로 단정하지 않습니다.'
   if r.get('first_chance')is not None:details+=' · 첫 처치 '+str(r['first_chance'])+'%'
   details+=' · '+str(r.get('condition')or '일반 드롭')
   rows.append((' / '.join(r.get('items',[])),details))
  body+=section('드롭 아이템',table(rows)or para(x.get('drop_table',{}).get('state','드롭 정보 미기재')))+evidence(x,c)
  page(routes[enemy_kind,n],label(x)+(' 위치·보스 공략'if enemy_kind=='bosses'else' 위치·드롭 정보'),f"필그램드 {label(x)}의 출현 위치, 전투 패턴, 방어력, 드롭과 영혼 보상을 확인하세요.",body,'보스')
for x in quests:
 body=('<p class="note">'+E({'removed':'삭제된 퀘스트','event':'이벤트 퀘스트 · 현재 수주 가능 여부 확인 필요'}.get(x.get('state'),'일반 진행 자료'))+'</p>')
 body+=section('퀘스트 받는 방법',table([('NPC',x.get('npc')),('지역',x.get('region')),('유형',x.get('kind')),('선행 조건',x.get('requirements'))])+para(x.get('accept')))
 body+=section('진행 순서',listing(x.get('steps',[]),True))+section('보상',listing(x.get('rewards',[])))+section('주의 사항',para(x.get('note')))+section('연결 퀘스트',listing(x.get('related_quests',[])))+evidence(x)
 page(routes['quests',x['name']],label(x)+' 퀘스트·보상',f"필그램드 {label(x)} 퀘스트의 수주 NPC, 위치, 선행 조건, 진행 순서와 보상 안내입니다.",body,'퀘스트')
for x in npcs:
 body=section('위치와 찾아가는 방법',para(x.get('location'))+listing(x.get('steps',[]),True))+section('상점·서비스와 조건',para(x.get('service'))+para(x.get('condition')))
 body+=section('이 NPC의 퀘스트',cards('quests',[q for q in quests if x['name'] in q.get('npc','')]))+evidence(x)
 page(routes['npcs',x['name']],label(x)+' 위치·서비스',f"필그램드 {label(x)} NPC의 위치, 상점·서비스와 관련 퀘스트를 확인하세요.",body,'NPC')
for x in tech:
 body=section('획득 방법',para(x.get('place'))+para(x.get('require')))+section('효과와 사용 조건',table([('호환 무기',x.get('compat')),('마나',x.get('mana'))])+para(x.get('desc')))+evidence(x)
 page(routes['techniques',x['name']],label(x)+' 테크닉 얻는 법',f"필그램드 {label(x)} 테크닉의 획득처, 조건, 호환 무기와 효과 안내입니다.",body,'테크닉')
for x in regions.values():
 body='<p class="note">기존 기록에서 같은 지역으로 분류된 항목을 모았습니다. 지역명은 원문 표기를 유지하며, 서로 다른 하위 구역이 포함될 수 있습니다.</p>'
 body+=section('출현 보스',cards('bosses',[e for e in x['enemies']if e in bosses]))
 mobs=[e for e in x['enemies']if e not in bosses]
 body+=section('일반 몬스터',cards('mobs',mobs))
 body+=section('획득 기록이 있는 아이템',cards('items',x['items']))+section('관련 퀘스트',cards('quests',x['quests']))+section('관련 NPC',cards('npcs',x['npcs']))
 body+='<p class="muted">항목을 누르면 해당 자료의 획득 조건과 출처를 확인할 수 있습니다. 지역 분류만으로 모든 항목이 같은 장소에 있다는 뜻은 아닙니다.</p>'
 page(routes['regions',x['name']],label(x)+' 지역·획득처',f"필그램드 {label(x)} 지역에 연결된 보스, 몬스터, 아이템, 퀘스트와 NPC 기록입니다.",body,'지역')
# Remaining in-app categories all receive real static documents.
FIELD_LABELS={'manaFlat':'마나 회복량','manaPercent':'최대 마나 회복 (%)','buffs':'부여 효과','extra':'추가 효과','id':'효과','level':'강도','category':'분류','leader':'길드 대표','join':'가입 조건','levelup':'등급 올리는 방법','base_cost':'기본 비용','aced_cost':'에이스 비용','base':'기본 효과','aced':'에이스 효과','effect':'효과','effects':'효과','formula':'계산식','condition':'조건','location':'위치','requirement':'획득 조건','steps':'진행 순서','note':'주의 사항','lead':'개요','tips':'안내','range':'사거리','lure':'유인 수치','method':'획득 방법','potion':'포션 이름','type':'유형','kind':'종류','hpFlat':'체력 회복량','hpPercent':'최대 체력 회복 (%)','mpFlat':'마나 회복량','mpPercent':'최대 마나 회복 (%)','sickness':'포션 후유증 (초)','duration':'지속시간','durationSec':'지속시간 (초)','intellect':'지능','strength':'힘','defense':'방어력','agility':'민첩','projectileSize':'투사체 크기','manaRegen':'마나 회복','healthRegen':'체력 회복','damage':'피해량'}
def readable(v):
 if v is None:return '<span class="muted">미기재</span>'
 if isinstance(v,dict):return table([(FIELD_LABELS.get(k,k),format_inline(w))for k,w in v.items()])
 if isinstance(v,list):return listing([format_inline(w)for w in v])
 return para(v)
def format_inline(v):
 if isinstance(v,dict):return ' / '.join(FIELD_LABELS.get(k,k)+': '+format_inline(w)for k,w in v.items())
 if isinstance(v,list):return ' / '.join(format_inline(w)for w in v)
 return str(v) if v is not None else '미기재'
for kind in ['guilds','mirrors','achievements','skills','upgrades','status','alchemy','fishing','mechanics']:
 for x in groups[kind]:
  body=''
  if x.get('removed'):body+='<p class="note">삭제된 스킬 · 현행 스킬과 구분합니다.</p>'
  fields={'guilds':['location','leader','join','levelup'],'mirrors':['location'],'achievements':['condition'],'skills':['category','base_cost','base','aced_cost','aced'],'upgrades':['npc','location','requirement','effect','steps'],'status':['kind','effect','formula'],'alchemy':['potion','type','category'],'fishing':['kind','method','effects','range','lure'],'mechanics':['lead','steps','tips']}[kind]
  for key in fields:
   if key in x:body+=section(FIELD_LABELS.get(key,{'npc':'NPC'}.get(key,key)),readable(x[key]))
  if kind=='alchemy':
   body+=section('재료 수량별 단독 효과','<p>기존 표에서 확인된 결과만 표시합니다. 다른 재료와의 혼합 결과는 계산하지 않습니다.</p>'+''.join('<h3>'+E(qty)+'개</h3>'+readable(values)for qty,values in x.get('verified',{}).items()))
  if kind=='guilds':body+=section('등급별 보상',readable(x.get('rewards',{})))
  body+=section('주의 사항',para(x.get('note')))+section('관련 항목',listing(x.get('related',[])))
  if (kind,x['name'])!=('items',x['name']) and ('items',x['name'])in routes:body+=section('아이템 획득처·능력치',cards('items',[i for i in items if i['name']==x['name']]))
  if kind=='mechanics':body+=section('관련 도감', '<nav>'+''.join('<a href="../'+('regions'if k=='locations'else'techniques'if k=='tech'else k)+'/index.html">'+E(LABELS.get('regions'if k=='locations'else'techniques'if k=='tech'else k,k))+'</a> 'for k in x.get('links',[])if ('regions'if k=='locations'else'techniques'if k=='tech'else k)in groups)+'</nav>')
  body+=evidence(x)
  page(routes[kind,x['name']],label(x)+' '+LABELS[kind]+' 안내','필그램드 '+label(x)+'의 '+LABELS[kind]+' 정보, 조건과 기존 자료의 출처를 확인하세요.',body,LABELS[kind])
# Curated entry points contain only explanations supported by the existing data.
guides=[
 ('beginner','필그램드 초보자 진행 가이드','시작 마을에서 퀘스트, 장비, 곡괭이와 기본 서비스를 찾는 순서입니다.',section('첫 퀘스트와 도둑왕',cards('quests',[q for q in quests if q['name']in ['First Impressions','Thief Trouble','Mr Smith']]))+section('시작 마을의 서비스',cards('npcs',[x for x in npcs if x.get('location')=='Vermeil Village']))),
 ('wayfinder','웨이파인더(Wayfinder) 제작법·재료 획득처','제작 해금 조건과 필요한 재료를 한곳에서 확인하고 각 재료의 획득처로 이동하세요.',para(next(x for x in items if x['name']=='Wayfinder')['method'])+section('무기와 재료',cards('items',[x for x in items if x['name']in ['Wayfinder','Starshore Schematics','Lifesalt','Novacrystal','Onyx']]))+section('제작 NPC',cards('npcs',[x for x in npcs if x['name']=='Limo']))),
 ('elite-guard','엘리트 가드(Elite Guard) 얻는 법','테크닉 획득 조건과 엘리트 병영의 관련 NPC를 확인하세요.',section('획득 조건과 효과',cards('techniques',[x for x in tech if x['name']=='Elite Guard']))+section('병영 NPC',cards('npcs',[x for x in npcs if x['name']in ['Kyle','Trinks','Garth']]))),
 ('junk-pits','정크 피트 진입 준비·퀘스트 안내','입장 준비에 연결되는 카타 공략과 정크 피트 관련 퀘스트·지역 자료를 모았습니다.', '<p class="note">완전한 입장 동선을 새로 검증한 공략은 아닙니다. 각 퀘스트의 수주 조건과 기존 이동 안내를 함께 확인하세요.</p>'+section('카타 위치와 선행 구간',cards('bosses',[x for x in bosses if x['name']=='Cata']))+section('관련 퀘스트',cards('quests',[x for x in quests if any(w in json.dumps(x,ensure_ascii=False).lower()for w in ['junk pits','lichenshire','expedition'])]))+section('지역별 자료',cards('regions',[x for x in regions.values()if any(w in x['name'].lower()for w in ['junk','lichen','landfill','stonesurgeon'])]))),
 ('souls','필그램드 영혼·영혼 조각 보스 목록','보스가 주는 영혼과 영혼 조각을 구분하고 위치·공략으로 이동하세요.',section('영혼 보스',cards('bosses',[x for x in bosses if D['souls417Data'].get('bosses',{}).get(x['name'],{}).get('kind')=='heart']))+section('영혼 조각 보스',cards('bosses',[x for x in bosses if D['souls417Data'].get('bosses',{}).get(x['name'],{}).get('kind')=='fragment']))+'<p>보상 종류가 기록되지 않은 보스는 이 목록에서 제외했습니다.</p>'),
 ('old-fart','올드 파트(Old Fart) 위치·봉인 해제 안내','기존 자료의 선행 조건, 봉인 위치와 보스 공략을 확인하세요.',section('선행 조건과 이동 순서',cards('bosses',[x for x in bosses if x['name']in ['Old Fart','Highway Son']]))+section('관련 장비와 NPC',cards('items',[x for x in items if x['name']=='Gemstone Pickaxe'])+cards('npcs',[x for x in npcs if x['name']=='Ploma'])))
]
for key,title,desc,body in guides:
 if key=='beginner':
  body+=section('권장 확인 순서',listing(['First Impressions의 안내에 따라 Vermeil Village의 Abraska를 찾아가세요.','Thief Trouble에서 도둑 처치와 보스 처치 목표를 확인하세요.','채광 도구가 필요하면 Vergil의 Mr Smith에서 재료와 보상을 확인하세요.'],True))
 if key=='elite-guard':
  entry=next((x for x in tech if x['name']=='Elite Guard'),None)
  if entry:body+=section('어디서 어떻게 받나요?',para(entry.get('place'))+para(entry.get('require')))+section('사용 조건과 효과',para(entry.get('compat'))+para(entry.get('desc')))+evidence(entry)
 if key in ['old-fart','junk-pits']:
  entry=next(x for x in bosses if x['name']==('Old Fart'if key=='old-fart'else'Cata'));g=entry.get('location_guide',{})
  body+=section('기존 자료의 이동 안내',para(g.get('start'))+listing(g.get('requirements',[]))+listing(g.get('steps',[]),True)+para(g.get('review_note')))+evidence(entry)
 if key=='wayfinder':body+=evidence(next(x for x in items if x['name']=='Wayfinder'))
 page('guides/'+key+'.html',title,desc,body,'한국어 공략')
links='<ul class="cards">'+''.join('<li><a href="'+k+'.html">'+E(t)+'</a></li>'for k,t,_,_ in guides)+'</ul>'
page('guides/index.html','필그램드 한국어 공략 모음','초보자 진행, 장비 제작, 테크닉 획득과 보스 위치를 주제별로 찾아보세요.',links+section('전체 분야','<nav>'+''.join('<a href="../'+k+'/index.html">'+v+'</a>'for k,v in NAV if k!='guides')+'</nav>'),'공략 목차')
for kind,rows in groups.items():
 title=LABELS[kind]+' 도감·목차'
 page(kind+'/index.html',title,'필그램드 '+LABELS[kind]+' 문서를 이름으로 찾고 각 항목의 상세 안내를 확인하세요.','<label for="filter">이름 검색</label><input id="filter" type="search" placeholder="한글·영문 이름 입력">'+cards(kind,rows),'분야별 목차',True)
page('encyclopedia/index.html','필그램드 전체 문서 목차','아이템부터 몬스터, 스킬과 생활 시스템까지 모든 도감 항목을 개별 주소로 확인하세요.','<ul class="cards">'+''.join('<li><a href="../'+k+'/index.html">'+E(LABELS[k])+' · '+str(len(rows))+'개</a></li>'for k,rows in groups.items())+'</ul>','전체 문서')
# Add the same useful links to the rendered home and its initial HTML, once.
hub='<section class="searchGuideHub" aria-label="한국어 공략"><h2>한국어 공략과 획득처</h2><p>장비 제작, 보스 위치와 퀘스트를 개별 문서로 확인하세요.</p><nav>'+''.join('<a href="guides/'+k+'.html">'+E(t)+'</a>'for k,t,_,_ in guides)+'</nav><nav>'+''.join('<a href="'+k+'/index.html">'+v+' 전체 보기</a>'for k,v in NAV)+'</nav></section>'
source=re.sub(r'<!-- V310_HOME_START -->.*?<!-- V310_HOME_END -->','',source,flags=re.S)
source=re.sub(r'/\* V310_CSS_START \*/.*?/\* V310_CSS_END \*/','',source,flags=re.S)
source=source.replace('V3.0.0','V3.1.0')
source=source.replace('</section><div class="homeColumns">','</section><!-- V310_HOME_START -->'+hub+'<!-- V310_HOME_END --><div class="homeColumns">',1)
source=re.sub(r'(<main\b[^>]*\bid="content"[^>]*>).*?(</main>)',lambda m:m[1]+'<h1>필그램드 한국어 위키</h1><p>로블록스 필그램드(Pilgrammed)의 장비 획득처, 보스 공략, 퀘스트를 한국어로 정리한 비공식 팬 위키입니다.</p>'+hub+m[2],source,count=1,flags=re.S)
source=source.replace('</style>','/* V310_CSS_START */.searchGuideHub{margin:0 0 32px;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:12px}.searchGuideHub h2{margin-bottom:8px}.searchGuideHub p{color:var(--muted);font-size:12px}.searchGuideHub nav{display:flex;flex-wrap:wrap;gap:10px 20px;margin:14px 0}.searchGuideHub a{font-size:13px}/* V310_CSS_END */</style>',1)
title='필그램드 한국어 위키 | Pilgrammed 비공식 팬 위키'
description='로블록스 필그램드(Pilgrammed) 한국어 위키입니다. 무기와 장비 획득처, 보스 공략, 퀘스트, 지역과 제작 재료를 확인하세요.'
source=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',source,count=1,flags=re.S)
for tag,value in [('description',description),('og:title',title),('og:description',description)]:
 attr='property' if tag.startswith('og:') else 'name'
 source=re.sub(r'<meta\b(?=[^>]*\b'+attr+r'=["\']'+re.escape(tag)+r'["\'])[^>]*>','',source,flags=re.I)
 source=source.replace('</head>','<meta '+attr+'="'+tag+'" content="'+E(value)+'"></head>',1)
# A direct URL is also available from each supported in-app detail.
source=re.sub(r'/\* V310_ROUTES_START \*/.*?/\* V310_ROUTES_END \*/','',source,flags=re.S)
lookup={(('tech'if k=='techniques'else'locations'if k=='regions'else k)+'|'+n):p for(k,n),p in routes.items()}
routecode='/* V310_ROUTES_START */function staticDocUrl(e){return '+json.dumps(lookup,ensure_ascii=False)+"[e.kind+'|'+e.name]||'';}/* V310_ROUTES_END */"
source=source.replace('function detailView(e)',routecode+'function detailView(e)',1)
anchor="${staticDocUrl(e)?`<p><a class=\"button\" href=\"${E(staticDocUrl(e))}\">個別文書を開く</a></p>`:''}"
anchor=anchor.replace('個別文書を開く','개별 주소로 문서 열기')
if anchor not in source:source=source.replace('</header><div class="docColumns">','</header>'+anchor+'<div class="docColumns">',1)
(ROOT/'index.html').write_text(source)
(ROOT/'assets/guide-routes.json').write_text(json.dumps([{'kind':k,'name':n,'path':p}for(k,n),p in routes.items()],ensure_ascii=False))
print('정적 문서 생성:',len(written),'개; 보스',len(bosses),'퀘스트',len(quests),'지역',len(regions),'NPC',len(npcs),'테크닉',len(tech))

import subprocess
subprocess.run([sys.executable,str(ROOT/"tools/refine_v312.py")],check=True)
