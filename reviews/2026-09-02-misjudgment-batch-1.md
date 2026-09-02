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

> ⚠️ **本節第一版的第 2 條證據是錯的,獨立複審(F-01/F-02)抓到後更正如下。**
> 原版寫「未過與 R-001 poor 零交集;5 個 logo 型未過者 R-001 全是 good」——
> 重算後**交集是 1 不是 0**(`sindresorhus/awesome`:H-002 未過且 R-001 poor),
> 「全是 good」也不成立(`fiber` 是 mixed)。**而且那 7 次未過全是「無文字 H1」支——
> bare-name 支在該批零次觸發**(抽樣目錄名帶前綴),拿它支持撤銷 bare-name 扣分
> 正是雙抽樣框報告自己警告過的「混為一談會讓證據說謊」。我又犯了一次。

更正後的證據結構,**兩支分開講**:

- **bare-name 支(撤銷扣分的對象)**:證據是 (a) **規範矛盾** —— Standard Readme spec
  明文 "Title must match repository, folder and package manager names",舊版扣的正是
  規範要求的形狀,與自己引用的來源打架;(b) Phase 6 的 n=15 語料中 bare-name 支確實開火
  (含本 repo 自身,而其定位句就在 H1 下一行,運作良好)。**沒有 12 份批次的統計支持
  ——那批打不到這一支。**
- **no-text-H1 支(保留回報、severity 降 info 的對象)**:12 份中未過 7 次,
  其中 6 次的 R-001 是 good/mixed(定位由 logo+tagline 承載,R-001 判得出來);
  唯一的 R-001 poor(`awesome`)成因是**廣告佔屏**,與 H1 形式無關。
  ⇒ 把 H-002 當定位訊號會誤標大多數定位良好的 README;它的價值是結構事實回報。

修法:pass = 有文字 H1(ATX/setext/HTML 皆認);「與 repo 名相同」降為事實回報;
severity warning → info。**「無文字 H1」仍回報**——logo 型是已文件化的 LLM 複核項。
⚠️ 語義半邊(bare-name 不扣分)第一版**零守衛**(複審 F-03)——四個 fixture 沒有一個
H1 等於目錄名,把 pass 邏輯改回扣分版全綠。已補 bare-name 夾具斷言 + 突變。

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
第一輪 **9 個突變 9/9 轉紅**;獨立複審(見 §8)點名 5 個未涵蓋的邊界後,
守衛與突變清單擴充到 **17 個,17/17 轉紅、復原後全綠**。
(⚠️ 自跑突變只涵蓋自己想得到的形狀 —— 第一輪的 9/9 就漏了複審找到的那 5 類,
而且擴充時**又**抓到一個沒有鑑別力的夾具,見 §8。)

```
🔴 01 slug 退回折疊空白         🔴 10 H-002 pass 改回 bare-name 扣分(F-03)
🔴 02 拿掉 setext 支援          🔴 11 拿掉表格列排除分支(F-13)
🔴 03 拿掉 HTML 標題            🔴 12 拿掉底線消耗重設(F-14)
🔴 04 拿掉 fence 遮罩(標題)    🔴 13 未閉合尾塊不遮罩(F-10)
🔴 05 拿掉 frontmatter 剝除     🔴 14 閉合不查長度(F-10 巢狀)
🔴 06 拿掉具名錨                🔴 15 anchor 收自未遮罩原文(F-09)
🔴 07 rubric H-002 severity     🔴 16 BOM 不剝(F-11)
🔴 08 rubric R-005 鍵 drift     🔴 17 frontmatter 不查 YAML 形狀(F-12)
🔴 09 evals 案例掉一維
```

每個突變的**紅燈原文**(第一行 AssertionError)已錄於 §8 附錄——
複審的「待補證據 1」指出第一輪只交了修復後的綠燈,沒交紅燈證據,這裡補上。

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
Maintainers 條款獨立佐證。實測 12 份有 **10 份**寫了可指認的求問管道——
讀者面的真實慣例,判準此前完全看不見。
(⚠️ 第一版寫 11 份,複審 F-07 抓到與本批自己的 R-005 判讀矛盾:`ai/size-limit`
與 `sindresorhus/awesome` 都沒有 —— size-limit 連 Contributing 段都沒有,
指向 estimo 的 issue 連結是**別的 repo** 的;已重數更正。)

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


