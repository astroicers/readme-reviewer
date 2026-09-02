#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blind_agreement.py — 三位不知情判讀者 vs 作者(rubric 0.2.0)的一致度

盲判報告(reviews/2026-09-02-blind-rejudge-020.md)引用的每個數字由本檔重算並斷言。
判定紀律(承姊妹專案裁定):**只出 percent agreement 描述統計,不算 κ**
(n=12 遠低於 κ 可解讀所需;分維度 κ 已被證明在此規模下不可用)。

資料:
  - 判讀者:reviews/blind-2026-09-02/judges.yaml(零依賴解析,格式固定)
  - 作者值:import scripts/resimulate_18.py 的 ROWS(單一事實源,不抄第二份)

用法:python3 scripts/blind_agreement.py
"""
import os
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "readme-reviewer", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import lint_readme as L            # noqa: E402
from resimulate_18 import ROWS     # noqa: E402

DIMS = ("R-001", "R-002", "R-003", "R-004", "R-005")
# resimulate 的 repo 名(斜線)→ 判讀檔的 repo 名(底線)
NAME_MAP = {
    "httpie/httpie": "httpie_httpie", "gofiber/fiber": "gofiber_fiber",
    "dbt-labs/dbt-core": "dbt-labs_dbt-core", "ai/size-limit": "ai_size-limit",
    "amplication/amplication": "amplication_amplication", "choojs/choo": "choojs_choo",
    "facebook/react": "facebook_react", "torvalds/linux": "torvalds_linux",
    "freeCodeCamp/freeCodeCamp": "freeCodeCamp_freeCodeCamp",
    "public-apis/public-apis": "public-apis_public-apis",
    "sindresorhus/awesome": "sindresorhus_awesome",
    "vinta/awesome-python": "vinta_awesome-python",
}

# 報告引用的統計 —— 改了資料沒改報告(或反之),斷言轉紅
EXPECT = {
    "n_repos": 12,
    "judge_pairwise_dim_agree": {"R-001": 100.0, "R-002": 83.3, "R-003": 83.3,
                                 "R-004": 69.4, "R-005": 94.4},
    "judge_pairwise_overall": 86.1,
    "judges_vs_author": {"R-001": 91.7, "R-002": 77.8, "R-003": 80.6,
                         "R-004": 47.2, "R-005": 88.9},
    "unanimous_rows_incl_author": 41,      # 60 格中四方全同的格數
    "verdict_agree_3judges": 8,            # 12 份中三位判讀者 rollup verdict 全同
    "verdict_all4_agree": 6,               # 加上作者仍全同
    "author_r004_poor": 5, "judges_r004_poor_votes": 2,   # 12×3=36 票中 poor 票數
    "shape_agree": 11,                     # 12 份中三位形狀判定全同(fCC 分歧)
}


def load_judges(path):
    """固定格式解析:兩層縮排的 'name: {shape: "...", dims: [a, b, c, d, e]}'。"""
    out = {}
    cur = None
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"^  (\w):\s*$", ln)
        if m:
            cur = m.group(1)
            out[cur] = {}
            continue
        m = re.match(r"^    ([\w.-]+):\s*\{shape: \"([^\"]+)\",\s*dims: \[([^\]]+)\]\}", ln)
        if m and cur:
            dims = [d.strip() for d in m.group(3).split(",")]
            assert len(dims) == 5 and all(d in L.CRAFT_DIM_VALUES for d in dims), (m.group(1), dims)
            out[cur][m.group(1)] = {"shape": m.group(2), "dims": dict(zip(DIMS, dims))}
    return out


def pct(a, b):
    return round(100.0 * a / b, 1)


def main():
    judges = load_judges(os.path.join(ROOT, "reviews", "blind-2026-09-02", "judges.yaml"))
    assert set(judges) == {"A", "B", "C"} and all(len(v) == EXPECT["n_repos"] for v in judges.values())
    author = {}
    for repo, batch, _old4, n4, _e4, n5, _e5 in ROWS:
        if repo in NAME_MAP:
            old = dict(zip(DIMS[:4], _old4))
            author[NAME_MAP[repo]] = dict(old, **{"R-004": n4, "R-005": n5})
    assert len(author) == EXPECT["n_repos"], len(author)
    repos = sorted(author)

    # ── 判讀者兩兩一致(3 對 × 12 repo = 36 比較/維度)──────────────────
    pairs = [("A", "B"), ("A", "C"), ("B", "C")]
    dim_agree, total_hit, total_n = {}, 0, 0
    for d in DIMS:
        hit = sum(1 for r in repos for x, y in pairs
                  if judges[x][r]["dims"][d] == judges[y][r]["dims"][d])
        dim_agree[d] = pct(hit, len(repos) * len(pairs))
        total_hit += hit
        total_n += len(repos) * len(pairs)
    overall = pct(total_hit, total_n)

    # ── 判讀者 vs 作者(3 × 12 = 36 比較/維度)───────────────────────────
    va = {}
    for d in DIMS:
        hit = sum(1 for r in repos for j in judges if judges[j][r]["dims"][d] == author[r][d])
        va[d] = pct(hit, len(repos) * 3)

    # ── 四方全同格數(12×5=60 格)────────────────────────────────────────
    unanimous = sum(1 for r in repos for d in DIMS
                    if len({judges[j][r]["dims"][d] for j in judges} | {author[r][d]}) == 1)

    # ── verdict 層(rollup 純函式)────────────────────────────────────────
    v = {j: {r: L.craft_verdict_rollup(judges[j][r]["dims"]) for r in repos} for j in judges}
    v["author"] = {r: L.craft_verdict_rollup(author[r]) for r in repos}
    v3 = sum(1 for r in repos if len({v[j][r] for j in "ABC"}) == 1)
    v4 = sum(1 for r in repos if len({v[j][r] for j in "ABC"} | {v["author"][r]}) == 1)

    # ── R-004 的方向差(作者偏嚴?)────────────────────────────────────────
    a_poor = sum(1 for r in repos if author[r]["R-004"] == "poor")
    j_poor = sum(1 for r in repos for j in "ABC" if judges[j][r]["dims"]["R-004"] == "poor")

    shape_agree = sum(1 for r in repos if len({judges[j][r]["shape"] for j in "ABC"}) == 1)

    # ── 印表 ─────────────────────────────────────────────────────────────
    print(f"{'repo':<26}" + "".join(f"{j:^24}" for j in ("A", "B", "C", "author")))
    for r in repos:
        row = ""
        for src in (judges["A"][r]["dims"], judges["B"][r]["dims"],
                    judges["C"][r]["dims"], author[r]):
            row += ("/".join(x[0] if x != "n/a" else "-" for x in
                    (src[d] for d in DIMS))).center(24)
        print(f"{r:<26}{row}")
    print("\n維度一致度(判讀者兩兩,36 比較/維度):", dim_agree, f"整體 {overall}%")
    print("判讀者 vs 作者(36 比較/維度):", va)
    print(f"四方全同:{unanimous}/60 格")
    print("verdict:", {j: sorted(v[j].values()) and
          {x: list(v[j].values()).count(x) for x in set(v[j].values())} for j in v})
    print(f"三判讀者 verdict 全同:{v3}/12;含作者全同:{v4}/12")
    for r in repos:
        vs = {j: v[j][r] for j in ("A", "B", "C", "author")}
        if len(set(vs.values())) > 1:
            print(f"  分歧:{r:<26} " + "  ".join(f"{j}={x}" for j, x in vs.items()))
    print(f"R-004 poor:作者 {a_poor}/12,判讀者 {j_poor}/36 票")
    print(f"形狀全同:{shape_agree}/12")

    assert dim_agree == EXPECT["judge_pairwise_dim_agree"], dim_agree
    assert overall == EXPECT["judge_pairwise_overall"], overall
    assert va == EXPECT["judges_vs_author"], va
    assert unanimous == EXPECT["unanimous_rows_incl_author"], unanimous
    assert (v3, v4) == (EXPECT["verdict_agree_3judges"], EXPECT["verdict_all4_agree"]), (v3, v4)
    assert (a_poor, j_poor) == (EXPECT["author_r004_poor"], EXPECT["judges_r004_poor_votes"]), (a_poor, j_poor)
    assert shape_agree == EXPECT["shape_agree"], shape_agree
    print("\n✅ 全部統計與報告宣稱一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
