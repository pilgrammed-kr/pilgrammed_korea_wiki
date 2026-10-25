from pathlib import Path
root=Path(__file__).resolve().parents[1]
workflow=(root/'.github/workflows/deploy-pages.yml').read_text()
for required in ['assets','sw.js','manifest.webmanifest']:
 assert required in workflow,f'deployment does not copy {required}'
html=(root/'index.html').read_text()
assert 'id="release261LayoutFix"' in html,'late static sections must be placed inside information panel'
print('Deployment assets and late-section layout guard: PASS')