---

## §8 獨立複審回合(reality-checker,NEEDS_WORK → 修正)

依 land 政策,本批(實質邏輯改動)於 merge 前派**獨立唯讀 reviewer**
(工具白名單 Read/Grep/Glob,證據由呼叫端先落檔)。
判定 **NEEDS_WORK(正面 9 / 反面 12,另 5 項既有/低度)** —— 這是它該有的樣子:
第一輪自跑的 9/9 突變全綠**不構成證據**,只有讓別人來打它才算。

### 它抓到的,按嚴重度

| # | 發現 | 處置 |
|---|------|------|
| F-01 | **§1 的「零重疊」統計被本 PR 自己的資料表推翻**(交集=1:`sindresorhus/awesome`;「全 good」也偽:`fiber` 是 mixed) | ✅ 重算並改寫 §1,三處複本(CHANGELOG、lint 模組註解)同步更正 |
| F-02 | **該統計整個屬於另一支**(那 7 次未過全是 no-text 支;bare-name 支該批零觸發)——雙抽樣框報告自己警告過「混為一談會讓證據說謊」,我又犯一次 | ✅ §1 改為兩支分開舉證;bare-name 支承認只有 spec 矛盾 + n=15 語料 |
| F-03 | H-002 語義半邊(bare-name 不扣分)**零守衛**——改回扣分版全綠 | ✅ 補 bare-name 夾具斷言 + 突變 10 |
| F-04 | R-005 鏈斷在 plugin/marketplace 描述(仍寫 four dimensions,本 commit 只動了版本號) | ✅ 兩份描述改五維;CI 新增守衛(描述必須引用 `R-001~{CRAFT_DIMS[-1]}`) |
| F-05 | evals 案例名寫「四維俱全」、斷言驗五維 | ✅ 文案對齊 |
| F-06 | awesome-list fixture 的 R-005=good 不被內容支撐(「收錄建議開 issue」≠ 求問管道,同批對同形狀的 awesome 判 mixed 的理由正是這個),且該值承重(改 mixed 會翻 verdict) | ✅ fixture 補真正的求問管道(Discussions),good 有了支撐 |
| F-07 | 「11 份寫了求助管道」與本批自己對 size-limit 的判讀矛盾 | ✅ 重數為 **10 份**,三處同步更正 |
| F-08 | rubric 兩處「本輪不修」狀態句已與本版事實相反;三處統計理由段仍在條文內 | ✅ 狀態句更新、統計外移到本報告 |
| F-09 | own-anchor 收自**未遮罩**原文、連結掃遮罩文本——fence 裡示範用的 `<a name=>` 會讓真死鏈靜默變合法 | ✅ 兩邊同吃遮罩文本 + 斷言 + 突變 15 |
| F-10 | `mask_fences` 對**未閉合 fence 不遮罩尾段**(正是本批要修的 amplication 形狀);巢狀 ```` 被 ``` 提早關閉 | ✅ `_fence_regions` 統一配對(CommonMark:同字元且長度≥開頭;未閉合延伸到檔尾)+ 斷言 + 突變 13/14 |
| F-11 | UTF-8 BOM 同時打壞 ATX 第一行與 frontmatter 判定 | ✅ `read_text` 改 `utf-8-sig` + 斷言 + 突變 16 |
| F-12 | `_strip_frontmatter` 對「`---` 開場但不是 frontmatter」整段塗白——與本批要修的根因同型 | ✅ 補 YAML 形狀檢查(每個非空行須是 key:/註解/縮排)+ 斷言 + 突變 17 |
| F-13/F-14 | 兩個「名字宣稱驗 A、實際驗 B / 無鑑別力」夾具(表格列夾具打不到排除分支;連續底線夾具有無重設結果相同) | ✅ 換成有鑑別力的形狀(`\| a \| b \|\n---` 與 `A\n===\n===`)+ 突變 11/12 |
| F-15 | 待處理條數三處不一致(10/12/6→12) | ✅ two-frame 報告可見更正為 12 |
| F-16 | `fence_stats` docstring 宣稱「單獨 fence 不計」而程式照計(既有) | ✅ 與 `mask_fences` 共用 `_fence_regions`,docstring 照實寫 |
| F-17 | H-004 門檻守衛硬編字面 `70%`,沒綁常數(單向失效) | ✅ 綁 `FENCE_LANG_MIN_PCT` |
| F-18 | 重複註解兩行 | ✅ 去重 |

**兩個不修**:`24kchengYe` 的 R-003 佔位(它已確認不影響任何被斷言的數字,
resimulate 內已註明);`read_text` 對 OSError 靜默回空(複審列為觀察,
行為與「找不到 README」合流是既定設計——H-001 的 detail 已能區分路徑存在與否)。

### ⭐ 擴充突變時又抓到一個沒鑑別力的夾具

F-12 的第一版夾具把真標題放在第二條 `---` **之後**——塗白與否結果相同,
突變 17 因此存活。**這是同一天內第三次撞見「夾具打不到它宣稱的分支」**
(F-13、F-14、這裡),形態與 0.1.0 那個 F1 回歸夾具完全相同。
⇒ 夾具的鑑別力要件:**受測內容必須落在會被突變改變的區域裡**。已換夾具,17/17 轉紅。

### 突變紅燈原文(待補證據 1 的補件)

```
🔴 01 slug 退回折疊空白
     ↳ assert github_slug("Art & Design") == "art--design", github_slug("Art & Design")
