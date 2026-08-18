# sh26-w7k2 — 한국사회사 2026-2 (전남대) 강의 저장소

학생용 페이지: **https://juncholkimso.github.io/sh26-w7k2/** (GitHub Pages, `main` 브랜치 `/docs`, Jekyll minimal 테마)

## 구성
- `docs/index.md` 수업 홈(세 주소·15주 표·평가·링크) · `syllabus.md` 강의계획 요약 · `submit.md` 제출 안내
- `docs/weekNN/index.md` **짧은 주차 안내**(질문·읽을 것·수업 순서·과제) — 손으로 쓴다(`tools/`의 생성 스크립트 참고) / `handout.md` 인쇄물 안내문 전문(볼트에서 이식) / `data/` 교수 제공 데이터(README 양식 필수)
- `docs/common/` readings(강독 논문·묶음 쪽 지도) · bibliography · concept-map · templates(양식 5종) · guides(자료 찾기 요약·통계 안내·시드 규칙) · grid(격자)
- `docs/workshop-stats/` 08-18 제작 통계연감 지면 뷰어(광주·전남 면적·광공업; 인용 불가 상태) — 3주 보조. `build.py`가 여기로 빌드
- `tools/sync_from_vault.py` 볼트(Obsidian) 배포문서 v2 → `weekNN/handout.md`, 공통 노트 → `common/`. `--week NN` / `--all` / `--misc` / `--force`

## 운영 규칙
- 순서: 볼트 초안 → 검토 → 이식 → 커밋. 커밋 메시지에 주차 명시(`week05: …`). 수업 전 주 금요일까지 다음 주 폴더.
- 데이터 업로드: `docs/weekNN/data/<이름>/` + `README.md`(`docs/common/templates/data-readme.md` 양식: 출처·수정일·정제 상태·이용 범위). 원본은 `raw/`(gitignore).
- 저작권: 논문 PDF는 저장소에 넣지 않는다(묶음 PDF는 드라이브 링크). 시드 자료는 정제본만.
- Pages는 공개 호스팅. `robots.txt`로 색인 차단, 링크는 학생에게만.
