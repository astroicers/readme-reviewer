# 第一次誤判批次處理(2026-09-02,12 條)→ rubric 0.2.0 / 工具 0.2.0

> `misjudgments.md` 待處理 12 條,達 5–10 門檻上緣後一次處理。
> **每條先查證再裁決**;裁決分四種:修 / 查證後刻意不修 / 轉待測 / 記入分歧。
> 結果:**8 條修、2 條刻意不修、2 條記分歧或使用陷阱**(細目見下)。

## 總覽

| # | 條目 | 查證結果 | 裁決 |
|---|------|---------|------|
| 1 | H-002「H1=repo 名」扣分 | spec 矛盾 + 實測零重疊(見 §1) | **修**:撤銷扣分、降 info、只報事實 |
| 2 | H-004 40% 觸發率 | 抽查 6/6 未標註 fence 是輸出/示意型(見 §2) | **刻意不修**門檻;補 known_false_positives |
| 3 | R-004 二元開關 | 18 份實測 mixed 僅 1 次(見 §3) | **修**:decision_order 三出口 → 五出口 |
| 4 | 機械同步判 poor(n=3) | 三種不同機械形式全漏接 | **修**:併入 §3 的 `equivalent_forms` |
| 5 | pass_criteria 無取值映射 | 首批判讀者被迫自選讀法 | **修**:rubric 加 `craft_value_mapping` |
| 6 | 形狀表缺索引/導覽型 | linux/anthropics-skills 無列可套 | **修**:SKILL.md 加一列(R-003 判導覽品質,不歸零) |
| 7 | `HEADING_RE` 只認 ATX | linux ATX 0/setext 15;choo HTML h1(見 §4) | **修**:三語法 + fence 遮罩 + frontmatter 剝除 |
| 8 | `github_slug` 折疊空白 | 12 個 anchor 死鏈全是此形狀 | **修**:逐空白換 `-`;標題先取渲染文字 |
| 9 | 不認 HTML 具名錨 | `<a name=>` GitHub 認我們不認 | **修**:`name=`/`id=` 進 own-anchor 集合 |
| 10 | H-005 需要完整 repo | 16 個相對路徑命中全無效 | **修文件 + 偵測**:rubric/SKILL.md 明寫前提;lint 對稀疏 root 主動警示 |
| 11 | 「求助/維護」零維度承載 | 兩獨立規範明文要求(見 §5) | **修**:新增 R-005,分母影響一起算 |
| 12 | 本 repo 違反 Short Description 規則 | spec 規定,GitHub Docs 無此條 | **記分歧**:README 註明,不改寫法 |

版本:rubric **0.1.0 → 0.2.0**(H-002 語義、R-004 改寫、R-005 新增、取值映射、形狀表);
工具 **0.1.0 → 0.2.0**(標題抽取、slug、具名錨、H-002 severity、稀疏 root 警示、`CRAFT_DIMS` 五維)。

---

## §1 H-002:撤銷「H1 等於 repo 名」的扣分

兩條獨立證據,方向一致:

1. **規範矛盾**:Standard Readme spec 明文 "Title must match repository, folder and
   package manager names" —— 舊版扣的正是規範要求的形狀,**與自己引用的來源打架**。
2. **實測零重疊**:12 份真實 README 中 H-002 未過 7 次,與 R-001 poor(2 次)**零交集**;
   5 個 logo 型未過者的 R-001 全是 good。⇒ H-002 的「定位」訊號在真實語料上**全是假陽性**,
   定位判斷 R-001 完全接得住(misjudgment 條目要求先確認這點,已確認)。

修法:pass = 有文字 H1(ATX/setext/HTML 皆認);「與 repo 名相同」降為事實回報;
severity warning → info。**「無文字 H1」仍回報**——logo 型是已文件化的 LLM 複核項。

## §2 H-004:查證後刻意不修

