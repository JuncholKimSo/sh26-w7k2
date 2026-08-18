# sahoesa-workshop — 한국사회사 2026-2 자료 워크숍 학생용 사이트

- `build.py` — `~/apps/gwangju-index/work/stats/`에서 CSV·지면을 읽어 `docs/`를 만든다 (정제 없음, 열 이름만 한글화, png→1600px 그레이 JPEG)
- `docs/` — GitHub Pages 루트. index(안내·고지·다운로드·열 설명·공개 도구) / viewer(지면 + 추출 행, x위치 세로선) / data / pages
- 재빌드: `python3 build.py` (이미 변환된 이미지는 건너뜀)
- 로컬 확인: `python3 -m http.server 8791 --directory docs`

## 배포 (GitHub Pages, 비공개 URL)
Pages는 공개 호스팅이다. "비공개"는 색인 차단(noindex)+짐작하기 어려운 저장소 이름+링크 미공개로 만든다.
1. GitHub에서 저장소 새로 만들기 — 이름은 짐작 어려운 것(`sh26-w7k2` — 2026-08-18 배포됨), Public (Private Pages는 유료 플랜)
2. 이 폴더에서: `git remote add origin git@github.com:<계정>/<저장소>.git && git push -u origin main`
3. 저장소 Settings → Pages → Source: Deploy from a branch, Branch: `main`, Folder: `/docs` → Save
4. 배포 주소: **https://juncholkimso.github.io/sh26-w7k2/**. 학생에게는 이 링크만 준다
5. 학기 끝나면 Settings → Pages → Unpublish, 또는 저장소 삭제

⚠ 데이터는 인용 불가 상태. 사이트 상단 고지 유지. 검색엔진 색인은 `noindex`로 막았지만 링크가 퍼지면 접근 가능하다.
