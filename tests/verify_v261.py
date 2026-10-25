from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,re
root=Path(__file__).resolve().parents[1]
new=BeautifulSoup((root/'index.html').read_text(),'html.parser')
critical={'name','canonical_name','aliases','ko','ko_name','id','source','official_source','url','ref','evidence_excerpt','value','stats','name_ko'}
def structural(v,key=''):
 if key in critical or isinstance(v,(int,float,bool)) or v is None:return v
 if isinstance(v,str):return '<prose>'
 if isinstance(v,list):return [structural(x,key) for x in v]
 if isinstance(v,dict):return {k:structural(x,k) for k,x in v.items()}
baseline=json.loads((root/'tests/data_integrity_v261.json').read_text())
for id,digest in baseline.items():
 value=structural(json.loads(new.find('script',id=id).get_text()))
 assert hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==digest,id
assert len(json.loads(new.find(id='atlasData').get_text())['current'])==676
text=(root/'index.html').read_text()+'\n'+''.join(p.read_text() for p in (root/'assets').glob('*.js'))
remaining={w for w in re.findall(r'[가-힣]+요(?=[.!?。…\s\"\'<>\\,]|$)',text) if not w.endswith('세요') and w not in {'필요','중요','주요','담요','소요'}}
assert not remaining,remaining
assert 'V2.6.0' not in (root/'index.html').read_text()
print('Preserved data schemas/identifiers/numbers/stats/evidence:',len(baseline),'datasets; items: 676; conversational endings: 0')