🔴 02 拿掉 setext 支援
     ↳ assert [(l, t) for l, t, _ in hs] == [(1, "Linux kernel"), (2, "Quick Start")], hs
🔴 03 拿掉 HTML 標題
     ↳ assert extract_headings("<h1 align='center'>Choo</h1>")[0][:2] == (1, "Choo")
🔴 04 拿掉 fence 遮罩(標題)
     ↳ assert not extract_headings("```bash\n# 這是註解不是標題\n```\n"), \
🔴 05 拿掉 frontmatter 剝除
     ↳ assert extract_headings("---\ntitle: x\n---\n# T\n")[0][:2] == (1, "T"), \
🔴 06 拿掉具名錨
     ↳ assert sorted(bad) == ["#ghost_anchor", "#nope", "docs/nope.md"], \
🔴 07 rubric H-002 severity drift
     ↳ assert hyg[hid].get("severity") == hsev, \
🔴 08 rubric R-005 鍵 drift
     ↳ assert craft_ids == set(CRAFT_DIMS), \
🔴 09 evals 案例掉一維
     ↳ ✗ rollup 與 evals 逐案對帳: good-readme: craft_dimensions 必須五維俱全,缺 ['R-005'] 多 ['R-005-gone']
🔴 10 H-002 pass 改回 bare-name 扣分(F-03)
     ↳ assert nh2["pass"] is True, "H1 等於 repo 名不得扣分(Standard Readme Title 規則)"
🔴 11 拿掉表格列排除分支(F-13)
     ↳ assert not extract_headings("| a | b |\n---\n"), "表格列後的裸 --- 不是 setext"
🔴 12 拿掉底線消耗重設(F-14)
     ↳ assert [(l, t) for l, t, _ in dup] == [(1, "A")], dup
🔴 13 未閉合尾塊不遮罩(F-10)
     ↳ assert not extract_headings("```bash\n# 未閉合 fence 的註解也不是標題\n"), \
🔴 14 閉合不查長度(F-10 巢狀)
     ↳ assert not extract_headings("````md\n```\n# 巢狀範例裡的假標題\n```\n````\n"), \
🔴 15 anchor 收自未遮罩原文(F-09)
     ↳ assert sorted(bad) == ["#ghost_anchor", "#nope", "docs/nope.md"], \
🔴 16 BOM 不剝(F-11)
     ↳ assert analyze(os.path.dirname(bp))["h1"] == "BomTitle", \
🟢 未轉紅! 17 frontmatter 不查 YAML 形狀(F-12)

16/17 轉紅
🔴(換夾具後) 17 frontmatter 不查 YAML 形狀(F-12)
     ↳ AssertionError: 以分隔線開場的 README 不是 frontmatter,不得整段塗白(複審 F-12):[]
✅ 17/17 轉紅;復原後綠
```
