---
title: "04주: 자료는 어디에 있고, 무엇을 가져와 어떻게 쌓는가"
layout: default
---
[← 수업 홈](../) · [제출 폼](https://forms.gle/9qDjkpWd9wg7fgbX6)

# 4주: 자료는 어디에 있고, 무엇을 가져와 어떻게 쌓는가

**회차·날짜**: 9~10회 · 10/6(화) · 10/8(목)

## 읽을 것
* 자료 찾기 가이드(「역사·사회 연구를 위한 디지털 자료 찾기」): [../common/guides/digital-sources.html](../common/guides/digital-sources.html)
* 김백영 외(2016) 7장 서호철 「사회사/역사사회학의 자료와 그 이용」: 발췌("자료 없는 방법론이란 불모의 환상")

## 7부 DB: 부마다 대표 2~3곳

| 부 | DB | 시기 | 팁 |
|---|---|---|---|
| 1 법령·관보 | [국가법령정보센터](https://www.law.go.kr/) | 현행~폐지 연혁 | 법률>시행령>시행규칙 위계. 연혁 검색으로 제정·개정 추적 |
| 1 법령·관보 | [국립중앙도서관 관보](https://www.nl.go.kr/NL/contents/N20301000000.do) | 구한국·조선총독부·미군정 |  |
| 1 법령·관보 | [국가기록원 관보](https://theme.archives.go.kr/next/gazette/viewIntroduction01.do) | 1948~2000 |  |
| 2 통계 | [KOSIS 국가통계포털](https://kosis.kr/) | 1949~ | 국가승인통계 통합. 시점·분류 조정 후 다운로드 |
| 2 통계 | [통계청](https://kostat.go.kr/) |  | 총조사 원자료·보고서 |
| 2 통계 | [매디슨 프로젝트](https://www.rug.nl/ggdc/historicaldevelopment/maddison/) | 장기 | 원자료 없는 구간은 추계: 주의 |
| 3 공간 | [국토정보플랫폼](https://map.ngii.go.kr/mn/mainPage.do) |  |  |
| 3 공간 | [서울 항공사진](https://map.seoul.go.kr/smgis2/divisionMap) | 1972~ |  |
| 3 공간 | [부산 항공사진](http://lifemap.busan.go.kr/) | 1972~ |  |
| 4 공문서 | [국가기록원](https://www.archives.go.kr/) |  | 기관명으로 먼저 검색. 키워드만으로는 한계 |
| 4 공문서 | [대통령기록관](https://www.pa.go.kr/) |  |  |
| 4 공문서 | [국무회의록](https://theme.archives.go.kr/next/cabinet/keywordDetailSearch.do) |  |  |
| 5 언론 | [국립중앙도서관 신문 아카이브](https://nl.go.kr/newspaper/) | 1880~1966 |  |
| 5 언론 | [한국역사정보통합시스템 신문](http://www.koreanhistory.or.kr/newsPaper.do) | 1896~1963 |  |
| 5 언론 | [네이버 뉴스라이브러리](https://newslibrary.naver.com/) | 1920~1999 | 동아·조선·경향·매경·한겨레 |
| 6 생활사 | [e뮤지엄](http://www.emuseum.go.kr/) |  |  |
| 6 생활사 | [대한민국역사박물관 디지털아카이브](http://archive.much.go.kr/) | 근현대 |  |
| 6 생활사 | [근대기록문화아카이브](https://modern.koreastudy.or.kr/) | 1910~1970년대 | 일상 사진 풍부 |
| 7 기초·학술 | [한국사데이터베이스](http://db.history.go.kr/) |  | 국사편찬위 |
| 7 기초·학술 | [한국학 디지털 아카이브](http://yoksa.aks.ac.kr/) |  |  |
| 7 기초·학술 | [규장각 원문검색](https://kyudb.snu.ac.kr/) |  |  |

전체 42곳: [db_directory.csv](data/db_directory.csv) · 원칙과 부별 설명: [디지털 자료 찾기(요약)](../common/guides/digital-sources.html)

## 자료 메모 예시 (공동 자료 목록 한 줄)

| 주제(시드 ID) | 자료명 | 유형 | DB | 생산 기관·시기 | 핵심 내용 | 내 주제와의 관계 | 의문 |
|---|---|---|---|---|---|---|---|
| S-0231 월세 | 「임대차보호법」 제정 관보 | 법령 | 1 법령·관보 | 국회/법제처 · 1981-03-05 | 최초 제정 조문: 임차인 보호 범위 | 광장 발언의 '집' 문제의 제도적 기원 | 왜 1981년인가 |

양식: [source_list_template.csv](data/source_list_template.csv) · 대조 짝: [paired_sources](data/paired_sources.html)

## 이 주의 자료(교수 제공)
* [data/db_directory.csv](data/db_directory.csv): 7부 DB 목록(이름·URL·시기·자료 유형·검색 팁)
* [data/source_list_template.csv](data/source_list_template.csv): 반 공동 자료 목록 양식(자료 5건 기입용)
* [data/seed/](data/seed/): 시드 자료 정제본(4주 1회차에 게시; 규칙 [../common/guides/seed-data-rules.html](../common/guides/seed-data-rules.html))
* [data/paired_sources.md](data/paired_sources.md): 공식/비공식 사료 대조 짝(유신헌법 조문 vs 박완서 문장 등)
* [디지털 자료 찾기(요약)](../common/guides/digital-sources.html): 4주 본체
* [시드 자료 이용 규칙](../common/guides/seed-data-rules.html)
* [아카이빙 계획서 양식](../common/templates/archiving-plan.html)

## 과제
* **실습 ① 4주분 「자료 찾아 컬렉션 만들기」**: 자료 5건(공동 자료 목록 양식) + 못 찾은 것 1건 + 해석 한 단락 + 아카이빙 계획서 → 폼
* 5주 준비: 강독 시작: 박명규(2001) pp.2~34 · 조계원(2016) pp.35~65. **리뷰 첫 제출**(양식 [../common/templates/review-note.html](../common/templates/review-note.html)), 1회차 수업 전

