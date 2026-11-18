import json,re
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
SEARCH='https://careers.gene.com/us/en/search-results?keywords=%23ComputationCoE'
OUT=Path('roles.json'); META=Path('sync-meta.json')
def focus(title):
 t=title.lower()
 if 'lab automation' in t or 'robot' in t:return 'Lab Automation & Robotics'
 if 'agent' in t:return 'Agentic AI'
 if 'protein' in t or 'antibody' in t or 'biologic' in t:return 'Protein & Biologics ML'
 if 'reasoning' in t or 'foundation' in t or 'frontier' in t or 'foundational' in t:return 'Foundation & Reasoning Models'
 if 'structure' in t or 'simulation' in t or 'molecule' in t or 'synthesis' in t or 'therapeutics discovery' in t:return 'Molecular Design & Discovery'
 if 'biology' in t or 'genomic' in t or 'translation' in t or 'perturbation' in t:return 'Biology & Translation'
 if 'engineer' in t or 'devops' in t or 'infra' in t:return 'ML Engineering & Infrastructure'
 if 'product' in t or 'head' in t or 'leader' in t:return 'Scientific Product Leadership'
 return 'Computational Sciences'
def org(title):
 t=title.lower()
 if 'ai for drug discovery' in t or 'aidd' in t:return 'AI for Drug Discovery'
 if 'ai for biology' in t or 'aibt' in t or 'braid' in t:return 'AI for Biology & Translation'
 return 'Computational Sciences CoE'
def clean_location(text):
 lines=[re.sub(r'\s+',' ',x).strip() for x in text.splitlines() if x.strip()];loc=[]
 for x in lines:
  if re.search(r'(South San Francisco|New York City|Boston|Basel|Welwyn|Mississauga)',x,re.I):
   x=re.sub(r'^Location\s*','',x,flags=re.I);x=re.sub(r',\s*(California|New York|Massachusetts|Basel-City|Hertfordshire|Ontario),.*$','',x);loc.append(x)
 return ' or '.join(dict.fromkeys(loc)) or 'See official posting'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1200},user_agent='Mozilla/5.0')
 page.goto(SEARCH,wait_until='domcontentloaded',timeout=90000);page.wait_for_timeout(6000)
 for _ in range(12):page.mouse.wheel(0,1800);page.wait_for_timeout(400)
 anchors=page.locator('a[href*="/job/"]');found={}
 for i in range(anchors.count()):
  a=anchors.nth(i);href=a.get_attribute('href') or '';title=' '.join((a.inner_text() or '').split())
  if not title or len(title)<8:continue
  m=re.search(r'(20\d{4}-\d{6})',href+' '+title)
  if not m:continue
  req=m.group(1)
  if href.startswith('/'):href='https://careers.gene.com'+href
  txt=''
  try:txt=a.locator('xpath=ancestor::*[self::li or self::div][1]').inner_text()
  except:pass
  found[req]={'title':re.sub(r'\s+20\d{4}-\d{6}.*$','',title).strip(),'org':org(title),'location':clean_location(txt),'req':req,'url':href.split('?')[0],'focus':focus(title)}
 browser.close()
roles=list(found.values());roles.sort(key=lambda r:r['req'],reverse=True)
if len(roles)<10:raise SystemExit(f'Refusing to overwrite roles.json: only {len(roles)} roles scraped')
OUT.write_text(json.dumps(roles,indent=2)+'\n',encoding='utf-8')
META.write_text(json.dumps({'source':SEARCH,'count':len(roles),'lastSyncedUtc':datetime.now(timezone.utc).isoformat()},indent=2)+'\n',encoding='utf-8')
print(f'Synced {len(roles)} roles')
