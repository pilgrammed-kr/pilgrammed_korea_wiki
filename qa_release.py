#!/usr/bin/env python3
"""Offline release checks. Does not claim legal clearance or browser E2E."""
from pathlib import Path
from bs4 import BeautifulSoup
import subprocess, tempfile, sys, re
root=Path(__file__).resolve().parent
htmls = sorted(p for p in root.rglob('*.html') if not p.name.startswith('google'))
errors=[]
for p in htmls:
 s=BeautifulSoup(p.read_text('utf-8'),'html.parser')
 if not s.title or not s.title.get_text(strip=True):errors.append(f'{p}: title missing')
 if not s.find('meta',attrs={'name':'description'}):errors.append(f'{p}: description missing')
 if not s.find('html',attrs={'lang':'ko'}):errors.append(f'{p}: lang=ko missing')
 for tag in s.find_all('script'):
  if tag.get('src'):continue
  code=tag.string or tag.get_text()
  if not code.strip() or tag.get('type','').lower() not in ('','text/javascript','module'):continue
  with tempfile.NamedTemporaryFile(suffix='.js',mode='w',encoding='utf-8') as f:
   f.write(code);f.flush()
   r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
   if r.returncode:errors.append(f'{p.relative_to(root)}: JS syntax: {r.stderr[:150]}')
 if p==root/'index.html' and 'V2.6.0' not in p.read_text('utf-8'):errors.append('old version in main')
print('HTML files:',len(htmls))
print('JavaScript syntax and basic metadata checks:', 'PASS' if not errors else 'FAIL')
for err in errors[:20]:print('ERROR',err)
sys.exit(1 if errors else 0)
