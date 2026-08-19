#!/usr/bin/env python3
"""[2026-08-19 사용자 결정: handout(안내문 전문)은 웹에 싣지 않고 인쇄물로 따로 배포 → --week/--all 이식은 기본 비활성. 필요 시 --handout 플래그로만.]
볼트 배포문서 v2 → docs/weekNN/handout.md 이식. (weekNN/index.md 는 짧은 안내 — 손으로 쓴다)

사용:
  python3 tools/sync_from_vault.py --week 05        # 한 주
  python3 tools/sync_from_vault.py --all            # 전체(01~15, 파일 있는 것만)
  python3 tools/sync_from_vault.py --all --force    # 검토(review) 표시 없어도 이식
  python3 tools/sync_from_vault.py --misc           # 강의계획서·강독 논문 목록·참고도서 → syllabus.md / common/readings.md / common/bibliography.md

규칙:
  - 볼트 frontmatter에 `review:` 값이 있으면 '검토 완료'로 보고 이식. 없으면 --force 없이는 건너뜀
    (사용자 방침: Obsidian 초안 → 검토 → GitHub).
  - frontmatter 제거, [[위키링크]] → 텍스트(또는 저장소 경로), 📖 발췌 유지.
  - 맨 위에 "← 수업 홈 / 수정일" 삽입. weekNN/data/ 가 있으면 끝에 '이 주의 데이터' 목록 자동.
"""
import argparse, glob, os, re, sys, datetime, urllib.parse

VAULT = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/WonderLab 2G/40 강의/2026_2_사회사")
DIST = os.path.join(VAULT, "강의노트", "배포")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
HOME = "https://juncholkimso.github.io/sh26-w7k2/"
FORM = "https://forms.gle/9qDjkpWd9wg7fgbX6"

# 볼트 내부 노트 → 저장소 경로
LINKMAP = {
    "강독 논문 목록": "../common/readings.html",
    "참고도서 — 사회사·역사사회학 방법론 단행본": "../common/bibliography.html",
    "개념 지도 — 한국사회사의 주된 개념들": "../common/concept-map.html",
    "강의계획서 (학생 배포용)": "../",
    "_사회사 MOC": "../",
}

FM_RE = re.compile(r"^---\n.*?\n---\n", re.S)

def strip_frontmatter(text):
    m = FM_RE.match(text)
    fm = m.group(0) if m else ""
    return fm, text[len(fm):]

def has_review(fm):
    return re.search(r"^review:\s*\S", fm, re.M) is not None

def convert_links(text):
    def repl(m):
        target = m.group(1).strip(); alias = m.group(2)
        label = alias if alias else target
        # 배포문서 링크: [[05주 배포 — 사회]] → ../week05/
        wm = re.match(r"^(\d\d)주 배포", target)
        if wm:
            return f"[{label}](../week{wm.group(1)}/)"
        if target in LINKMAP:
            return f"[{label}]({LINKMAP[target]})"
        # 강의노트/논문노트 등 내부 링크는 텍스트로
        return label
    return re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", repl, text)

def data_index(week):
    d = os.path.join(DOCS, f"week{week}", "data")
    if not os.path.isdir(d):
        return ""
    items = sorted(x for x in os.listdir(d) if not x.startswith(".") and x != "README.md")
    if not items:
        return ""
    lines = ["", "---", "### 이 주의 데이터 (교수 제공)", ""]
    for x in items:
        p = os.path.join(d, x)
        if os.path.isdir(p):
            rd = os.path.join(p, "README.md")
            desc = ""
            if os.path.exists(rd):
                for line in open(rd, encoding="utf-8"):
                    if line.startswith("# "):
                        desc = line[2:].strip(); break
            lines.append(f"- [{x}](data/{urllib.parse.quote(x)}/) — {desc} (README의 출처·정제 상태·이용 범위를 먼저 읽을 것)")
        else:
            lines.append(f"- [{x}](data/{urllib.parse.quote(x)})")
    return "\n".join(lines) + "\n"

def sync_week(week, force=False):
    files = glob.glob(os.path.join(DIST, f"{week}주 배포 — *.md"))
    if not files:
        print(f"[skip] week{week}: 볼트 배포문서 없음"); return False
    src = files[0]
    text = open(src, encoding="utf-8").read()
    fm, body = strip_frontmatter(text)
    if not force and not has_review(fm):
        print(f"[skip] week{week}: 검토(review) 표시 없음 — --force 로 강제 가능"); return False
    body = convert_links(body)
    mtime = datetime.date.fromtimestamp(os.path.getmtime(src)).isoformat()
    head = (f"---\ntitle: \"{week}주\"\nlayout: default\n---\n"
            f"[← 수업 홈]({HOME}) · [← 이 주 안내](./) · [제출 폼]({FORM}) · 수정일 {mtime}\n\n")
    out_dir = os.path.join(DOCS, f"week{week}"); os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "handout.md")
    open(out, "w", encoding="utf-8").write(head + body.rstrip() + "\n" + data_index(week))
    print(f"[ok] week{week} ← {os.path.basename(src)}"); return True

def sync_misc(force=False):
    pairs = [
        # 강의계획서는 요약본을 손으로 쓴다(docs/syllabus.md) — 전문은 인쇄물
        ("강독 논문 목록.md", os.path.join("common", "readings.md"), "강독 논문 목록"),
        ("참고도서 — 사회사·역사사회학 방법론 단행본.md", os.path.join("common", "bibliography.md"), "참고도서"),
        ("개념 지도 — 한국사회사의 주된 개념들.md", os.path.join("common", "concept-map.md"), "개념 지도"),
    ]
    for src_name, dst_rel, title in pairs:
        src = os.path.join(VAULT, src_name)
        if not os.path.exists(src):
            print(f"[skip] {src_name} 없음"); continue
        fm, body = strip_frontmatter(open(src, encoding="utf-8").read())
        body = convert_links(body)
        mtime = datetime.date.fromtimestamp(os.path.getmtime(src)).isoformat()
        rel_home = "../" if os.sep in dst_rel else "./"
        head = f"---\ntitle: \"{title}\"\nlayout: default\n---\n[← 수업 홈]({rel_home}) · 수정일 {mtime}\n\n"
        dst = os.path.join(DOCS, dst_rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write(head + body.rstrip() + "\n")
        print(f"[ok] {dst_rel} ← {src_name}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--week"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true"); ap.add_argument("--misc", action="store_true"); ap.add_argument("--handout", action="store_true", help="handout 이식 허용(기본 비활성)")
    a = ap.parse_args()
    if (a.week or a.all) and not a.handout:
        print("handout 이식은 비활성(인쇄물 배포). --handout 을 붙이면 실행."); a.week=None; a.all=False
    if a.week: sync_week(a.week.zfill(2), a.force)
    if a.all:
        for w in [f"{i:02d}" for i in range(1, 16)]: sync_week(w, a.force)
    if a.misc: sync_misc(a.force)
    if not (a.week or a.all or a.misc): ap.print_help()
