"""Editorial guides built from existing records; no invented unlock routes."""
def enhanced_guides(D,guides,section,para,listing,table,cards,evidence):
 quests={x['name']:x for x in D['quests414Data']['quests']};bosses={x['name']:x for x in D['b3Data']['bosses']}
 item={x['name']:x for x in D['atlasData']['current']}
 def quest(name):
  q=quests[name]
  return para(q.get('accept'))+listing(q.get('steps',[]),True)+section('완료하면 얻는 것',listing(q.get('rewards',[])))
 def route(name):
  g=bosses[name].get('location_guide',{})
  return para(g.get('start'))+listing(g.get('requirements',[]))+listing(g.get('steps',[]),True)
 def battle(name):
  c=D['combat416Data'].get(name,{})
  return para(c.get('overview'))+listing(c.get('tips',[]))
 beginner=para('처음 시작해 첫 보스와 기본 상점 서비스를 익히고, 엘리트 기사단 가입을 준비하는 안내입니다. 아래 순서는 이해하기 쉬운 권장 동선이며 모든 지역을 반드시 이 순서로 돌아야 하는 것은 아닙니다.')
 beginner+=section('먼저 볼 진행 순서',listing(['시작 동굴의 안내를 받고 시작 마을의 Abraska를 찾습니다.','Thief Trouble을 받고 도둑 5마리를 처치해 첫 무기를 선택합니다.','도둑왕을 처치하고 Abraska에게 완료를 보고합니다.','곡괭이·상점 서비스를 준비하고 동굴 퀘스트를 진행합니다.','완료한 퀘스트를 확인하고 엘리트 기사단 가입을 준비합니다.'],True))
 beginner+=section('1. 시작 마을에서 누구를 찾나요?',para('First Impressions를 진행하면 Vermeil Village의 Abraska에게 가라는 목표를 받습니다. 마을에 도착하면 아래 건물을 기준으로 필요한 NPC를 찾으세요.')+table([('북쪽 여관 · Abraska','침대 4개와 거울이 있는 건물입니다. 첫 진행 퀘스트 Thief Trouble을 받습니다.'),('동쪽 무기점 · Gerald','장비를 살펴보는 곳입니다. 건물 밖의 Vergil은 대장장이입니다.'),('남쪽 전당포 · Joe / Teller','Joe는 아이템 판매, Teller는 골드 보관을 담당합니다.'),('서쪽 건물 · Capillus','외형 변경 서비스를 찾을 때 방문합니다.')])+para('먼저 Abraska에게 퀘스트를 받은 뒤 밖으로 나가세요. 처음부터 멀리 이동하기보다 퀘스트 목표를 하나씩 완료하는 것을 권합니다.'))
 beginner+=section('2. 도둑 5마리와 첫 무기 선택',para(quests['Thief Trouble']['accept'])+listing(['The Prairie에서 Thief 5마리를 처치합니다.','Abraska에게 돌아와 진행 대화를 끝냅니다.','Bronze Greatsword, Wooden Bow, Magic Branch 중 하나를 고릅니다.','선물을 받은 뒤 도둑왕 조사 목표로 진행합니다.'],True)+para('무기 선택은 조작 취향을 익히는 단계로 생각하세요. 근접 공격을 연습하려면 Bronze Greatsword, 거리를 유지하고 싶으면 Wooden Bow, 마법 무기를 익히려면 Magic Branch를 먼저 비교해 볼 수 있습니다. 세 무기 중 하나가 모든 상황에서 가장 좋다는 의미는 아닙니다.')+cards('items',[item[n]for n in ['Bronze Greatsword','Wooden Bow','Magic Branch']if n in item]))
 beginner+=section('3. 첫 보스 도둑왕을 잡고 보고하기',route('Thief King')+battle('Thief King')+para('권장 연습: 먼저 공격을 피하거나 막을 타이밍을 보고, 안전한 틈에 짧게 공격하세요. 연속으로 맞는다면 공격 횟수를 줄여 패턴을 관찰하는 편이 좋습니다. 보스를 잡은 뒤에는 Abraska에게 돌아가 퀘스트 완료 대화까지 마치세요.')+section('퀘스트 완료 보상',listing(quests['Thief Trouble']['rewards']))+cards('bosses',[bosses['Thief King']]))
 beginner+=section('4. 곡괭이와 제작·재련 서비스 준비',para('시작 마을 동쪽 무기점 밖의 Vergil에게 Mr Smith를 확인하세요. Copper 4개와 Tin 2개를 제출하면 Bronze Pickaxe를 받고 상점·재련 서비스가 열립니다. 재료가 없다면 아래 각 재료 페이지의 획득처부터 확인하세요.')+cards('items',[item[n]for n in ['Copper','Tin','Bronze Pickaxe']if n in item])+para('권장 지출 순서: 먼저 사용할 무기와 필요한 도구를 확보한 뒤 방어구를 비교하세요. 초반에 장비를 자주 바꾼다면 재련에 가진 골드를 전부 사용하지 않는 편을 권합니다. 이 지출 순서는 공략상의 제안입니다.'))
 beginner+=section('5. 다음 목표: 슬라임 동굴 퀘스트',quest('Sticky Situation')+para('동굴을 조사한 뒤 보고하는 단계와 보스를 처치하는 단계를 구분하세요. 조사만 하고 끝난 것으로 생각하지 말고 Archer와 다시 대화해 현재 목표를 확인하세요.')+battle('Yalgaroth')+cards('bosses',[bosses['Yalgaroth']]))
 beginner+=section('6. 엘리트 기사단 가입 준비',para('Elite Knights는 Thief Trouble, The Outlaw Torn, Down In Flames, Sticky Situation, Hunting Hunters 중 2개를 완료한 뒤 Kyle에게 가입을 요청하는 조건입니다. 위 안내대로 Thief Trouble과 Sticky Situation을 완료했다면 가입 조건을 확인해 보세요.')+para('Kyle은 Forest 해안의 Theodore 오두막 근처 언덕 아래 Elite Barracks 내부에 있습니다. 붉은 피부와 뿔이 있는 기사를 찾으세요.')+cards('npcs',[x for x in D['npcs413Data']if x['name']=='Kyle'])+para('가입과 Journeyman 승급은 서로 다른 단계입니다. 정크 피트 원정대처럼 Journeyman을 요구하는 진행은 가입만으로 바로 열리지 않습니다.'))
 beginner+=section('막혔을 때 확인할 것',table([('보스를 잡았는데 퀘스트가 그대로입니다.','퀘스트를 먼저 수주했는지, 처치 후 NPC에게 완료를 보고했는지 확인하세요.'),('장비가 있어도 같은 자리에서 계속 죽습니다.','해당 보스 문서의 공격 패턴과 막기·패링·회피 판정을 확인하세요. 막을 수 없는 공격을 일반 막기로 버티려 하지 마세요.'),('어디로 가야 할지 모르겠습니다.','현재 퀘스트 문서의 수주 NPC·지역·진행 순서를 확인하세요. 동굴의 세부 구간은 보스 위치 문서와 함께 보세요.'),('성장이 안 되는 것 같습니다.','일반 경험치 보상과 영혼·영혼 조각 보상을 구분하고 보스 보상 목록을 확인하세요.')]))
 beginner+=section('이 다음에는',para('첫 퀘스트와 장비 사용법에 익숙해지면 보스 보상·길드 진행·지역 퀘스트 중 다음 목표를 정하세요. 정크 피트는 여러 선행 조건이 있는 후속 진행이므로, 먼저 정크 피트 가는 법의 준비 목록부터 확인하는 것이 좋습니다.')+'<p><a href="junk-pits.html">정크 피트 가는 법 →</a></p><p><a href="souls.html">영혼·영혼 조각 보스 목록 →</a></p>')
 beginner+=evidence({'sources':[r for name in ['Thief Trouble','Mr Smith','Sticky Situation']for r in quests[name].get('sources',[])]})
 junk=para('정크 피트는 Village of Ravine의 엘리베이터에서 Ull의 Falling Down 진행을 통해 들어갑니다. 카타만 처치하면 바로 입장하는 방식이 아니라, 선행 보스·소울 레벨·대장장이 영입 조건을 함께 확인해야 합니다.')
 junk+=section('출발 전 준비 목록',listing(['Soul Level 8에 도달했는지 확인하세요.','Highway Son을 처치한 뒤 Elite Barracks에서 대화하세요.','Sweetberry Catacombs의 Cata를 처치하세요.','Old Fart 처치 조건을 충족하세요.','Betsy 영입을 위해 Elite Knights Journeyman 이상을 준비하세요.']))
 junk+=section('1. Highway Son 처치 후 병영 대화',route('Highway Son')+para('보스 처치와 병영에서의 NPC 대화는 별개입니다. 처치만 하고 엘리베이터로 가지 말고 Elite Barracks에서 Highway Son과 대화했는지 확인하세요.')+cards('bosses',[bosses['Highway Son']]))
 junk+=section('2. 카타 진입 준비: 리모의 도구상자',quest('Hardy Hardware')+para('Catacombs Key는 이 퀘스트에서 도구상자를 Limo에게 돌려주면 얻습니다. 열쇠를 준비한 뒤 Sweetberry Catacombs 구간을 진행하세요.')+cards('items',[item[n]for n in ['Catacombs Key','Broken Lever Piece']if n in item]))
 junk+=section('초입 레버를 찾고 있다면',para('공식 위키에는 첫 Armored Twigface를 만난 뒤 오른쪽 갈래에 있는 첫 레버가 필수는 아니지만 이용을 권장하는 것으로 설명돼 있습니다. 이 초입 레버와 감옥 안 Broken Lever Piece로 수리하는 레버를 구분하세요.')+para('지역 문서의 일부 검색 색인만 확인한 내용입니다. 나머지 레버의 정확한 동선은 원문 또는 실제 지형과 함께 확인하세요.'))
 junk+=section('3. 감옥 레버와 카타 보스방',route('Cata')+para('Broken Lever Piece는 감옥 내부의 Tomb를 조사해 얻는 재료입니다. 처음 구간의 잠긴 문, 레버 수리, 보스방까지의 이동을 한 번에 같은 단계로 생각하지 말고 현재 막힌 지점을 확인하세요. 아래 보스방 동선은 감옥 레버 수리 이후 구간을 기준으로 합니다.')+cards('bosses',[bosses['Cata']]))
 junk+=section('4. 올드 파트 봉인 해제와 처치',route('Old Fart')+para('Ploma의 봉인 안내와 관련 위치를 확인하고 이동하세요. 붉고 흰 버섯 근처의 약한 벽 뒤에 있는 문양은 위치별로 찾아야 합니다. 자세한 보스 패턴은 개별 문서에서 확인할 수 있습니다.')+'<p><a href="old-fart.html">올드 파트 봉인 해제 안내 →</a></p>'+cards('bosses',[bosses['Old Fart']]))
 junk+=section('5. Village of Ravine의 Ull에게 출발 요청',para('선행 조건을 갖춘 뒤 Village of Ravine의 엘리베이터 앞 Ull과 대화하세요. 엘리베이터가 무엇인지 묻고 아래로 내려가고 싶다는 대화를 진행하면 원정대 대장장이 영입을 부탁받습니다.')+para('Ull에게 영입 부탁을 받기 전과 받은 뒤의 대화는 다릅니다. Betsy에게 먼저 갔는데 원정대 대화가 없다면 이 단계를 확인하세요.'))
 junk+=section('6. 벳시를 원정대에 영입하기',para('Elite Barracks 복도 맨 끝 방의 대장장이 Betsy를 찾으세요. Falling Down이 진행 중이고 Elite Knights Journeyman 이상일 때 원정대 대장장이 영입 대화를 확인할 수 있습니다.')+listing(['Ull에게 대장장이 영입 부탁을 받습니다.','엘리트 병영의 Betsy에게 원정대 합류를 제안합니다.','Village of Ravine의 Ull에게 돌아가 영입을 보고합니다.'],True)+cards('npcs',[x for x in D['npcs413Data']if x['name']=='Betsy']))
 junk+=section('7. 엘리베이터를 타고 리켄셔 도착',para('Ull에게 보고한 뒤 엘리베이터 장면을 거치면 Junk Pits의 Lichenshire에 도착합니다. 도착 후 Ull과 대화를 마치고 거점의 NPC와 서비스를 확인하세요.')+para('정크 피트 진입 뒤의 Morline 제작 등은 별도 후속 퀘스트입니다. 입장 조건과 입장 후 진행을 구분하세요.')+cards('quests',[quests['Falling Down'],quests['Making A Morline']]))
 junk+=section('대화가 안 뜨거나 출발할 수 없을 때',table([('Ull이 출발시켜 주지 않습니다.','Soul Level 8, Highway Son 처치 후 병영 대화, Cata, Old Fart 조건을 다시 확인하세요.'),('Betsy에게 영입 대화가 없습니다.','Falling Down에서 Ull의 부탁을 받았는지, 길드 등급이 Journeyman 이상인지 확인하세요.'),('벳시에게 말했는데 진행이 그대로입니다.','Ull에게 돌아가 영입 보고를 해야 합니다.'),('카타가 있는 구간에 못 들어갑니다.','Hardy Hardware의 열쇠 획득과 감옥의 Broken Lever Piece·레버 수리 단계를 구분해 확인하세요.')]))
 junk+=para('자료 안내: 선행 조건과 퀘스트 순서는 기존 퀘스트·NPC 자료를 재구성했습니다. 2026-10-27 공식 위키 검색 색인에서 Ull의 일부 조건과 Betsy의 Journeyman 영입 조건을 부분 대조했습니다. 공식 문서 본문 접근이 제한되어 모든 대화와 이동 경로를 새로 전수 검증한 것은 아닙니다.')
 junk+=evidence({'checked_date':'2026-10-23','sources':[r for name in ['Falling Down','Hardy Hardware']for r in quests[name].get('sources',[])]+[{'url':'https://pilgrammed.miraheze.org/wiki/Sweetberry_Catacombs','date':'2026-10-27'}],'official_verification_note':'2026-10-27 추가 대조 범위: Ull의 일부 조건, Betsy의 길드 등급 조건, 초입 첫 레버의 선택 여부와 Armored Twigface 기준 방향. 나머지 내용은 기존 자료 기준입니다.'})
 out=[]
 for key,title,desc,body in guides:
  if key=='beginner':title='필그램드 초보자 공략 · 시작부터 첫 길드까지';desc='첫 퀘스트, 무기 선택, 도둑왕, 곡괭이와 길드 준비를 순서대로 안내합니다.';body=beginner
  if key=='junk-pits':title='정크 피트 가는 법 · 선행 조건과 엘리베이터';desc='소울 레벨, 선행 보스, 도구상자·열쇠, 벳시 영입과 리켄셔 도착까지 단계별 안내입니다.';body=junk
  out.append((key,title,desc,body))
 return out
