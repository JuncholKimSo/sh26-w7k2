#!/usr/bin/env python3
"""한국사회사 자료 워크숍 — 학생용 정적 사이트 빌드.

원천: ~/apps/gwangju-index/work/stats/  (<계열>_values.csv · <계열>_headers.csv · png/)
      통계사색인.db catalog (source='연감(PDF)') → 표 카탈로그
산출: ./docs/workshop-stats/  (GitHub Pages)

원칙: 데이터를 정제하지 않는다. 열 이름만 한글로 바꾸고 값·플래그는 그대로.
계열은 *_values.csv 가 있는 것을 전부 자동으로 싣는다(목록 하드코딩 없음).
값 0행인 계열은 '실패 표본'으로 머리글 + 지면 표본(최대 3장)만 싣는다.

실행: python3 build.py   (PIL 필요)
"""
import csv, json, os, shutil, sqlite3, sys, unicodedata, datetime, re
from pathlib import Path
from PIL import Image, ImageFilter

SRC = Path.home() / "apps/gwangju-index/work/stats"
OUT = Path(__file__).parent / "docs" / "workshop-stats"
DB = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/통계사/통계사색인.db"
IMG_W = 1100
IMG_Q = 72
FAIL_SAMPLE_N = 3   # 값 0행 계열의 지면 표본 수

KO_COLS = {
    "series": "계열", "edition": "판", "page": "쪽", "table": "표제목", "chapter": "장",
    "block": "블록", "region": "지역", "matched_by": "매칭", "col_idx": "열순번",
    "x": "x위치", "raw": "원문", "value": "값", "conf": "신뢰도", "flag": "플래그",
    "row_text": "행원문",
}
ROW_COLS = ["block", "region", "col_idx", "x", "raw", "value", "conf", "flag", "row_text"]


def nfd(s):
    return unicodedata.normalize("NFD", s)


def nfc(s):
    return unicodedata.normalize("NFC", s)


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
    """1100px 그레이 JPEG q72. 이미 같은 폭으로 만들어진 것은 건너뛴다."""
    if dst.exists():
        try:
            if Image.open(dst).size[0] == IMG_W:
                return
        except Exception:
            pass
    im = Image.open(src).convert("L")
    w, h = im.size
    im = im.resize((IMG_W, int(h * IMG_W / w)), Image.LANCZOS)
    im = im.filter(ImageFilter.MedianFilter(3))   # 스캔 잡티 제거 → 용량 약 20% 절감
    im.save(dst, "JPEG", quality=IMG_Q, optimize=True)


def edkey(kv):
    ed, pg = kv
    return (int(ed) if ed.isdigit() else 0, int(pg) if pg.isdigit() else 0)