misjudgment 條目要求「先確認那 6 個命中裡有幾個是輸出型」。已抽查 3 個 repo 的全部
6 個未標註 fence:**目錄樹 1、`/plugin` 指令 1、對話樣張 2、ASCII 架構圖 1、ASCII 流程圖 1
—— 6/6 本就無語言可標**(```text 可標但非慣例)。且真實 README 語料 12/12 通過、
info 級不進 verdict。⇒ 門檻與 severity 都不動,rubric 補 known_false_positives 一段。

## §3 R-004:三出口 → 五出口,`mixed` 從兩側可達

舊結構的問題不是「太嚴」,是**出口太少**:「無易腐內容」對真實 README 幾乎不可能成立,
於是實際只剩「有陳述→good」與「無陳述→poor」兩個出口——18 份實測 R-004 標記
**good 7 / mixed 1 / poor 10**,12 個 poor 有 10 個出自它。

新 decision_order(rubric 0.2.0):

1. 有陳述 **且** 易腐內容帶時效/驗證 → good
2. 有陳述但易腐裸露**或已實際腐壞** → mixed
3. 無陳述但易腐內容有**機械同步形式** → mixed
4. 無陳述也無易腐內容 → n/a
5. 無陳述且易腐裸露 → poor

「機械同步形式」收進 `equivalent_forms`,三個實測實例、三種不同形式:
指向單一事實源(amplication 的 `engines` 指標)、repo 內相對路徑(linux 的
`Documentation/**`)、機械同步標記+CI(Jeffallan 的 `<!-- SKILL_COUNT -->`)。
**外部文件網站明文排除**——外部 docs 一樣會腐,只是腐在別處。

⚠️ 依處理紀律,**理由與數字不寫進 rubric 條文**(污染下一輪判讀),住在本報告與 CHANGELOG。

## §4 三個程式缺陷的修法與實測

全部見 `readme-reviewer/scripts/lint_readme.py` 與其 selftest 新增斷言。
**9 個突變逐個打過,9/9 轉紅,復原後全綠**(⚠️ 自跑突變只涵蓋自己想得到的形狀,
獨立複審仍是 land 前的必要步驟):

```
🔴 1 slug 退回折疊空白          🔴 6 拿掉具名錨
🔴 2 拿掉 setext 支援           🔴 7 rubric H-002 severity 改回 warning(drift)
🔴 3 拿掉 HTML 標題             🔴 8 rubric 的 R-005 改名(維度鍵 drift)
🔴 4 拿掉 fence 遮罩            🔴 9 evals 案例掉一維(鍵打錯)
🔴 5 拿掉 frontmatter 剝除
```

**修後對 12 份語料重跑**:

- `torvalds/linux`:H-002 ✗→✓(setext H1)、H-003 ✗→✓(`Quick Start` 現形)
- `choojs/choo`:H-002 ✗→✓(HTML `<h1>Choo</h1>`)
- **anchor 死鏈 12 → 0**(`art--design` 型全數解析)
- ⚠️ **一個行為變更要誠實記**:`amplication` 的 H-002 由 ✓ 轉 ✗。舊版把
  ```shell fence 裡的 `# running the server component` 當成 H1——**它以前是因錯誤的
  理由通過**。fence 遮罩後它回到真實狀態(HTML h1 是 logo-only,無文字),
  與其他 logo 型一樣交 LLM 複核。
- 修 heading 抽取時**一次修了同類的第四個面向**:fence 內的 markdown 連結不再進
  死鏈掃描(與 bash 註解變 H1 同根:掃了不該掃的區域)。

## §5 R-005「求助與維護」:新增維度,分母影響一起算

**依據**(皆 2026-09-02 逐字查證):GitHub Docs 五項內容的第 4、5 項
+ Standard Readme 的 Contributing("State where users can ask questions")與
Maintainers 條款獨立佐證。實測 12 份有 11 份寫了求助管道——讀者面的真實慣例,
判準此前完全看不見。

**設計上刻意避開 R-004 踩過的坑**:

- **缺席不設 poor**(GitHub 預設有 Issues 頁籤,缺席是弱點不是失格);
  poor 只保留給「寫了但已失效/誤導」——與 R-001 的「錯誤定位比沒有更糟」同構
- 「本專案不提供支援」是**合格答案**(判準是讀者知不知道處境,不是有沒有 Discord)
- 內部工具豁免 n/a(姊妹專案 packaging 0/14 系統性誤判內部 skill 的教訓)

**分母影響**(misjudgment 條目要求「兩件事要一起算」):rollup 門檻維持**絕對值 2**,
刻意不隨分母 4→5 調整;18 份重模擬顯示 R-005 造成的 verdict 變動只有兩個
**軟化**(approved → approved-with-notes),零個 needs-revision 翻轉——
新維度有牙齒,而且咬在設計的方向上(溫和)。

## §6 rubric 0.1.0 → 0.2.0 對 18 份判讀的重模擬

**數字由 `scripts/resimulate_18.py` 重算並斷言,已掛 CI**——改了判讀表沒改報告會轉紅。
每個新值附一行證據句(空證據被斷言擋下)。

| 分佈 | 舊(0.1.0) | 新(0.2.0) |
|---|---|---|
| approved | 3 | **1** |
| approved-with-notes | 4 | **7** |
| needs-revision | 11 | **10** |
| R-004 good/mixed/poor | 7 / 1 / 10 | 7 / **4** / **7** |
| R-005(新增) | — | good 10 / mixed 6 / poor 1 / n/a 1 |

**三個 verdict 變動,逐個講清楚**:

- `torvalds/linux`:needs-revision → approved-with-notes。**唯一由 R-004 改寫翻正的**
  ——repo 內相對路徑是機械同步,舊條文看不見。
- `claude-code-warp`、`ai/size-limit`:approved → approved-with-notes。**R-005 咬的**
  ——兩份都沒有可指認的求助管道與維護主體內文陳述(grep 實測)。這不是誤傷:
  size-limit 連 Contributing 段都沒有,而它是被人工策展收錄的「模範 README」——
  **策展標準(偏視覺/打包)與內容涵蓋面(規範要求)本來就不是同一件事**。

**R-004 不再是二元開關**:三個實值出口都有人住(7/4/7),斷言釘住。

⚠️ **重模擬不是校準**:兩批判讀者是同一人(rubric 作者)。它能回答的是
「條文改寫後判定怎麼變」,不能回答「判得準不準」。

## §7 逐條收尾與明確不做的事

- **#12 Short Description 分歧**:README 的證據性質段已加註——本 repo 定位句在
  blockquote 裡,違反 Standard Readme 的三條規則;**保留寫法**(GitHub Docs 無此規定,
  視覺效果是刻意的),但引用該規範就註明分歧。
- **H-002 misjudgment 的 n=15「53% 觸發率」**:那批含「與 repo 名相同」分支的觸發;
  雙抽樣框批次已證明 **7/12 全是另一支(無文字 H1)**,兩支已在修法中分開處置——
  bare-name 支撤銷、no-text 支保留為事實回報。
- **沒動 rollup 門檻**(`≥2 mixed` 維持):18 份重模擬下新分佈健康
  (needs-revision 11→10),沒有調整的證據基礎;它仍是「借來的門檻」,待測條目不變。
- **沒有宣稱任何一條「校準完成」**:本批所有重模擬都出自同一judge,見 §6 警語。

## 下一步

1. **派不知情的獨立判讀者**用 rubric 0.2.0 重跑 12+ 份——這仍是唯一能把
   「會開火」升級成「判得準」的動作(現在條文有了取值映射,信度測試才有意義)
2. R-005 累積跨批次觸發率紀錄(evidence_note 已標:首兩批重模擬不算)
3. 查證剩餘兩個 triangulation 來源(Make a README、Diátaxis)
