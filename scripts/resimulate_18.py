#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resimulate_18.py — rubric 0.1.0 → 0.2.0 對既有 18 份判讀的重模擬

批次處理報告(reviews/2026-09-02-misjudgment-batch-1.md)引用的 verdict 數字
全部由本檔重算 —— **散文裡的數字無法轉紅,可執行的斷言可以**(姊妹專案教訓)。

輸入的維度值是**判讀**(LLM 判的,不可由程式推導);本檔保證的是:
  1. verdict 一律走 lint_readme.craft_verdict_rollup(),無手推
  2. 報告引用的分佈數字與這裡的斷言一致 —— 改了判讀表沒改報告,CI 轉紅
  3. 每個新值都附一行證據句(evidence),空字串會被斷言擋下

⚠️ 兩批的判讀者是同一人(rubric 作者),重模擬**不是**校準,
不得引用為「判準判得準」的證據。

用法:python3 scripts/resimulate_18.py        # 印表 + 斷言
"""
import os
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "readme-reviewer", "scripts"))
import lint_readme as L   # noqa: E402

# (repo, 批次, 舊四維 R-001..R-004, 新 R-004, 新 R-004 證據, 新 R-005, 新 R-005 證據)
# 舊值抄自 reviews/ 兩份報告;新值是 2026-09-02 依 rubric 0.2.0 重判。
ROWS = [
    ("visual-web-stack", 1, ("good", "good", "good", "good"),
     "good", "序1:版本對照表+撰寫基準 2026-06+查證紀錄",
     "n/a", "內部工具豁免:讀者與維護者同圈(exemption)"),
    ("claude-code-warp", 1, ("good", "good", "good", "good"),
     "good", "序1:Legacy Support 適用邊界;protocol version 帶協商說明",
     "mixed", "序4:README 無求助管道、維護主體無內文指認(grep 實測)"),
    ("anthropics/skills", 1, ("good", "good", "mixed", "good"),
     "good", "序1:Disclaimer 明確;易腐內容少",
     "good", "序2:support.claude.com 求助文章 ×3 + 主體 Anthropic 內文可指認"),
    ("superpowers-marketplace", 1, ("good", "good", "mixed", "poor"),
     "poor", "序5:plugin 描述散文複製、無陳述、無同步機制(絕對連結指向源 repo 不同步描述)",
     "mixed", "序4:README 無求助管道、無維護主體陳述(grep 實測)"),
    ("Jeffallan/claude-skills", 1, ("mixed", "good", "good", "poor"),
     "mixed", "序3:<!-- SKILL_COUNT --> 機械同步標記 + CI 驗證(姊妹專案實測)",
     "good", "序2:Support 段(Issues+Discussions)+ Author 段具名"),
    ("24kchengYe/human-skill-tree", 1, ("mixed", "mixed", "good", "poor"),
     # R-003 首批未判(823 行只讀了抽樣),poor 已定 verdict;重模擬以 good 佔位計最寬情形
     "poor", "序5:無陳述、易腐裸露、無同步",
     "mixed", "序4:無求助管道、無維護主體陳述(星乞求段不是)"),
    ("httpie/httpie", 2, ("good", "mixed", "good", "poor"),
     "poor", "序5:無陳述;安裝/文件全委外部網站(equivalent_forms 明文:外部不算)",
     "good", "序2:Community & support 段六管道 + 主體 org 內文可指認"),
    ("gofiber/fiber", 2, ("mixed", "good", "good", "good"),
     "good", "序1:⚠️ Limitations 段 + Go 1.25 tested-with 陳述",
     "good", "序2:Discord + Contribute + Code Contributors + 主體 org"),
    ("dbt-labs/dbt-core", 2, ("good", "mixed", "good", "good"),
     "good", "序1:v2 分支 WARNING + beta 標記 + OS/arch 支援表",
     "good", "序2:dbt Community Slack/Discourse + 主體 dbt Labs"),
    ("ai/size-limit", 2, ("good", "good", "good", "good"),
     "good", "序1:time 量測不穩定性明述並附 estimo issue 連結",
     "mixed", "序4:無求助管道、無維護主體內文陳述(grep 實測;logo 署名是繪者非維護者)"),
    ("amplication/amplication", 2, ("mixed", "good", "mixed", "poor"),
     "mixed", "序3:node/npm 版本指向 package.json engines(單一事實源,不複製)",
     "good", "序2:Discord 'for support' + bug/feature 模板 + 主體 org"),
    ("choojs/choo", 2, ("good", "mixed", "good", "mixed"),
     "mixed", "序2:stability: experimental 徽章是維護狀態陳述,但 Travis/freenode 已腐",
     "poor", "序1:求助管道已失效(freenode chat 已不存在)而 README 未更新"),
    ("facebook/react", 2, ("good", "good", "good", "poor"),
     "poor", "序5:無陳述;createRoot 版本耦合範例裸露;外部 docs 不算同步",
     "good", "序2:Where to Get Support 連結 + CoC + 主體 Facebook 內文具名"),
    ("torvalds/linux", 2, ("good", "n/a", "good", "poor"),
     "mixed", "序3:30+ 條 repo 內相對路徑(Documentation/**),隨版控天然同步",
     "good", "序2:lore.kernel.org 社群管道 + Maintainer 角色段"),
    ("freeCodeCamp/freeCodeCamp", 2, ("good", "mixed", "good", "good"),
     "good", "序1:Academic Honesty 邊界 + 各認證 beta 標記",
     "good", "序2:forum+Discord+報 bug 分流 + 主體 501(c)(3) 具名(高分:有分流)"),
    ("public-apis/public-apis", 2, ("poor", "n/a", "mixed", "poor"),
     "poor", "序5:API 表格(Auth/HTTPS/CORS)裸露、無陳述、無同步",
     "mixed", "序3:維護主體有陳述(community+APILayer);求助管道只在贊助商區塊(anti_pattern)"),
    ("sindresorhus/awesome", 2, ("poor", "n/a", "good", "poor"),
     "poor", "序5:無陳述;條目描述裸露、無同步機制可指認",
     "mixed", "序3:主體可指認(作者自述段);無求問管道(contributing ≠ ask questions)"),
    ("vinta/awesome-python", 2, ("good", "n/a", "good", "poor"),
     "poor", "序5:無陳述;條目描述裸露、無同步機制可指認",
     "good", "序2:contact @vinta 具名管道 + Contributing"),
]

# 報告引用的分佈 —— 改了上表沒改這裡(或反之),斷言轉紅
EXPECT = {
    "old": {"approved": 3, "approved-with-notes": 4, "needs-revision": 11},
    "new": {"approved": 1, "approved-with-notes": 7, "needs-revision": 10},
    "r004_old": {"good": 7, "mixed": 1, "poor": 10},
    "r004_new": {"good": 7, "mixed": 4, "poor": 7},
    "r005_new": {"good": 10, "mixed": 6, "poor": 1, "n/a": 1},
    "flips": [("torvalds/linux", "needs-revision", "approved-with-notes")],
    "softened": [("claude-code-warp", "approved", "approved-with-notes"),
                 ("ai/size-limit", "approved", "approved-with-notes")],
}


def main():
    dist_old, dist_new = {}, {}
    r4o, r4n, r5n = {}, {}, {}
    changes = []
    print(f"{'repo':<28}{'舊verdict':<22}{'新R-004':<8}{'新R-005':<8}{'新verdict':<22}")
    print("─" * 88)
    for repo, _b, old4, n4, ev4, n5, ev5 in ROWS:
        assert ev4.strip() and ev5.strip(), f"{repo}: 新值必須附證據句"
        old = dict(zip(("R-001", "R-002", "R-003", "R-004"), old4))
        vo = L.craft_verdict_rollup(old)
        new = dict(old, **{"R-004": n4, "R-005": n5})
        vn = L.craft_verdict_rollup(new)
        dist_old[vo] = dist_old.get(vo, 0) + 1
        dist_new[vn] = dist_new.get(vn, 0) + 1
        r4o[old4[3]] = r4o.get(old4[3], 0) + 1
        r4n[n4] = r4n.get(n4, 0) + 1
        r5n[n5] = r5n.get(n5, 0) + 1
        if vo != vn:
            changes.append((repo, vo, vn))
        mark = "  ⇐ 變" if vo != vn else ""
        print(f"{repo:<28}{vo:<22}{n4:<8}{n5:<8}{vn:<22}{mark}")

    print()
    print(f"舊分佈:{dist_old}")
    print(f"新分佈:{dist_new}")
    print(f"R-004:{r4o} → {r4n}")
    print(f"R-005(新增):{r5n}")
    print(f"verdict 變動:{changes}")

    assert dist_old == EXPECT["old"], (dist_old, EXPECT["old"])
    assert dist_new == EXPECT["new"], (dist_new, EXPECT["new"])
    assert r4o == EXPECT["r004_old"], (r4o, EXPECT["r004_old"])
    assert r4n == EXPECT["r004_new"], (r4n, EXPECT["r004_new"])
    assert r5n == EXPECT["r005_new"], (r5n, EXPECT["r005_new"])
    flips = [c for c in changes if c[1] == "needs-revision"]
    soft = [c for c in changes if c[1] == "approved"]
    assert flips == EXPECT["flips"], (flips, EXPECT["flips"])
    assert sorted(soft) == sorted(EXPECT["softened"]), (soft, EXPECT["softened"])
    # R-004 不再是二元開關:三個實值出口都要有人住
    assert all(r4n.get(v) for v in ("good", "mixed", "poor")), r4n
    print("\n✅ 重模擬與報告宣稱的分佈一致(斷言全過)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
