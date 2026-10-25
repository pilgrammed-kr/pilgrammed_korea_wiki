# Pilgrammed Korea Wiki V2.5.1 — 공개 전 최종 후보

**주의: 현재까지 저작권 원문 전수 대조·정확도 검증은 끝나지 않았습니다. 최종 공개 전 검토가 필요합니다.**

## GitHub Pages 수동 배포
1. `copyright.html`에 실제 권리·정정 문의처를 추가하고 외부 설명문의 재사용 조건을 확인하세요.
2. GitHub에 `pilgrammed_korea_wiki` 저장소를 만든 뒤 **이 ZIP의 내용물**(ZIP 자체 아님)을 저장소 최상단에 업로드하세요.
3. 저장소 Settings → Pages → Build and deployment → Source: **GitHub Actions**로 설정하세요.
4. Actions → `Deploy pilgrammed_korea_wiki (manual)` → **Run workflow**를 누르면 그때 공개 배포됩니다. 자동 실행되지 않습니다.
5. 배포 결과로 생성된 실제 HTTPS URL에서 `sitemap.xml`, `robots.txt`, 아이템 페이지, 검색 및 모바일 동작을 확인하세요.
6. Google Search Console / 네이버 서치어드바이저에서 **본인 사이트 소유권을 인증**하고 사이트맵 URL을 제출하세요. Google·네이버 색인은 보장되지 않습니다.

## 수동 배포 (다른 정적 호스팅)
`pip install beautifulsoup4` 다음 `python make_sitemap.py https://실제-사이트-주소/` 실행 후 `index.html`, `items/`, `copyright.html`, `robots.txt`, `sitemap.xml`, `.nojekyll`을 배포하세요.

## 참고
- 권리자의 원문 설명, 번역문, 이미지·아트워크는 라이선스에 따라 별도 허락 또는 고지가 필요할 수 있습니다.
- 메인 UI의 기존 데이터/필터는 유지했습니다. 실제 브라우저의 전 기능 자동 E2E 검증은 미완료입니다.
- 자동 생성 검색용 아이템 페이지 676개, 총 HTML 679개.

## 출시 판정
브라우저 로컬 접근이 실행 환경에서 차단되어 자동 E2E 테스트는 미완료입니다. 외부 원문·라이선스 전수 대조와 운영자 문의처 등록도 미완료입니다. **자동 코드·링크 검사를 통과해도 정식 공개가 법적으로 안전하다는 의미는 아닙니다.**

## 검증 명령
`python verify_site.py` 로 상대경로 링크 검사, `python qa_release.py` 로 파일/메타/스크립트/배포 워크플로 검사. 실제 URL을 확정한 뒤 `python make_sitemap.py https://YOUR-PAGES-URL/` 실행하고 `python verify_site.py --production`으로 검사하세요.

## V2.5.1 표시 수정
- 사이트 상단, 사이드바, 홈 제목과 브라우저 제목의 이름·버전을 통일했습니다.
- 아이템별 페이지 677개 및 저작권 안내의 사이트명도 변경했습니다.
- 게임 수치와 출처 내용은 수정하지 않았습니다. 기존 저작권 원문 대조는 별도로 필요합니다.
