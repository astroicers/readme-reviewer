#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_evals.py — readme-reviewer 的行為迴歸測試

與 `lint_readme.py --selftest` 的分工:
  - selftest 測「純函式與單一判定」(regex、rollup、drift-guard)
  - 本檔測「**對整個 repo 的端到端行為契約**」——擋/不擋分界、形狀豁免、security 語意

**所有 fixture 都進版控**,不依賴任何外部 clone ——
只跑在未進版控語料上的斷言會在 CI 上 skip,那等於用 skip 換一個「已驗證」的錯覺。

用法:
    python3 run_evals.py         # 全部
    python3 run_evals.py --ci    # 同上(fixtures 一律在版控內,無 skip 概念)
"""
import json
import os
import subprocess
import sys

# Windows 可攜性:本檔的契約名稱含中文,重導向時走 locale 編碼會 UnicodeEncodeError。
# ⚠️ 2026-09-02:第一次修這個問題時**只補了 lint_readme.py**(那支才是報紅的),
# run_evals.py 同樣印中文卻漏掉 —— 於是 CI 再紅一次,失敗步驟換成 `Eval regression`。
# **修的是報紅的那一支,不是同一類的全部。** 現在改為對每個 Python 進入點系統性檢查。
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(os.path.dirname(HERE), "scripts", "lint_readme.py")
FIXTURES = os.path.join(HERE, "fixtures")

SECURITY_REVIEW_VALUES = ("confirmed", "false-positive")


def _lint_module():
    """import lint_readme,`sys.path` 只動一次(避免每次呼叫都 insert)。"""
    p = os.path.join(os.path.dirname(HERE), "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import lint_readme as L
    return L


def lint(repo, *extra):
    # ⚠️ `text=True` 在 Windows 用 **locale 編碼**解子行程的 stdout(cp1252),
    # 而子行程寫的是 UTF-8 → UnicodeDecodeError,`r.stdout` 變 None,
    # 接著 `json.loads(None)` 拋 TypeError。**寫者側修好不等於讀者側也好了。**
    # 這是同一個根因(Windows locale 編碼)的第三種面貌,也是第三次 CI 紅燈。
    r = subprocess.run([sys.executable, LINT, repo, "--json", *extra],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise AssertionError(f"lint 執行失敗 rc={r.returncode}: {r.stderr[:200]}")
    return json.loads(r.stdout)


def spec():
    return json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))


def hyg(d, rid):
    return next(h for h in d["hygiene"] if h["id"] == rid)


# ── schema:預期行為住在案例檔,程式端**無預設值** ──────────────────────────
# 有預設值會讓「漏填」看起來像「刻意宣告」。缺欄一律炸。
def expect_block(expected, who="?"):
    if "expect_block" not in expected:
        raise AssertionError(f"{who}: 缺 `expect_block` —— 每個 case 都要明說該不該擋,"
                             "不得靠程式端的預設值")
    v = expected["expect_block"]
    if not isinstance(v, bool):
        raise AssertionError(f"{who}: `expect_block` 必須是布林,實得 {v!r}")
    if not expected.get("expect_block_reason"):
        raise AssertionError(f"{who}: 標了 `expect_block` 就要附 `expect_block_reason` —— "
                             "布林值說不出『因為 H-001』還是『因為根本沒 error』")
    return v


def security_confirmed(expected, who="?"):
    """evals.json 的 security → rollup 的 `security_error_confirmed`。

    只有**經步驟 5 複核確認成立**且 **severity 為 error** 的紅旗才翻 verdict。
    severity 查 `lint_readme.SECURITY_SEVERITY`,不在 evals 再編一次。
    """
    L = _lint_module()
    out = False
    for e in expected.get("security") or []:
        if not isinstance(e, dict):
            raise AssertionError(f"{who}: security 必須是物件陣列(字串陣列語意含混):{e!r}")
        for k in ("id", "flag", "review"):
            if not e.get(k):
                raise AssertionError(f"{who}: security 條目缺必填欄位 `{k}`:{e}")
        if e["review"] not in SECURITY_REVIEW_VALUES:
            raise AssertionError(f"{who}: review 取值域外:{e['review']}")
        if e["flag"] not in L.SECURITY_SEVERITY:
            raise AssertionError(f"{who}: 未知 flag `{e['flag']}` —— 與 SECURITY_RULES 不同步")
        if e["review"] == "confirmed" and L.SECURITY_SEVERITY[e["flag"]] == "error":
            out = True
    return out


def case_verdict(expected, who="?"):
    """一個 case 的 expected → rollup 算出的 verdict。

    抽成函式是為了讓斷言能行使**同一條路徑** —— 否則
    `security_confirmed(...)` 的呼叫點退回 `bool(...)` 不會被任何斷言接到。
    """
    L = _lint_module()
    return L.craft_verdict_rollup(
        expected["craft_dimensions"],
        hygiene_error=str(expected.get("hygiene", "")).startswith("FAIL"),
        security_error_confirmed=security_confirmed(expected, who))


# ── 行為契約 ────────────────────────────────────────────────────────────
def c_fixture_behaviour():
    """每個 case 的 fixture 實跑,擋/不擋與 hygiene 逐條對上 evals.json。"""
    for c in spec()["cases"]:
        who = c["fixture"]
        d = lint(os.path.join(FIXTURES, who))
        want = expect_block(c["expected"], who)
        assert d["blocks"] is want, f"{who}: 擋={d['blocks']} 但預期={want}"
        declared_fail = str(c["expected"].get("hygiene", "")).startswith("FAIL")
        assert (not hyg(d, "H-001")["pass"]) is declared_fail, \
            f"{who}: H-001 實測與 evals 宣告的 hygiene 欄不一致"
        # ⚠️ 逐條釘住,不是只釘 H-001。第一版只驗 blocks 與 H-001,於是把
        # good-readme 的安裝段標題改壞**不會轉紅**(H-003 是 warning,blocks 不變)
        # —— 突變測試當場抓到這個覆蓋缺口。
        want_h = c["expected"].get("hygiene_pass")
        assert want_h, f"{who}: 缺 `hygiene_pass` —— 每條 hygiene 的預期要住在案例檔"
        got_h = {x["id"]: x["pass"] for x in d["hygiene"]}
        assert got_h == want_h, f"{who}: hygiene 逐條不符\n  實測 {got_h}\n  預期 {want_h}"


def c_security_matches_lint():
    """凡標了 `security`,lint 必須真的在該 fixture 命中該 flag。

    標註與偵測脫節就是『證據說謊』——這條讓它不可能靜默發生。
    """
    n = 0
    for c in spec()["cases"]:
        ents = c["expected"].get("security") or []
        if not ents:
            continue
        security_confirmed(c["expected"], c["fixture"])       # schema 先過
        got = {s["flag"] for s in lint(os.path.join(FIXTURES, c["fixture"]))["security"]}
        for e in ents:
            assert e["flag"] in got, \
                (f"{c['fixture']}: evals 標了 {e['id']}/{e['flag']} 但 lint 沒命中"
                 f"(實得 {got})—— 標註與偵測脫節")
            n += 1
    assert n >= 1, "沒有任何 case 行使 security 標註,這條斷言等於沒跑"


def c_rollup_matches_evals():
    """evals 標的 craft_verdict 必須等於 rollup 純函式算出來的。"""
    n = 0
    L = _lint_module()
    for c in spec()["cases"]:
        e = c["expected"]
        if not e.get("craft_dimensions"):
            continue
        # SKILL.md:「每一個維度都要有值,不得略過」。rollup 接受子集是給程式彈性,
        # 案例檔沒有這個彈性 —— 少一維的案例會讓「新維度從 evals 消失」靜默通過。
        declared = set(e["craft_dimensions"])
        assert declared == set(L.CRAFT_DIMS), \
            (f"{c['fixture']}: craft_dimensions 必須五維俱全,"
             f"缺 {sorted(set(L.CRAFT_DIMS) - declared)} 多 {sorted(declared - set(L.CRAFT_DIMS))}")
        got = case_verdict(e, c["fixture"])
        assert got == e["craft_verdict"], \
            f"{c['fixture']}: rollup 算出 {got} 但 evals 標 {e['craft_verdict']}"
        n += 1
    assert n >= 3, f"標了 craft_dimensions 的 case 只有 {n} 個 —— rollup 覆蓋不足"


def c_verdict_domain_and_coverage():
    """取值域**集合相等**,且三態各至少被行使一次。

    ⚠️ 集合相等而非逐個 `in`:`'approved' in 'approved-with-notes'` 恆真,
    逐個 in 的那圈永遠不可能獨立失敗。
    """
    L = _lint_module()
    seen = {c["expected"].get("craft_verdict") for c in spec()["cases"]}
    bad = seen - set(L.CRAFT_VERDICT_VALUES)
    assert not bad, f"evals 的 craft_verdict 落在取值域外:{sorted(bad)}"
    missing = set(L.CRAFT_VERDICT_VALUES) - seen
    assert not missing, \
        f"取值域有值零覆蓋:{sorted(missing)} —— 合法化了卻沒有案例行使它"


def c_shape_exemption_is_exercised():
    """必須有 case 行使**形狀豁免**(某維度判 n/a)。

    形狀判定是本工具最大的誤判來源;沒有 case 行使它,等於那條路徑沒被測過。
    """
    na = [(c["fixture"], k) for c in spec()["cases"]
          for k, v in (c["expected"].get("craft_dimensions") or {}).items() if v == "n/a"]
    assert na, "沒有任何 case 行使 n/a(形狀豁免)—— 那條路徑沒被測過"
    shapes = {c["shape"] for c in spec()["cases"]}
    assert len(shapes) >= 3, f"只涵蓋 {len(shapes)} 種形狀,形狀表的鑑別力不足:{shapes}"


def c_no_readme_is_the_only_blocker():
    """擋/不擋兩側都要有 case,否則分界沒有被行使。"""
    blk = [c["fixture"] for c in spec()["cases"] if c["expected"]["expect_block"]]
    ok = [c["fixture"] for c in spec()["cases"] if not c["expected"]["expect_block"]]
    assert blk and ok, f"擋/不擋分界未被行使:擋={blk} 不擋={ok}"


CASES = [
    ("fixture 行為與 evals 宣告一致", c_fixture_behaviour),
    ("security 標註與 lint 實測對帳", c_security_matches_lint),
    ("rollup 與 evals 逐案對帳", c_rollup_matches_evals),
    ("verdict 取值域與三態覆蓋", c_verdict_domain_and_coverage),
    ("形狀豁免(n/a)有被行使", c_shape_exemption_is_exercised),
    ("擋/不擋分界兩側都有 case", c_no_readme_is_the_only_blocker),
]


def main():
    failed = 0
    print("── 行為契約(fixtures 全部在版控內,CI 必跑)──")
    for name, fn in CASES:
        try:
            fn()
            print(f"  ✓ {name}")
        except (AssertionError, ValueError) as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    print()
    if failed:
        print(f"❌ {failed} 個案例失敗")
        return 1
    print(f"✅ 全部通過({len(CASES)} 條契約 × {len(spec()['cases'])} 個 fixture)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
