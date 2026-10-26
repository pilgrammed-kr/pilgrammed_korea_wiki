#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import tempfile,subprocess,sys
root=Path(__file__).resolve().parent
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.lang=False;self.title=False;self.description=False;self.in_title=False;self.collect=False;self.buf=[];self.scripts=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='html':self.lang=a.get('lang')=='ko'
  if t=='title':self.in_title=True
  if t=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
  if t=='script':self.collect=not a.get('src') and a.get('type','') in ('','text/javascript','module');self.buf=[]
 def handle_data(self,d):
  if self.in_title and d.strip():self.title=True
  if self.collect:self.buf.append(d)
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='script' and self.collect:self.scripts.append(''.join(self.buf));self.collect=False
errors=[];pages=[p for p in root.rglob('*.html') if not p.name.startswith('google') and '_site' not in p.relative_to(root).parts]
for p in pages:
 parser=Parser();parser.feed(p.read_text())
 if not (parser.lang and parser.title and parser.description):errors.append(str(p.relative_to(root))+': metadata')
 for code in parser.scripts:
  if not code.strip():continue
  with tempfile.NamedTemporaryFile(mode='w',suffix='.js') as f:
   f.write(code);f.flush();result=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
   if result.returncode:errors.append(str(p.relative_to(root))+': '+result.stderr[:200])
for p in [*(root/'assets').glob('*.js'),root/'sw.js']:
 result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
 if result.returncode:errors.append(str(p.relative_to(root))+': JS syntax')
print('HTML files:',len(pages));print('Metadata and JavaScript:', 'PASS' if not errors else 'FAIL')
for e in errors[:20]:print(e)
sys.exit(bool(errors))
