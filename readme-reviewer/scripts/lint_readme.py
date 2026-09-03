#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_readme.py — README 的確定性過濾器(**不是**品質結論)

分工(這是本專案最重要的一條設計):
  - 本檔:hygiene 門檻 + 安全紅旗 + 可機械查證的事實(死連結、code fence)
  - SKILL.md 的 LLM 層:craft 判讀 R-001~005 —— **那才是主判**

姊妹專案 skill-quality-research 跑完六個 phase 的結論是
「星數關聯的是打包面,不是內容工藝」。所以本檔刻意**不計品質分數**:
它只輸出門檻結果與待複核清單,`craft_verdict` 留白給 LLM 層填。

零依賴(stdlib only,Python 3.9+)。

用法:
    python3 lint_readme.py <repo 目錄>            # 人看
    python3 lint_readme.py <repo 目錄> --json     # 給 SKILL.md 層吃
    python3 lint_readme.py --selftest             # 純函式斷言(CI 用)
"""
import argparse
import json
import os
import re
import sys

# Windows 可攜性:輸出重導向時 Python 用 locale 編碼(cp1252/cp950),本工具的訊息含中文,
# 不處理會直接 UnicodeEncodeError 而不是印出結果。**出貨工具必須自己站得住**,
# 不能要求使用者先設 PYTHONUTF8=1。(reconfigure 是 3.7+;失敗就維持原狀,不擋主流程。)
#
# ⚠️ 這一段是 2026-09-02 首次 CI 紅燈補上的。在此之前 CI 的 windows job 註解寫著
# 「刻意用 PYTHONUTF8=0 驗證 lint 自己 reconfigure 得起來」—— 而**程式碼裡根本沒有
# reconfigure**。CI 步驟是從姊妹專案抄來的,對應的實作沒跟著抄。
# **註解宣稱了一個程式沒有的行為**,正是本工具自己在抓的形態。
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

MAX_READ = 2_000_000
README_NAMES = ("readme.md", "readme.markdown", "readme.rst", "readme.txt", "readme")

# ── craft verdict 的取值域與維度鍵 ──────────────────────────────────────────
CRAFT_DIM_VALUES = ("good", "mixed", "poor", "n/a")
CRAFT_DIMS = ("R-001", "R-002", "R-003", "R-004", "R-005")
CRAFT_VERDICT_VALUES = ("approved", "approved-with-notes", "needs-revision")

# ── hygiene 的門檻常數(rubric 是 canonical,這裡是可執行鏡像)────────────────
FENCE_LANG_MIN_PCT = 70.0        # H-004:code fence 標語言的最低比例
# severity 提到模組層,selftest 的 drift-guard 逐條與 rubric 對帳(ADR-031:
# 同一意義兩處編碼必 drift)。H-002 是 2026-09-02 批次處理降的 info,
# 理由與實測見批次處理報告(⚠️ 該報告第一版的「零重疊」統計是錯的,
# 獨立複審抓到後已更正 —— 以報告的更正版為準,不要抄舊說法)。
HYGIENE_SEVERITY = {"H-001": "error", "H-002": "info", "H-003": "warning",
                    "H-004": "info", "H-005": "warning"}

# ── security 靜態規則:(flag, rule id, severity, confidence)─────────────────
# 提到模組層是刻意的:evals 需要 flag→severity 的對應來判斷哪一條會翻 verdict。
# 讓它自己再抄一份就是「同一意義兩處編碼」,那會 drift。
SECURITY_RULES = [
    ("pipe_to_shell",      "S-001", "warning", "medium"),
    ("real_looking_secret", "S-002", "error",   "low-static-needs-llm"),
    ("obey_remote_output", "S-003", "warning", "low-static-needs-llm"),
]
SECURITY_SEVERITY = {f: s for f, _i, s, _c in SECURITY_RULES}

PIPE_TO_SHELL = re.compile(
    # 三種「下載即執行」形(同一 flag,S-001 極性照舊:標示 ≠ 扣分):
    #   管道形 curl|sh、行程替換形 bash <(curl …)、PowerShell irm … | iex
    # 後兩形是真實使用 B1 抓到的全盲(AI-SOP README 6 處,security 曾報 0)。
    r"(?i)(?:\b(?:curl|wget)\b[^\n|]{0,200}\|\s*(?:sudo\s+)?(?:ba|z|k)?sh\b"
    r"|\b(?:ba|z|k)?sh\s+<\(\s*(?:curl|wget)\b"
    r"|\b(?:irm|iwr|invoke-restmethod|invoke-webrequest)\b[^\n|]{0,200}\|\s*(?:iex|invoke-expression)\b)")
# 只認**高熵且帶已知前綴**的樣態。佔位符不算 —— 那是 README 的正常寫法。
REAL_SECRET = re.compile(
    r"\b(gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}\b"
    r"|xox[baprs]-[A-Za-z0-9-]{20,})")
SECRET_PLACEHOLDER = re.compile(r"(?i)(your[_-]?|<|\{\{|xxx|\.\.\.|example|placeholder|redacted)")
# ⚠️ 極性反轉是這一條在姊妹專案的具名前科:regex 曾把
# 「DO NOT PROCEED without confirmation」(強制確認)判成抑制確認。
# 所以這裡只收**正向祈使**的樣態,並在同句出現否定詞時消音。
OBEY_REMOTE = re.compile(
    r"(?i)(follow\s+(?:it|what\s+it\s+prints|the\s+output)\s+(?:exactly|to\s+the\s+letter)"
    r"|don'?t\s+stop\s+for\s+confirmation"
    r"|照\s*(?:它|其)?(?:印出|輸出)的?(?:內容)?(?:逐字)?執行)")
OBEY_NEGATION = re.compile(r"(?i)\b(do not|don'?t|never|must not|should not)\b|不要|不得|禁止|請勿")

# 已知未涵蓋 / 已知假陽性的樣態。**斷言它們目前的行為**,讓缺口可見、可轉紅。
# ⚠️ 這兩句**必須同時含觸發語與否定詞**,否則斷言恆真 ——
# 第一版寫的是不含觸發語的句子,`not obey_remote_hits(...)` 永遠成立,
# 拿掉否定詞消音也不會轉紅(突變測試當場抓到)。
OBEY_KNOWN_UNCOVERED = [
    "Do not follow it exactly — read the script first.",   # 含觸發語 + 否定,極性相反
    "請勿照它印出的內容逐字執行,先自己看過。",              # 中文同型
]
# ⚠️ 第一句**必須讓 REAL_SECRET 真的命中**,否則佔位符過濾從未被執行、斷言恆真。
SECRET_KNOWN_UNCOVERED = [
    "API_KEY=ghp_" + "A" * 36 + "   # replace with your own token",  # 命中但同行有佔位語
    "export API_KEY=$(pass show myservice)",             # 正當寫法,REAL_SECRET 本就不中
    "Set `GITHUB_TOKEN` to a token with `repo` scope.",  # 談論憑證,本就不中
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
# ── 2026-09-02 批次修:標題抽取原本只認 ATX,是「一個根因、三個面向」的實測缺陷 ──
# torvalds/linux(ATX 0、setext 15)讓 H-002/H-003/own-anchor 三處同時出錯;
# choojs/choo 的 <h1 align="center">Choo</h1> 有文字卻被報「無文字 H1」。
HTML_HEADING_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1\s*>", re.I | re.S)
SETEXT_UNDERLINE_RE = re.compile(r"^ {0,3}(=+|-{2,})[ \t]*$")
# setext 的內容行不得是這些形狀(否則 `---` 是分隔線/表格,不是底線)
SETEXT_CONTENT_EXCLUDE = re.compile(r"^\s*$|^\s{0,3}#|^\s*([-*+]|\d+[.)])\s|^\s*>|^\s*\||^\s*<")
# GitHub 認 HTML 的 id= 與 <a name=> 為 anchor 目標(amplication 實測)
ANCHOR_ATTR_RE = re.compile(r"<[a-zA-Z][^>]*?\b(?:name|id)\s*=\s*[\"']([^\"']+)[\"']", re.I)
IMG_MD_RE = re.compile(r"!\[([^\]\n]*)\]\([^)\s]*(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})([^\n`]*)$", re.M)
LINK_RE = re.compile(r"\[([^\]\n]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SECTION_KEYWORDS = re.compile(
    r"(?i)(install|usage|quick\s*start|getting\s+started|setup|how\s+to\s+use"
    r"|安裝|使用|快速開始|快速上手|入門)")


def read_text(p):
    # utf-8-sig:UTF-8 BOM 若留在第 0 字元,HEADING_RE 的 `^#` 與
    # `_strip_frontmatter` 的 startswith 都會在第一行失配(複審 F-11)。
    try:
        with open(p, encoding="utf-8-sig", errors="replace") as f:
            return f.read(MAX_READ)
    except OSError:
        return ""


def find_readme(root):
    """回傳 (相對路徑, 內容);找不到回傳 (None, "")。"""
    try:
        entries = sorted(os.listdir(root))
    except OSError:
        return None, ""
    for name in entries:
        if name.lower() in README_NAMES:
            full = os.path.join(root, name)
            if os.path.isfile(full):
                return name, read_text(full)
    return None, ""


def _heading_render_text(h):
    """slug 作用在**渲染後**的標題文字:圖片取 alt、連結取 text、剝 HTML tag。
    react 的 `### [Code of Conduct](url)` 若不先取 text,URL 字串會混進 slug。"""
    h = IMG_MD_RE.sub(r"\1", h)
    h = LINK_RE.sub(lambda m: m.group(1), h)
    return re.sub(r"<[^>]+>", "", h)


def github_slug(heading):
    """GitHub 的 anchor slug 規則。**CJK 字元保留** —— 本專案自己的標題就是中文。

    ⚠️ 空白是**逐個**換 `-`,不是折疊:`Art & Design` 去掉 `&` 剩兩個空白,
    GitHub 產出 `art--design`。2026-09-02 批次修 —— 折疊版讓 12 個真實 anchor
    (public-apis 8、awesome-python 2、choo 1)全數誤報死鏈,ground truth 是
    三個獨立高星 repo 從 GitHub UI 抄來的連結。
    已知近似:emoji 標題的 slug 未實測(語料中無內部 anchor 指向 emoji 標題)。"""
    s = _heading_render_text(heading).strip().lower()
    s = re.sub(r"[^\w\s一-鿿぀-ヿ가-힯-]", "", s)
    # ⚠️ 移除字元後**不得再 strip**:emoji 開頭標題(`📖 概述`)移除 emoji 剩前導空白,
    # GitHub 逐空白轉 `-` 且不 re-trim → 實際 anchor 是 `#-概述`。
    # 真實使用 B1 實測 23 個假陽性(backup-worker),ground truth=作者抄自 GitHub UI 的 TOC。
    return re.sub(r"\s", "-", s)


def _fence_regions(text):
    """成對(或未閉合)fence 的 (內文起, 內文迄, info)。

    閉合規則照 CommonMark:同字元且**長度 ≥ 開頭**(```` 內的 ``` 不會提早關閉外層)。
    未閉合的尾塊視為**延伸到檔尾** —— GitHub 同樣把其餘內容當程式碼渲染;
    第一版沒處理這個,未閉合 fence 裡的 `# comment` 仍會冒充 H1(複審 F-10)。"""
    open_m = None
    for m in FENCE_RE.finditer(text):
        if open_m is None:
            open_m = m
        elif m.group(2)[0] == open_m.group(2)[0] and len(m.group(2)) >= len(open_m.group(2)):
            yield open_m.end(), m.start(), open_m.group(3).strip()
            open_m = None
    if open_m is not None:
        yield open_m.end(), len(text), open_m.group(3).strip()


def mask_fences(text):
    """把 fenced code 區塊(含未閉合尾塊)換成等長空白,保留換行與偏移。

    標題/連結/anchor 抽取要在遮罩後的文本上做 —— amplication 的 ```shell 區塊裡
    `# running the server component` 曾被當成 H1,讓 H-002 **因錯誤的理由通過**。
    security regex 則刻意掃**原文**(指令本來就住在 fence 裡)。"""
    out = []
    last = 0
    for start, end, _info in _fence_regions(text):
        out.append(text[last:start])
        out.append("".join(c if c == "\n" else " " for c in text[start:end]))
        last = end
    out.append(text[last:])
    return "".join(out)


def _strip_frontmatter(text):
    """開頭的 YAML frontmatter 換成等長空白(closing `---` 會被誤認成 setext 底線)。

    ⚠️ 只有**長得像 YAML** 的區塊才剝:每個非空行須是 `key:`、註解或縮排續行。
    第一版只看「以 `---` 開頭」——以分隔線開場、文中另有 `---` 的 README
    會被整段塗白,真標題跟著消失(複審 F-12,與本批要修的根因同型)。"""
    if not text.startswith("---\n"):
        return text
    m = re.search(r"\n(---|\.\.\.)[ \t]*\n", text[4:])
    if not m:
        return text
    body = text[4:4 + m.start() + 1]
    for ln in body.splitlines():
        if not ln.strip() or ln.lstrip().startswith("#") or ln[:1] in (" ", "\t"):
            continue
        if not re.match(r"[\w\"'.-]+[ \t]*:", ln):
            return text
    end = 4 + m.end()
    return "".join(c if c == "\n" else " " for c in text[:end]) + text[end:]


def extract_headings(text):
    """回傳文件序的 [(level, text, pos)],涵蓋 ATX + setext + HTML 三種語法。

    fence 內文與 frontmatter 先遮罩;HTML 標題剝 tag 後**無文字者不計**
    (logo-only 的 <h1><img></h1> 不是文字標題 —— 那是 H-002 已文件化的形狀,
    要留給 LLM 複核,不能在這裡吞掉)。"""
    masked = _strip_frontmatter(mask_fences(text))
    found = []
    for m in HEADING_RE.finditer(masked):
        found.append((len(m.group(1)), m.group(2).strip(), m.start()))
    lines = masked.splitlines(keepends=True)
    pos = 0
    prev, prev_pos = "", 0
    for ln in lines:
        bare = ln.rstrip("\n")
        um = SETEXT_UNDERLINE_RE.match(bare)
        if um and prev.strip() and not SETEXT_CONTENT_EXCLUDE.match(prev) \
                and not SETEXT_UNDERLINE_RE.match(prev):
            found.append((1 if um.group(1)[0] == "=" else 2, prev.strip(), prev_pos))
            prev = ""          # 底線消耗掉內容行,連續兩條底線不會各配一次
        else:
            prev, prev_pos = bare, pos
        pos += len(ln)
    for m in HTML_HEADING_RE.finditer(masked):
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if txt:
            found.append((int(m.group(1)), txt, m.start()))
    return sorted(found, key=lambda t: t[2])


def fence_stats(text):
    """(區塊數, 帶語言標註數)。

    與 mask_fences 共用 `_fence_regions` 的配對規則(複審 F-16:第一版兩處
    配對邏輯不一致,且 docstring 宣稱「單獨一個 fence 不計」而程式照計 ——
    實際行為是**未閉合的尾塊也算一塊**,與 GitHub 渲染一致,docstring 改為照實寫)。"""
    total = tagged = 0
    for _s, _e, info in _fence_regions(text):
        total += 1
        if info:
            tagged += 1
    return total, tagged


def broken_links(text, root, readme_rel):
    """相對連結與同檔 anchor 的死連結。**不驗 http**(需要網路且會偽陰性)。

    ⚠️ 前提:`root` 是**完整的 repo**。只餵一個 README 檔時相對路徑全滅,
    那是抽樣假陽性不是死鏈(2026-09-02 實測踩過)。"""
    masked = mask_fences(text)
    own = {github_slug(h) for _lvl, h, _p in extract_headings(text)}
    # anchor 目標與連結掃描吃**同一份遮罩文本**(複審 F-09:第一版 anchor 收自
    # 原文,fence 裡示範用的 <a name=> 會讓真死鏈靜默變合法)。
    own |= {a.lower() for a in ANCHOR_ATTR_RE.findall(masked)}   # <a name=> / id=
    bad = []
    for m in LINK_RE.finditer(masked):
        tgt = m.group(2)
        if tgt.startswith(("http://", "https://", "mailto:")):
            continue
        path, _, anchor = tgt.partition("#")
        if not path:                                   # 同檔 anchor
            if anchor and anchor.lower() not in own:
                bad.append(tgt)
            continue
        full = os.path.normpath(os.path.join(root, path))
        if not os.path.exists(full):
            bad.append(tgt)
    return bad


def obey_remote_hits(text):
    """逐句判 + 否定詞消音。跨句合併會讓長條列的任何 `not` 變成消音海綿,
    所以刻意**不**做段落級合併 —— 這是姊妹專案實測過的失敗模式。"""
    hits = []
    for sent in re.split(r"[。！？!?\n]", text):
        if OBEY_REMOTE.search(sent) and not OBEY_NEGATION.search(sent):
            hits.append(sent.strip()[:120])
    return hits


def secret_hits(text):
    out = []
    for m in REAL_SECRET.finditer(text):
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        line = text[line_start: line_end if line_end != -1 else len(text)]
        if SECRET_PLACEHOLDER.search(line):
            continue
        out.append(m.group(0)[:12] + "…")
    return out


def craft_verdict_rollup(dimensions, hygiene_error=False, security_error_confirmed=False):
    """rubric 的 craft_verdict_rollup 的可執行鏡像。canonical 是 rubric.yaml。

    security_error_confirmed:**步驟 5 複核後確認成立**才傳 True。
        低信心紅旗單憑 lint 命中**不得**判 needs-revision。
    """
    if not dimensions:
        raise ValueError("dimensions 不得為空——五個維度每一條都要有值,"
                         "不適用請明寫 'n/a'(SKILL.md 步驟 4)")
    unknown = sorted(set(dimensions) - set(CRAFT_DIMS))
    if unknown:
        raise ValueError(f"未知的維度鍵:{unknown}(合法鍵 {list(CRAFT_DIMS)})")
    bad = {k: v for k, v in dimensions.items() if v not in CRAFT_DIM_VALUES}
    if bad:
        raise ValueError(f"維度取值域外:{bad}(合法值 {CRAFT_DIM_VALUES})")
    if hygiene_error:            return "needs-revision"          # 1
    if security_error_confirmed: return "needs-revision"          # 2
    vals = list(dimensions.values())
    if any(v == "poor" for v in vals):  return "needs-revision"   # 3
    n_mixed = sum(1 for v in vals if v == "mixed")
    if n_mixed >= 2:             return "needs-revision"          # 4
    if n_mixed == 1:             return "approved-with-notes"     # 5
    return "approved"                                             # 6


_RULE_SPLIT = re.compile(r"^\s*-\s+id:", re.M)


def parse_rubric_block(txt, top_key):
    """從 rubric.yaml 取出某個頂層清單下的規則塊。零依賴,不用 PyYAML。

    先剝**整行註解**,再以 `- id:` 切塊,欄位錨在行首縮排 —— 三者缺一不可:
      · 不剝註解 → 談論舊值的註解會被讀成值(姊妹專案實測過真 drift 完全空過)
      · 不切塊   → 跨塊非貪婪匹配會把 A 的欄位配到 B
      · 不錨行首 → 區塊純量裡的散文會被當成欄位
    欄位值容忍**行尾註解**。
    """
    clean = "\n".join(l for l in txt.splitlines() if not l.lstrip().startswith("#"))
    body = clean.split("\n" + top_key + ":", 1)
    if len(body) < 2:
        return {}
    seg = re.split(r"^[A-Za-z_][\w-]*:", body[1], maxsplit=1, flags=re.M)[0]
    out = {}
    for blk in _RULE_SPLIT.split(seg)[1:]:
        rid = blk.splitlines()[0].strip()
        fields = {}
        for m in re.finditer(r"^ {4}(\w+):[ \t]*([^\s#][^\n#]*?)[ \t]*(?:#[^\n]*)?$",
                             blk, re.M):
            fields[m.group(1)] = m.group(2).strip()
        # 逐 flag 的 confidence(縮排更深一層)
        cm = re.search(r"^ {4}confidence:[ \t]*(?:#[^\n]*)?$\n((?:^ {6}\S.*$\n?)+)", blk, re.M)
        if cm:
            fields["_confidence"] = dict(
                re.findall(r"^ {6}(\w+):[ \t]*([^\s#]+)", cm.group(1), re.M))
        out[rid] = fields
    return out


def analyze(root):
    rel, text = find_readme(root)
    n_fence, n_tagged = fence_stats(text)
    pct_tagged = round(100.0 * n_tagged / n_fence, 1) if n_fence else 100.0
    headings = extract_headings(text)
    h1 = [h for lvl, h, _p in headings if lvl == 1]
    repo_name = os.path.basename(os.path.abspath(root))
    h1_is_bare_name = bool(h1) and re.sub(r"[\W_]+", "", h1[0]).lower() == \
        re.sub(r"[\W_]+", "", repo_name).lower()
    # H-005 的抽樣陷阱偵測:root 幾乎只有 README(無子目錄、≤3 個非隱藏檔)
    # 時,相對路徑的死鏈更可能是「只餵了單檔」而不是真死鏈 —— 回報時明說。
    try:
        entries = [e for e in os.listdir(root) if not e.startswith(".")]
    except OSError:
        entries = []
    sparse_root = bool(rel) and len(entries) <= 3 and \
        not any(os.path.isdir(os.path.join(root, e)) for e in entries)
    return {
        "readme_path": rel,
        "readme_lines": text.count("\n") + 1 if text else 0,
        "nonempty": bool(text.strip()),
        "h1": h1[0] if h1 else None,
        "h1_is_bare_repo_name": h1_is_bare_name,
        "heading_count": len(headings),
        "has_usage_section": any(SECTION_KEYWORDS.search(h) for _l, h, _p in headings),
        "fence_total": n_fence,
        "fence_tagged": n_tagged,
        "fence_tagged_pct": pct_tagged,
        "sparse_root": sparse_root,
        "broken_links": broken_links(text, root, rel) if text else [],
        "_redflags": {
            "pipe_to_shell": bool(PIPE_TO_SHELL.search(text)),
            "real_looking_secret": bool(secret_hits(text)),
            "obey_remote_output": bool(obey_remote_hits(text)),
        },
        "_text": text,
    }


def build_findings(m):
    f = {"hygiene": [], "security": [], "craft_llm_todo": []}
    f["hygiene"].append({"id": "H-001", "pass": m["nonempty"],
                         "severity": HYGIENE_SEVERITY["H-001"],
                         "detail": f"README={m['readme_path'] or '(找不到)'}, "
                                   f"{m['readme_lines']} 行"})
    # H-002:pass = 有文字 H1(ATX/setext/HTML 皆認)。
    # 「H1 等於 repo 名」**只回報事實不扣分** —— Standard Readme spec 明文要求
    # 標題等於 repo 名,舊版扣這個分是與自己引用的規範打架(2026-09-02 批次修)。
    # 定位判斷整個歸 R-001:12 份實測,H-002 未過與 R-001 poor 零重疊。
    f["hygiene"].append({"id": "H-002", "pass": bool(m["h1"]),
                         "severity": HYGIENE_SEVERITY["H-002"],
                         "detail": (f"H1={m['h1']!r}" if m["h1"] else "無文字 H1")
                                   + ("(與 repo 名相同 —— 事實回報,不影響 pass)"
                                      if m["h1_is_bare_repo_name"] else ""),
                         "note": "logo 圖片取代 H1 時 lint 看不出來——交步驟 4 複核;"
                                 "定位好壞由 R-001 判,本條只報結構事實"})
    f["hygiene"].append({"id": "H-003", "pass": m["has_usage_section"],
                         "severity": HYGIENE_SEVERITY["H-003"],
                         "detail": f"安裝/使用段落={'有' if m['has_usage_section'] else '無'}",
                         "note": "awesome 清單型判 N/A,見步驟 3 形狀表"})
    f["hygiene"].append({"id": "H-004", "pass": m["fence_tagged_pct"] >= FENCE_LANG_MIN_PCT,
                         "severity": HYGIENE_SEVERITY["H-004"],
                         "detail": f"code fence {m['fence_tagged']}/{m['fence_total']} "
                                   f"帶語言標註({m['fence_tagged_pct']}%,門檻 {FENCE_LANG_MIN_PCT}%)",
                         "note": "目錄樹/對話樣張/ASCII 圖本就無語言可標——"
                                 "未標註 fence 屬此類時不是缺陷,見 rubric known_false_positives"})
    h5_note = "只驗相對路徑與同檔 anchor,不驗 http;需要完整 repo"
    if m["sparse_root"] and m["broken_links"]:
        h5_note += ("。⚠️ root 無子目錄且檔案極少——若這是抽出來的單檔 README,"
                    "相對路徑的死鏈是抽樣假陽性(教訓與實測見誤判批次報告)")
    f["hygiene"].append({"id": "H-005", "pass": not m["broken_links"],
                         "severity": HYGIENE_SEVERITY["H-005"],
                         "detail": (f"{len(m['broken_links'])} 個死連結:{m['broken_links'][:5]}"
                                    if m["broken_links"] else "相對連結與 anchor 全部可解析"),
                         "note": h5_note})
    rf = m["_redflags"]
    for flag, rid, sev, conf in SECURITY_RULES:
        if rf[flag]:
            f["security"].append({"id": rid, "flag": flag, "severity": sev, "confidence": conf})
    f["craft_llm_todo"] = list(CRAFT_DIMS)
    return f


def blocks(findings):
    """hygiene 是否有 error 級未過(gate 端消費的判定)。"""
    return any(h["severity"] == "error" and h["pass"] is False for h in findings["hygiene"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_dir", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.repo_dir:
        ap.error("需要 repo 目錄(或 --selftest)")
    # fails-open 修(fresh 小輪實錘):餵入檔案路徑/不存在路徑時,原版靜默輸出
    # 缺席型 findings(無 H1/無安裝段),五份相同輸出才被識破。非目錄一律硬失敗。
    if not os.path.isdir(a.repo_dir):
        print(f"❌ 不是目錄:{a.repo_dir}(本工具吃 repo 目錄,不吃 README 檔案路徑)",
              file=sys.stderr)
        return 2
    m = analyze(a.repo_dir)
    if m["readme_path"] is None:
        print("⚠️ 目錄內無 README——以下全部為缺席型 findings,別當成內容判定", file=sys.stderr)
    f = build_findings(m)
    if a.json:
        out = {"repo": a.repo_dir, "readme_path": m["readme_path"],
               "readme_lines": m["readme_lines"], "hygiene": f["hygiene"],
               "security": f["security"], "craft_llm_todo": f["craft_llm_todo"],
               "craft_verdict": None,
               "craft_verdict_note": "留白是刻意的——craft 是主判,由 SKILL.md 的 LLM 層填",
               "blocks": blocks(f)}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print(f"== readme-reviewer lint: {a.repo_dir} ==")
    print("[hygiene] " + "  ".join(
        f"{h['id']}={'✓' if h['pass'] else '✗'}" for h in f["hygiene"]))
    for h in f["hygiene"]:
        if not h["pass"]:
            print(f"   {h['severity']:7} {h['id']}  {h['detail']}")
    print("[security] " + ("; ".join(
        f"{s['id']}:{s['flag']}({s['confidence']})" for s in f["security"]) or "無紅旗"))
    print("[craft] PENDING-LLM —— R-001~005 由 SKILL.md 層判,**那才是主判**")
    print("\n措辭紀律:本輸出不是品質結論。lint 只做門檻與過濾。")
    return 0


# ════════════════════════════════════════════════════════════════════════
def selftest():
    import tempfile
    # ── rollup 六條規則各一 case(五維:R-001~R-005)─────────────────────
    D = lambda a, b, c, d, e: dict(zip(CRAFT_DIMS, (a, b, c, d, e)))
    ALLGOOD = D("good", "good", "good", "good", "good")
    assert craft_verdict_rollup(ALLGOOD, hygiene_error=True) == "needs-revision"          # 1
    assert craft_verdict_rollup(ALLGOOD, security_error_confirmed=True) == "needs-revision"  # 2
    assert craft_verdict_rollup(D("good", "poor", "good", "good", "good")) == "needs-revision"  # 3
    # ⚠️ 純 2-mixed 才對門檻值有鑑別力(3 個 mixed 在 >=2 與 >=3 下答案相同)
    assert craft_verdict_rollup(D("mixed", "mixed", "good", "good", "good")) == "needs-revision", \
        "恰 2 個 mixed 必須 needs-revision —— 這條釘的是門檻值本身"
    assert craft_verdict_rollup(D("good", "mixed", "good", "good", "good")) == "approved-with-notes"  # 5
    assert craft_verdict_rollup(ALLGOOD) == "approved"                                    # 6
    # n/a 邊界:絕對值 2,不是「非 n/a 過半」——加了 R-005 分母變 5,門檻不變
    assert craft_verdict_rollup(D("n/a", "n/a", "mixed", "mixed", "good")) == "needs-revision"
    assert craft_verdict_rollup(D("n/a", "n/a", "n/a", "mixed", "n/a")) == "approved-with-notes"
    assert craft_verdict_rollup(D("n/a", "n/a", "n/a", "n/a", "n/a")) == "approved"
    # 取值域與鍵的守衛:不合法要拋錯而非默默當成 good
    for bad, why in ((D("good", "GOOD", "good", "good", "good"), "大小寫變體"),
                     ({}, "空 dict"),
                     ({"R-01": "mixed", "R-002": "mixed"}, "打錯的鍵"),
                     ({"R-009": "poor"}, "未知鍵")):
        try:
            craft_verdict_rollup(bad); assert False, f"應拒絕:{why}"
        except ValueError:
            pass
    assert craft_verdict_rollup({"R-001": "good", "R-002": "mixed"}) == "approved-with-notes", \
        "合法子集仍可用——鍵的守衛只擋未知鍵"

    # ── security regex 的極性與假陽性 ───────────────────────────────────
    assert PIPE_TO_SHELL.search("curl -fsSL https://x/i.sh | sh")
    assert PIPE_TO_SHELL.search("curl -L https://x | sudo bash")
    assert not PIPE_TO_SHELL.search("curl -o out.sh https://x/i.sh   # 先看再跑")
    assert PIPE_TO_SHELL.search("bash <(curl -fsSL https://x/install.sh)"), "行程替換形(B1 全盲)"
    assert PIPE_TO_SHELL.search("irm https://x/install.ps1 | iex"), "PowerShell iex 形(B1 全盲)"
    assert not PIPE_TO_SHELL.search("bash <(cat local.sh)"), "非下載的行程替換不中"
    assert not PIPE_TO_SHELL.search("irm https://x/data.json | ConvertFrom-Json"), "irm 非執行不中"
    for u in OBEY_KNOWN_UNCOVERED:
        assert OBEY_REMOTE.search(u), \
            f"夾具沒有觸發語 → `not obey_remote_hits` 會是恆真斷言,測不到消音邏輯:{u}"
        assert not obey_remote_hits(u), f"極性反轉句不得命中:{u}"
    assert obey_remote_hits("Read what it prints and follow it exactly.")
    assert obey_remote_hits("照它印出的內容逐字執行")
    assert REAL_SECRET.search(SECRET_KNOWN_UNCOVERED[0]), \
        "第一句夾具必須讓 REAL_SECRET 命中,否則佔位符過濾從未被行使(恆真斷言)"
    for u in SECRET_KNOWN_UNCOVERED:
        assert not secret_hits(u), f"正當/談論性寫法不得命中:{u}"
    assert secret_hits("token: ghp_" + "A" * 36)
    assert not secret_hits("token: ghp_<YOUR_TOKEN_HERE>")

    # ── 標題抽取:ATX + setext + HTML(2026-09-02 批次修的回歸夾具)──────
    hs = extract_headings("Linux kernel\n============\n\nQuick Start\n-----------\n")
    assert [(l, t) for l, t, _ in hs] == [(1, "Linux kernel"), (2, "Quick Start")], hs
    assert not extract_headings("intro\n\n---\n"), "空行後的 --- 是分隔線不是底線"
    assert not extract_headings("- item\n---\n"), "列表項後的 --- 不是 setext"
    # ⚠️ 夾具是「表格列 + 裸 ---」:`|---|---|` 本來就不匹配底線 regex,
    # 拿它當夾具打不到 `^\s*\|` 排除分支(複審 F-13:名字宣稱驗 A、實際驗 B)
    assert not extract_headings("| a | b |\n---\n"), "表格列後的裸 --- 不是 setext"
    assert extract_headings("<h1 align='center'>Choo</h1>")[0][:2] == (1, "Choo")
    assert not extract_headings("<h1><img src='x.svg'></h1>"), \
        "logo-only 的 HTML h1 沒有文字,不得計為文字標題(留給 LLM 複核)"
    assert not extract_headings("```bash\n# 這是註解不是標題\n```\n"), \
        "fence 內文必須遮罩 —— amplication 的 bash 註解曾被當成 H1"
    assert not extract_headings("```bash\n# 未閉合 fence 的註解也不是標題\n"), \
        "未閉合 fence 延伸到檔尾(GitHub 同樣渲染為程式碼)—— 複審 F-10"
    assert not extract_headings("````md\n```\n# 巢狀範例裡的假標題\n```\n````\n"), \
        "閉合 fence 須同字元且長度 ≥ 開頭,``` 不得提早關閉 ```` —— 複審 F-10"
    assert extract_headings("---\ntitle: x\n---\n# T\n")[0][:2] == (1, "T"), \
        "frontmatter 的 closing --- 不是 setext 底線"
    # ⚠️ 鑑別力要件:真標題必須落在兩條 --- **之間** —— 第一版把標題放在
    # 第二條 --- 之後,塗白與否結果相同,拿掉 YAML 形狀檢查突變不轉紅(當場抓到)
    hr = extract_headings("---\n\n# T\n\nIntro para\n\n---\nmore\n")
    assert [(l, t) for l, t, _ in hr] == [(1, "T")], \
        f"以分隔線開場的 README 不是 frontmatter,不得整段塗白(複審 F-12):{hr}"
    two = extract_headings("A\n===\nB\n===\n")
    assert [(l, t) for l, t, _ in two] == [(1, "A"), (1, "B")], two
    # ⚠️ 有鑑別力的「底線消耗內容行」夾具:拿掉 `prev = \"\"` 重設,
    # 第二條底線會再配一次同一內容行 → 產出兩個重複標題(複審 F-14)
    dup = extract_headings("A\n===\n===\n")
    assert [(l, t) for l, t, _ in dup] == [(1, "A")], dup

    # ── slug 與死連結 ───────────────────────────────────────────────────
    assert github_slug("統計限制(必讀)") == "統計限制必讀", github_slug("統計限制(必讀)")
    # emoji 開頭:移除後的前導空白轉 `-`,不 re-trim(B1 實測 ground truth)
    assert github_slug("📖 概述") == "-概述", github_slug("📖 概述")
    assert github_slug("🚀 核心特性") == "-核心特性"
    assert github_slug("Getting Started!") == "getting-started"
    # ⚠️ 空白逐個換 `-`,不是折疊 —— 折疊突變會在這三條轉紅(ground truth 是
    # public-apis / awesome-python / choo 寫在 README 裡的真實 anchor)
    assert github_slug("Art & Design") == "art--design", github_slug("Art & Design")
    assert github_slug("app = choo([opts])") == "app--chooopts"
    assert github_slug("[Code of Conduct](https://code.fb.com/coc)") == "code-of-conduct", \
        "標題內的 markdown 連結要先取 text 再 slug(react 的標題形狀)"
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "docs"))
        open(os.path.join(td, "docs", "a.md"), "w", encoding="utf-8").write("x")
        md = ("# T\n\n## 章節\n\nSetext 段\n---------\n\n<a name=\"named_anchor\"></a>\n\n"
              "[ok](docs/a.md) [self](#章節) [dead](docs/nope.md) [anc](#nope) "
              "[se](#setext-段) [na](#named_anchor) [gh](#ghost_anchor)\n"
              "```md\n[fence 內的假連結](docs/ghost.md)\n<a name=\"ghost_anchor\"></a>\n```\n")
        open(os.path.join(td, "README.md"), "w", encoding="utf-8").write(md)
        bad = broken_links(md, td, "README.md")
        assert sorted(bad) == ["#ghost_anchor", "#nope", "docs/nope.md"], \
            (f"setext 標題與 <a name=> 都是合法 anchor 目標;fence 內連結不掃、"
             f"fence 內的 <a name=> 也**不算目標**(複審 F-09):{bad}")
        # BOM:read_text 必須剝掉,否則第一行的 ATX H1 與 frontmatter 判定同時失配
        bp = os.path.join(td, "bom", "README.md")
        os.makedirs(os.path.dirname(bp))
        with open(bp, "wb") as f:
            f.write(b"\xef\xbb\xbf# BomTitle\n")
        assert analyze(os.path.dirname(bp))["h1"] == "BomTitle", \
            "UTF-8 BOM 未剝除,第一行 ATX H1 消失(複審 F-11)"
        # H-002 的 bare-name 語義:H1 = 目錄名 → pass 且 detail 照報事實
        # (複審 F-03:第一版四個 fixture 沒有一個 H1 等於目錄名,把 pass 邏輯
        #  改回扣分版全綠 —— 語義半邊零守衛)
        np_ = os.path.join(td, "acme")
        os.makedirs(np_)
        open(os.path.join(np_, "README.md"), "w", encoding="utf-8").write(
            "# acme\n\n定位句。\n\n## 安裝\nx\n")
        nf = build_findings(analyze(np_))
        nh2 = next(h for h in nf["hygiene"] if h["id"] == "H-002")
        assert nh2["pass"] is True, "H1 等於 repo 名不得扣分(Standard Readme Title 規則)"
        assert "與 repo 名相同" in nh2["detail"], "bare-name 是要照報的事實,不能靜默"

    # ── fence 統計 ──────────────────────────────────────────────────────
    t, g = fence_stats("```py\nx\n```\n\n```\ny\n```\n")
    assert (t, g) == (2, 1), (t, g)

    # ── drift-guard:硬編值必須與 rubric.yaml 一致 ───────────────────────
    rp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "references", "rubric.yaml")
    assert os.path.isfile(rp), f"drift-guard 找不到 {rp} —— 出貨副本不完整,不是可以跳過的情況"
    rub = read_text(rp)
    sec = parse_rubric_block(rub, "security")
    checked = 0
    for flag, rid, sev, conf in SECURITY_RULES:
        assert rid in sec, f"drift-guard 覆蓋缺口:rubric 沒有 {rid}"
        assert sec[rid].get("severity") == sev, \
            f"drift: {rid} severity lint={sev} rubric={sec[rid].get('severity')}"
        rconf = sec[rid].get("_confidence", {})
        assert rconf.get(flag) == conf, \
            f"drift: {flag} confidence lint={conf} rubric={rconf.get(flag)}"
        checked += 1
    assert checked == len(SECURITY_RULES), (checked, len(SECURITY_RULES))
    hyg = parse_rubric_block(rub, "hygiene")
    for hid, hsev in HYGIENE_SEVERITY.items():
        assert hid in hyg, f"drift-guard:rubric 缺 {hid}"
        assert hyg[hid].get("severity") == hsev, \
            f"drift: {hid} severity lint={hsev} rubric={hyg[hid].get('severity')}"
    assert HYGIENE_SEVERITY["H-001"] == "error", "H-001 必須是 error(唯一擋 gate 的門檻)"
    # craft 維度鍵也要同源:rubric 的 craft_llm 條目集合 == CRAFT_DIMS
    craft_ids = set(parse_rubric_block(rub, "craft_llm"))
    assert craft_ids == set(CRAFT_DIMS), \
        f"drift: craft 維度鍵 lint={sorted(CRAFT_DIMS)} rubric={sorted(craft_ids)}"
    # rollup 取值域:**集合相等**,不是逐個 in
    #(逐個 in 會被子字串吃掉:'approved' in 'approved-with-notes' 恆真)
    mv = re.search(r"^  values: \[([^\]]*)\]", rub, re.M)
    assert mv, "rubric 缺 craft_verdict_rollup.values —— 取值域無 canonical 來源"
    assert {v.strip() for v in mv.group(1).split(",")} == set(CRAFT_VERDICT_VALUES), \
        "取值域漂移:rubric 與程式不一致"
    # 門檻常數也要對得上
    assert f"{int(FENCE_LANG_MIN_PCT)}%" in rub or f"{FENCE_LANG_MIN_PCT}" in rub, \
        "H-004 的門檻值在 rubric 裡找不到(守衛綁 FENCE_LANG_MIN_PCT,改常數不改 rubric 會轉紅)"

    # ── 負向:解析器要讀得懂「值」而不是「談論值的註解」───────────────────
    # ⚠️ 註解必須放在**真值之後**才有鑑別力:本解析器逐行 finditer、後者覆蓋前者,
    # 註解在前會被真值蓋掉,`assert == 真值` 於是恆真(突變測試當場抓到第一版就是這樣)。
    anchor = "    severity: error\n    confidence:\n      real_looking_secret:"
    masked = rub.replace(anchor,
                         "    severity: error\n    # 舊值曾是 severity: warning\n"
                         "    confidence:\n      real_looking_secret:", 1)
    assert masked != rub, "F1 回歸夾具的 anchor 失效——請同步更新(測試本身壞了比漏測更糟)"
    assert "# 舊值曾是 severity: warning" in masked
    assert parse_rubric_block(masked, "security")["S-002"]["severity"] == "error", \
        "解析器讀到了談論舊值的註解而非真值(塊內註解可遮蔽 drift-guard)"

    # ── 可攜性守衛:每個會印中文的 Python 進入點都必須有 reconfigure ──────────
    # ⚠️ 這條是 2026-09-02 兩次 Windows CI 紅燈換來的。第一次是 CI 註解宣稱了
    # 程式沒有的行為;第二次是我**只修了報紅的那一支**,run_evals.py 同樣印中文卻漏掉。
    # 現在由程式檢查整個 repo,而不是等 Windows runner 一支一支告訴我。
    _root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _missing = []
    for _dp, _dn, _fn in os.walk(_root):
        _dn[:] = [d for d in _dn if d not in (".git", "__pycache__", "fixtures")]
        for _f in _fn:
            if not _f.endswith(".py"):
                continue
            _src = read_text(os.path.join(_dp, _f))
            _is_entry = "__main__" in _src
            _prints_cjk = any(ord(c) > 127
                              for _m in re.findall(r"print\(([^\n]*)", _src) for c in _m)
            # ⚠️ 比對的是**呼叫**而非字面字串:註解裡本來就有 "reconfigure" 這個字,
            # 用 `in _src` 會被自己的說明文字餵飽 —— 那正是本守衛要抓的形態。
            # 也要求帶 encoding 參數:`reconfigure(errors=...)` 修不了編碼問題。
            _has_call = re.search(r"\.reconfigure\s*\(\s*encoding\s*=", _src)
            if _is_entry and _prints_cjk and not _has_call:
                _missing.append(os.path.relpath(os.path.join(_dp, _f), _root))
    assert not _missing, (
        f"這些進入點會印非 ASCII 卻沒有 stdout/stderr 的 reconfigure,"
        f"在 Windows 重導向時會 UnicodeEncodeError:{_missing}")
    # 同一根因的另外兩種面貌 —— **寫者側修好不等於讀者側也好了**。
    # 三次 Windows CI 紅燈換來的清單:encode(stdout)、decode(subprocess)、open()。
    #
    # ⚠️ **本檔自己不在掃描範圍內,而且那是刻意的。** 前三版試著讓它掃自己,
    # 連續踩了三個自我指涉:偵測器的字面字串命中自己、逐行標記漏了訊息字串、
    # 連 sentinel 的偵測行都含 sentinel。**靜態掃自己是條爛路。**
    # 本檔改用**更強的驗證**:CI 的 windows job 在 `PYTHONUTF8=0` 下直接執行本檔
    # —— 那是行為驗證,比 grep 自己的原始碼可靠。
    _self = os.path.abspath(__file__)
    _enc = []
    for _dp, _dn, _fn in os.walk(_root):
        _dn[:] = [d for d in _dn if d not in (".git", "__pycache__", "fixtures")]
        for _f in _fn:
            if not _f.endswith(".py") or os.path.abspath(os.path.join(_dp, _f)) == _self:
                continue
            _rel = os.path.relpath(os.path.join(_dp, _f), _root)
            for _i, _l in enumerate(read_text(os.path.join(_dp, _f)).splitlines(), 1):
                if _l.lstrip().startswith("#"):
                    continue
                # ⚠️ 檢查**整行**有沒有 `encoding=`,不是 open() 的括號內 ——
                # `open\(([^)]*)\)` 會被巢狀括號截斷:
                # `open(os.path.join(a, b), encoding="utf-8")` 的 `[^)]*` 停在
                # `os.path.join(` 的右括號,於是看不到後面的 encoding(實測踩過)。
                _has_enc = "encoding=" in _l
                if ("text=True" in _l or "universal_newlines=True" in _l) and not _has_enc:
                    _enc.append(f"{_rel}:{_i} subprocess text=True 未指定 encoding")
                if re.search(r"(?<![\w.])open\s*\(", _l) and not _has_enc \
                        and not re.search(r"[\"']\s*[rwa]b[\"']", _l):
                    _enc.append(f"{_rel}:{_i} open() 未指定 encoding")
    assert not _enc, ("這些 I/O 邊界會吃 Windows 的 locale 編碼(cp1252),"
                      f"三次 CI 紅燈都出在這一類:{_enc}")

    # ── fails-open 修的負向 case:非目錄一律硬失敗(fresh 小輪實錘)────────
    import subprocess as _sp
    with tempfile.TemporaryDirectory() as td:
        fake = os.path.join(td, "README.md")
        open(fake, "w", encoding="utf-8").write("# x\n")
        r = _sp.run([sys.executable, os.path.abspath(__file__), fake],
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert r.returncode == 2 and "不是目錄" in r.stderr, \
            f"檔案路徑應硬失敗:rc={r.returncode} err={r.stderr[:80]!r}"
        r2 = _sp.run([sys.executable, os.path.abspath(__file__),
                      os.path.join(td, "no-such-dir")], capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert r2.returncode == 2, "不存在路徑應硬失敗"
        empty = os.path.join(td, "empty"); os.makedirs(empty)
        r3 = _sp.run([sys.executable, os.path.abspath(__file__), empty],
                     capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert r3.returncode == 0 and "缺席型" in r3.stderr, "真目錄無 README 應明示警告"

    print("[selftest] lint_readme: 全部通過 ✔"
          f"(rollup 6 規則 + n/a 邊界 + 鍵/值域守衛;"
          f"drift-guard 比對 {checked}/{len(SECURITY_RULES)} 條 severity+confidence"
          f" 與 5 條 hygiene severity + {len(CRAFT_DIMS)} 個 craft 維度鍵;"
          f"另檢查全 repo 進入點的 UTF-8 reconfigure)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
