#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blind_agreement_r2.py — 第二輪盲判(rubric 0.3.0)vs 第一輪(0.2.0)

第二輪報告引用的每個數字由本檔重算並斷言(掛 CI)。
比較的合法性:**同一批 12 份 README 逐字凍結、同三種閱讀順序、同協定**,
唯一變因是判準版本(與判讀者個體——同模型家族,不可分離,見報告限制)。

第一輪數字不重抄:import blind_agreement 的 EXPECT(單一事實源)。
預先登記:批次 #2 報告的「分裂格推導表」寫於本輪開跑之前,本檔逐格斷言其命中/未中。
"""
import os
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
import lint_readme as L                                  # noqa: E402
from blind_agreement import EXPECT as R1, load_judges, pct, DIMS   # noqa: E402

# 報告引用的第二輪統計 —— 改資料沒改報告(或反之)轉紅
EXPECT_R2 = {
    "judge_pairwise_dim_agree": {"R-001": 100.0, "R-002": 88.9, "R-003": 75.0,
                                 "R-004": 77.8, "R-005": 94.4},
    "judge_pairwise_overall": 87.2,
    "shape_agree": 11,          # linux 2:1(第一輪是 fCC 2:1)
    "verdict_agree_3judges": 9,
    "r004_poor_votes": 3,       # 36 票
}

# 預先登記(批次 #2 報告,本輪開跑前寫定)的分裂格 → 預測值
PREREG = [
    ("sindresorhus_awesome",  "R-004", "n/a"),
    ("vinta_awesome-python",  "R-004", "mixed"),
    ("gofiber_fiber",         "R-004", "good"),
    ("ai_size-limit",         "R-004", "good"),
    ("public-apis_public-apis", "R-005", "mixed"),
    ("dbt-labs_dbt-core",     "R-002", "poor"),
    ("facebook_react",        "R-002", "good"),
]
PREREG_SHAPE = ("freeCodeCamp_freeCodeCamp", "hosted")
EXPECT_PREREG_HITS = 6   # 7 格中 6 格三方一致命中;fiber R-004 未中(新縫:宣稱即陳述)


def main():
    judges = load_judges(os.path.join(ROOT, "reviews", "blind-2026-09-02-r2", "judges-030.yaml"))
    assert set(judges) == {"D", "E", "F"} and all(len(v) == 12 for v in judges.values())
    repos = sorted(judges["D"])
    pairs = [("D", "E"), ("D", "F"), ("E", "F")]

    dim_agree, th, tn = {}, 0, 0
    for d in DIMS:
        hit = sum(1 for r in repos for x, y in pairs
                  if judges[x][r]["dims"][d] == judges[y][r]["dims"][d])
        dim_agree[d] = pct(hit, len(repos) * len(pairs))
        th += hit
        tn += len(repos) * len(pairs)
    overall = pct(th, tn)

    shape_agree = sum(1 for r in repos if len({judges[j][r]["shape"] for j in "DEF"}) == 1)
    v = {j: {r: L.craft_verdict_rollup(judges[j][r]["dims"]) for r in repos} for j in judges}
    v3 = sum(1 for r in repos if len({v[j][r] for j in "DEF"}) == 1)
    r004_poor = sum(1 for r in repos for j in "DEF" if judges[j][r]["dims"]["R-004"] == "poor")

    print(f"{'維度':<8}{'R1(0.2.0)':>12}{'R2(0.3.0)':>12}{'Δ':>8}")
    for d in DIMS:
        r1 = R1["judge_pairwise_dim_agree"][d]
        print(f"{d:<8}{r1:>12}{dim_agree[d]:>12}{dim_agree[d]-r1:>+8.1f}")
    r1o = R1["judge_pairwise_overall"]
    print(f"{'整體':<8}{r1o:>12}{overall:>12}{overall-r1o:>+8.1f}")
    print(f"\n形狀全同:{shape_agree}/12(R1 {R1['shape_agree']}/12;分裂者由 fCC 換成 linux)")
    print(f"三判讀者 verdict 全同:{v3}/12(R1 {R1['verdict_agree_3judges']}/12)")
    for r in repos:
        vs = {j: v[j][r] for j in "DEF"}
        if len(set(vs.values())) > 1:
            print(f"  verdict 分歧:{r:<26} " + "  ".join(f"{j}={x}" for j, x in vs.items()))
    print(f"R-004 poor 票:{r004_poor}/36(R1 {R1['judges_r004_poor_votes']}/36)")

    print("\n── 預先登記的分裂格(批次 #2 報告,開跑前寫定)──")
    hits = 0
    for repo, dim, pred in PREREG:
        got = [judges[j][repo]["dims"][dim] for j in "DEF"]
        unanimous_hit = all(g == pred for g in got)
        hits += unanimous_hit
        print(f"  {'✅' if unanimous_hit else '❌'} {repo} {dim}: 預測 {pred} → 實得 {got}")
    sh = [judges[j][PREREG_SHAPE[0]]["shape"] for j in "DEF"]
    shape_hit = all("hosted" in x for x in sh)
    print(f"  {'✅' if shape_hit else '❌'} {PREREG_SHAPE[0]} 形狀: 預測 hosted → {sh}")

    assert dim_agree == EXPECT_R2["judge_pairwise_dim_agree"], dim_agree
    assert overall == EXPECT_R2["judge_pairwise_overall"], overall
    assert shape_agree == EXPECT_R2["shape_agree"], shape_agree
    assert v3 == EXPECT_R2["verdict_agree_3judges"], v3
    assert r004_poor == EXPECT_R2["r004_poor_votes"], r004_poor
    assert hits == EXPECT_PREREG_HITS, (hits, EXPECT_PREREG_HITS)
    assert shape_hit
    # 方向斷言:R-004 上升、R-001/R-005 不降
    assert dim_agree["R-004"] > R1["judge_pairwise_dim_agree"]["R-004"]
    assert dim_agree["R-001"] >= R1["judge_pairwise_dim_agree"]["R-001"]
    assert dim_agree["R-005"] >= R1["judge_pairwise_dim_agree"]["R-005"]
    print("\n✅ 全部統計與報告宣稱一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
