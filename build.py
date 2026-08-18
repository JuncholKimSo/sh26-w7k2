#!/usr/bin/env python3
"""한국사회사 자료 워크숍 — 학생용 정적 사이트 빌드.

원천: ~/apps/gwangju-index/work/stats/  (면적·광공업 values/headers CSV, 지면 png)
산출: ./docs/  (GitHub Pages 루트)

원칙: 데이터를 정제하지 않는다. 열 이름만 한글로 바꾸고 값·플래그는 그대로.
"""
import csv, json, os, shutil, sys, unicodedata
from pathlib import Path
from PIL import Image

SRC = Path.home() / "apps/gwangju-index/work/stats"
OUT = Path(__file__).parent / "docs" / "workshop-stats"
IMG_W = 1600
IMG_Q = 80

KO_COLS = {
    "series": "계열", "edition": "판", "page": "쪽", "table": "표제목", "chapter": "장",
    "block": "블록", "region": "지역", "matched_by": "매칭", "col_idx": "열순번",
    "x": "x위치", "raw": "원문", "value": "값", "conf": "신뢰도", "flag": "플래그",
    "row_text": "행원문",
}
SERIES = ["면적", "광공업"]
# 금융은 값 0행. 실패 진단용 지면 3장만 싣는다.
FINANCE_SAMPLE_EDITIONS = ["1952", "1975", "1995"]


def nfd(s):
    return unicodedata.normalize("NFD", s)


def read(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_ko_csv(rows, cols, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([KO_COLS.get(c, c) for c in cols])
        for r in rows:
            w.writerow([r.get(c, "") for c in cols])


def convert_png(src, dst):
    if dst.exists():
        return
    im = Image.open(src)
    w, h = im.size
    im = im.resize((IMG_W, int(h * IMG_W / w)), Image.LANCZOS).convert("L")
    im.save(dst, "JPEG", quality=IMG_Q, optimize=True)


def main():
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)

    manifest = {"series": {}, "finance": []}
    pngs = {nfd(p.name): p for p in (SRC / "png").iterdir()}

    def find_png(series, ed, page):
        name = nfd(f"{series}_{ed}_{page}.png")
        return pngs.get(name)

    for s in SERIES:
        vals = read(SRC / f"{s}_values.csv")
        cols = list(vals[0].keys())
        heads = read(SRC / f"{s}_headers.csv")
        # 배포용 CSV (열 한글화, 값 그대로)
        write_ko_csv(vals, cols, OUT / "data" / f"{s}_값.csv")
        write_ko_csv(heads, list(heads[0].keys()), OUT / "data" / f"{s}_표머리.csv")
        # 원본 그대로도 둔다
        shutil.copy(SRC / f"{s}_values.csv", OUT / "data" / f"{s}_values.csv")
        shutil.copy(SRC / f"{s}_headers.csv", OUT / "data" / f"{s}_headers.csv")

        head_by = {(h["edition"], h["page"]): h["header"] for h in heads}
        by_page = {}
        for r in vals:
            k = (r["edition"], r["page"])
            by_page.setdefault(k, []).append(r)
        pages = []
        for (ed, pg), rows in sorted(by_page.items(), key=lambda kv: (int(kv[0][0]), int(kv[0][1]))):
            src = find_png(s, ed, pg)
            img = None
            if src:
                img = f"pages/{s}_{ed}_{pg}.jpg"
                convert_png(src, OUT / img)
            else:
                print("png 없음:", s, ed, pg, file=sys.stderr)
            pages.append({
                "edition": ed, "page": pg, "img": img,
                "table": rows[0]["table"], "chapter": rows[0]["chapter"],
                "header": head_by.get((ed, pg), ""),
                "rows": [{
                    "block": r["block"], "region": r["region"], "x": r["x"],
                    "raw": r["raw"], "value": r["value"], "conf": r["conf"],
                    "flag": r["flag"], "row_text": r["row_text"],
                } for r in rows],
            })
        manifest["series"][s] = pages
        print(s, len(vals), "값", len(pages), "쪽")

    # 금융: 값 0행. 헤더 CSV와 표본 지면.
    fh = read(SRC / "금융_headers.csv")
    shutil.copy(SRC / "금융_headers.csv", OUT / "data" / "금융_headers.csv")
    shutil.copy(SRC / "금융_values.csv", OUT / "data" / "금융_values.csv")
    for h in fh:
        if h["edition"] in FINANCE_SAMPLE_EDITIONS:
            src = find_png("금융", h["edition"], h["page"])
            if not src:
                continue
            img = f"pages/금융_{h['edition']}_{h['page']}.jpg"
            convert_png(src, OUT / img)
            manifest["finance"].append({"edition": h["edition"], "page": h["page"], "img": img,
                                        "table": h["table"], "header": h["header"]})
            FINANCE_SAMPLE_EDITIONS.remove(h["edition"])  # 판당 1쪽
    with open(OUT / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)
    print("금융 표본", len(manifest["finance"]))
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"site 총 {total/1e6:.1f} MB")


if __name__ == "__main__":
    main()