def build_series(manifest, pngs, used_imgs):
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    (OUT / "pages").mkdir(exist_ok=True)

    def find_png(series, ed, page):
        return pngs.get(nfd(f"{series}_{ed}_{page}.png"))

    series_files = sorted(SRC.glob("*_values.csv"))
    for vf in series_files:
        s = nfc(vf.name[: -len("_values.csv")])
        hf = SRC / f"{s}_headers.csv"
        vals = read(vf)
        heads = read(hf) if hf.exists() else []
        head_by = {(h["edition"], h["page"]): h.get("header", "") for h in heads}
        # 원본 CSV 그대로 + 한글 열 CSV
        shutil.copy(vf, OUT / "data" / f"{s}_values.csv")
        if hf.exists():
            shutil.copy(hf, OUT / "data" / f"{s}_headers.csv")
        mtime = datetime.datetime.fromtimestamp(vf.stat().st_mtime).strftime("%Y-%m-%d")

        if not vals:
            # 실패 계열: 머리글 CSV + 지면 표본
            eds = sorted({h["edition"] for h in heads if h.get("edition")})
            if not eds:
                print(s, "값 0행 · 머리글도 없음 → 건너뜀", file=sys.stderr)
                continue
            picks = [eds[0], eds[len(eds) // 2], eds[-1]] if len(eds) >= 3 else eds
            pages = []
            seen = set()
            for h in heads:
                if h["edition"] in picks and h["edition"] not in seen:
                    src = find_png(s, h["edition"], h["page"])
                    if not src:
                        continue
                    img = f"pages/{s}_{h['edition']}_{h['page']}.jpg"
                    convert_png(src, OUT / img)
                    used_imgs.add(img)
                    seen.add(h["edition"])
                    pages.append({"edition": h["edition"], "page": h["page"], "img": img,
                                  "table": h.get("table", ""), "chapter": h.get("chapter", ""),
                                  "header": h.get("header", ""), "rows": []})
                if len(pages) >= FAIL_SAMPLE_N:
                    break
            if heads:
                write_ko_csv(heads, list(heads[0].keys()), OUT / "data" / f"{s}_표머리.csv")
            with open(OUT / "data" / f"{s}.json", "w", encoding="utf-8") as f:
                json.dump({"series": s, "cols": ROW_COLS, "failed": True, "pages": pages}, f, ensure_ascii=False)
            manifest["series"][s] = {
                "failed": True, "rows": 0, "updated": mtime,
                "editions": sorted({h["edition"] for h in heads}),
                "pages": [{"edition": p["edition"], "page": p["page"], "img": p["img"], "table": p["table"], "n": 0} for p in pages],
                "regions": [], "blocks": [],
            }
            print(s, "값 0행 · 머리글", len(heads), "· 표본 지면", len(pages))
            continue

        cols = list(vals[0].keys())
        write_ko_csv(vals, cols, OUT / "data" / f"{s}_값.csv")
        if heads:
            write_ko_csv(heads, list(heads[0].keys()), OUT / "data" / f"{s}_표머리.csv")

        by_page = {}
        for r in vals:
            by_page.setdefault((r["edition"], r["page"]), []).append(r)
        pages, mpages = [], []
        missing = 0
        for (ed, pg), rows in sorted(by_page.items(), key=lambda kv: edkey(kv[0])):
            src = find_png(s, ed, pg)
            img = None
            if src:
                img = f"pages/{s}_{ed}_{pg}.jpg"
                convert_png(src, OUT / img)
                used_imgs.add(img)
            else:
                missing += 1
            pages.append({
                "edition": ed, "page": pg, "img": img,
                "table": rows[0].get("table", ""), "chapter": rows[0].get("chapter", ""),
                "header": head_by.get((ed, pg), ""),
                "rows": [[r.get(c, "") for c in ROW_COLS] for r in rows],
            })
            mpages.append({"edition": ed, "page": pg, "img": img, "table": rows[0].get("table", ""), "n": len(rows)})
        with open(OUT / "data" / f"{s}.json", "w", encoding="utf-8") as f:
            json.dump({"series": s, "cols": ROW_COLS, "failed": False, "pages": pages}, f, ensure_ascii=False)
        regions = sorted({r["region"] for r in vals})
        blocks = sorted({r["block"] for r in vals})
        manifest["series"][s] = {
            "failed": False, "rows": len(vals), "updated": mtime,
            "editions": sorted({p["edition"] for p in mpages}, key=lambda e: int(e) if e.isdigit() else 0),
            "pages": mpages, "regions": regions, "blocks": blocks,
        }
        print(f"{s} {len(vals)}값 {len(pages)}쪽 {len(manifest['series'][s]['editions'])}판" + (f" · png 없음 {missing}" if missing else ""))


def build_catalog(manifest):
    """통계사색인.db catalog(source='연감(PDF)') → catalog.json (컴팩트 배열)."""
    if not DB.exists():
        print("catalog DB 없음:", DB, file=sys.stderr)
        return
    con = sqlite3.connect(str(DB))
    cur = con.execute("""select edition, chapter, table_no, title, pdf_page, master_cat
                         from catalog where source='연감(PDF)'
                         order by cast(edition as int), pdf_page, cast(table_no as int)""")
    chapters, cats = [], []
    cidx, kidx = {}, {}
    rows = []
    for ed, ch, tno, title, pg, mc in cur:
        ch = nfc(ch or ""); mc = nfc(mc or ""); title = nfc(title or "")
        if ch not in cidx:
            cidx[ch] = len(chapters); chapters.append(ch)
        if mc not in kidx:
            kidx[mc] = len(cats); cats.append(mc)
        rows.append([ed or "", cidx[ch], tno or "", title, pg if pg is not None else "", kidx[mc]])
    con.close()
    out = {"cols": ["edition", "chapter", "table_no", "title", "pdf_page", "cat"],
           "chapters": chapters, "cats": cats, "rows": rows,
           "updated": datetime.date.today().isoformat()}
    with open(OUT / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    eds = sorted({r[0] for r in rows}, key=lambda e: int(e) if e.isdigit() else 0)
    manifest["catalog"] = {"rows": len(rows), "editions": [eds[0], eds[-1]] if eds else []}
    print("catalog", len(rows), "행 ·", (OUT / "catalog.json").stat().st_size // 1000, "KB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"built": datetime.date.today().isoformat(), "img_w": IMG_W, "series": {}}
    pngs = {nfd(p.name): p for p in (SRC / "png").iterdir() if p.suffix == ".png"}
    used = set()
    build_series(manifest, pngs, used)
    # 쓰이지 않는 옛 이미지 정리
    for p in (OUT / "pages").glob("*.jpg"):
        if f"pages/{nfc(p.name)}" not in used:
            p.unlink()
    build_catalog(manifest)
    with open(OUT / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)
    pages_sz = sum(p.stat().st_size for p in (OUT / "pages").glob("*.jpg"))
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"pages/ {len(used)}장 {pages_sz/1e6:.1f} MB · site 총 {total/1e6:.1f} MB")


if __name__ == "__main__":
    main()
