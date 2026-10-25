"""Formalize Korean sentence endings without changing identifiers or evidence quotes."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
SPECIAL={'따라가요':'따라갑니다','바뀌어요':'바뀝니다',
'골라요':'고릅니다','깨요':'깹니다','끌려와요':'끌려옵니다','나와요':'나옵니다','나요':'납니까','나타나요':'나타납니다','남겨요':'남깁니다','낮춰요':'낮춥니다','내려와요':'내려옵니다','내려찍어요':'내려찍습니다','늘어요':'늘어납니다','달라요':'다릅니다','덮쳐요':'덮칩니다','돌아가요':'돌아갑니다','돌아다녀요':'돌아다닙니다','떨어져요':'떨어집니다','만나요':'만납니다','멈춰요':'멈춥니다','모아봐요':'모아 확인합니다','바꿔요':'바꿉니다','받아요':'받습니다','받아쳐요':'받아칩니다','밟아요':'밟습니다','베어요':'벱니다','보내요':'보냅니다','보여요':'보입니다','보여줘요':'보여줍니다','봐요':'확인합니다','붙어요':'붙습니다','뿌려요':'뿌립니다','생겨요':'생깁니다','쉬워요':'쉽습니다','쌓여요':'쌓입니다','써요':'사용합니다','쏴요':'발사합니다','아니에요':'아닙니다','아니요':'아닙니다','않아요':'않습니다','얻어요':'얻습니다','없어요':'없습니다','열려요':'열립니다','열어요':'엽니다','올라가요':'올라갑니다','와요':'옵니다','이어져요':'이어집니다','있나요':'있습니까','있어요':'있습니다','적어요':'적습니다','줄어요':'줄어듭니다','줄여요':'줄입니다','줘요':'줍니다','지켜요':'지킵니다','짧아져요':'짧아집니다','찾아봐요':'찾아봅니다','찾아요':'찾습니다','찾았나요':'찾았습니까','터져요':'터집니다','폭발시켜요':'폭발시킵니다','휘둘러요':'휘두릅니다','교체할까요':'교체하시겠습니까','복원할까요':'복원하시겠습니까','비울까요':'비우시겠습니까','사용하나요':'사용합니까','일으켜요':'일으킵니다','남겼어요':'남겼습니다','모았어요':'모았습니다','보여드려요':'보여드립니다'
}
NOUNS=set('강타다 개이다 공격이다 기준이다 내려찍기다 동작이다 레벨이다 무기다 미상이다 미확인이다 발이다 발차기다 배율이다 베기다 변수다 별도다 비용이다 상태명이다 수치이다 시스템이다 연타다 이다 자동화기다 초다 찌르기다 항목이다'.split())
# Commands ending in -세요 already use honorific speech and are retained.
def word(w):
 if w in SPECIAL:return SPECIAL[w]
 if w.endswith(('세요','십시오','니다')) or w in {'필요','중요','주요','담요'}:return w
 rules=[('했어요','했습니다'),('였어요','였습니다'),('었어요','었습니다'),('았어요','았습니다'),('이에요','입니다'),('예요','입니다'),('해져요','해집니다'),('져요','집니다'),('돼요','됩니다'),('해요','합니다'),('못해요','못합니다')]
 for suffix,out in rules:
  if w.endswith(suffix):return w[:-len(suffix)]+out
 if w.endswith('다'):
  if w in NOUNS:return (w[:-2] if w.endswith('이다') else w[:-1])+'입니다'
  if w.endswith('이다'):return w[:-2]+'입니다'
  if w.endswith('는다'):return w[:-2]+'습니다'
  stem=w[:-1]
  if not stem:return w
  code=ord(stem[-1])-0xAC00
  if not 0<=code<11172:return w
  final=code%28
  if final==4:return stem[:-1]+chr(ord(stem[-1])+13)+'니다'
  if final==0:return stem[:-1]+chr(ord(stem[-1])+17)+'니다'
  return stem+'습니다'
 return w
PAT=re.compile(r'[가-힣]+(?:요|다)(?=[.!?。…\s\"\'<>\\,]|$)')
changes={}
def prose(text):
 def replace(m):
  w=m[0]
  # Plain declarative -다 requires sentence punctuation to avoid nouns such as 바다.
  if w.endswith('다') and (m.end()==len(text) or text[m.end()] not in '.!?。'):return w
  new=word(w)
  if new!=w:changes[w]=new
  return new
 return PAT.sub(replace,text)
SKIP={'name','canonical_name','aliases','ko','ko_name','id','source','official_source','url','ref','evidence_excerpt','value','stats','name_ko'}
def json_prose(v,key=''):
 if key in SKIP:return v
 if isinstance(v,str):return prose(v)
 if isinstance(v,list):return [json_prose(x,key) for x in v]
 if isinstance(v,dict):return {k:json_prose(x,k) for k,x in v.items()}
 return v
def html(text):
 protected=[]
 def hold(m):
  block=m[0];match=re.match(r'(<script\b[^>]*>)(.*)(</script>)',block,re.S|re.I)
  try:payload=json.loads(match[2])
  except (ValueError,TypeError):return block
  protected.append(match[1]+json.dumps(json_prose(payload),ensure_ascii=False,separators=(',',':'))+match[3]);return f'@@JSONBLOCK{len(protected)-1}@@'
 text=re.sub(r'<script\b(?=[^>]*type=[\"\']application/json[\"\'])[^>]*>.*?</script>',hold,text,flags=re.S|re.I)
 text=prose(text)
 for i,block in enumerate(protected):text=text.replace(f'@@JSONBLOCK{i}@@',block)
 return text
if __name__=='__main__':
 count=0
 for path in root.rglob('*'):
  if not path.is_file() or '.git' in path.parts or path.suffix not in {'.html','.js'}:continue
  text=path.read_text();new=html(text) if path.suffix=='.html' else prose(text)
  if new!=text:path.write_text(new);count+=1
 print('Updated files:',count,'Endings:',len(changes))
 print(json.dumps(changes,ensure_ascii=False))
