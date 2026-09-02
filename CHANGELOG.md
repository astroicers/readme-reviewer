# CHANGELOG

版本語意:`plugin.json` / `marketplace.json` 追的是**工具**版本;
`rubric_version`(見 `references/rubric.yaml` 檔頭)追的是**判準**版本。兩者刻意分開。

---

## [Unreleased]

### triangulation 來源查證完成(零判準變更)

- **Make a README ✅**(2026-09-02 逐字查證):其 **Support / Authors / Project status**
  段構成 **R-005 的第三個獨立來源**;"Project status 放頂部" 獨立佐證 R-004 的
  維護狀態條款。查到的是**支持證據**——與首輪三條反證一樣如實記。
- **Diátaxis ✅**(2026-09-02 逐字查證):四象限與「越界是文件問題核心」成立;
  ⚠️ **該框架無 README 專屬指引**,對本 rubric 的適用是間接推衍,引用強度按此折扣。
- ⇒ 六個 triangulation 來源**全數查證完畢**(姊妹專案筆記按同作者非獨立折扣)。
  `rubric_version` 不動——改的是查證狀態,不是判準。

### ⭐ 第一批盲判資料:3 位不知情判讀者 × 12 份 README(rubric 0.2.0)

全文:`reviews/2026-09-02-blind-rejudge-020.md`;統計由 `scripts/blind_agreement.py`
重算並斷言(掛 CI);判讀值與 friction 逐字紀錄在 `reviews/blind-2026-09-02/`
(⚠️ 該目錄列入未來判讀者禁讀清單)。

- **判準骨架站得住**:兩兩整體 86.1%、R-001 100%、形狀 11/12、
  verdict 分佈四方同為 7 needs-revision
- **R-004 兩面失穩且作者是離群值**:兩兩 69.4%(最低)、vs 作者 47.2%;
  作者 poor 5/12 vs 判讀者 2/36 票——重模擬的 R-004 值系統性偏嚴,
  成因是**舊值錨定移植**(方法論教訓:重模擬要素讀,不可由舊值起手)
- **R-005(上一批新增)第二穩**(94.4%),保守設計未亂射;
  但其 anti-pattern 與 decision_order 的脫鉤被**雙向證實**(public-apis 3:1)
- **friction 三方收斂 6 條**——三個互不知情的 context 摸到同一批條文縫
  (量詞、易腐定義、陳述門檻、anti-pattern 落點、世界知識、瑕疵位置)
  ⇒ 9 條新誤判入帳,**批次 #2 蓄積中,本輪不修**
- 0.2.0 的兩個改動拿到盲判佐證:索引/導覽型列讓 linux 的 R-002 由「查不了」
  變三方一致 good;`choo`/`torvalds` 兩份 20 格近乎逐格全同

---

## [0.2.0] — 2026-09-02(rubric 0.2.0 / 工具 0.2.0)

**第一次誤判批次處理:12 條待處理 → 0。** 8 修 / 2 查證後刻意不修 / 2 記分歧或使用陷阱。
逐條裁決與重模擬全文:`reviews/2026-09-02-misjudgment-batch-1.md`。

### 判準(rubric 0.1.0 → 0.2.0)

- **R-004 `decision_order` 三出口 → 五出口**:舊結構下「無易腐內容」對真實 README
  幾乎不可能成立,實際只剩 good/poor 兩個出口(18 份實測 mixed 僅 1 次)。
  新結構讓 mixed 從兩側可達;**機械同步形式**(指向單一事實源 / repo 內相對路徑 /
  同步標記+CI)收進 `equivalent_forms`,**外部文件網站明文排除**
- **新增 R-005 求助與維護**:GitHub Docs 五項的第 4、5 項 + Standard Readme 兩條款
  獨立佐證(皆逐字查證;實測 12 份有 10 份寫了求問管道——第一版誤記 11,
  複審 F-07 更正)。**缺席不設 poor**(GitHub 預設有 Issues;poor 只給
  「寫了但已失效/誤導」);「不提供支援」是合格答案;內部工具 n/a。
  rollup 門檻維持**絕對值 2**,刻意不隨分母 4→5 調整
- **H-002 撤銷「H1 等於 repo 名」扣分,severity 降 info**:與自己引用的
  Standard Readme Title 規則直接矛盾。(⚠️ 本段第一版還引了一條「與 R-001 poor
  零重疊」的統計——獨立複審重算後**交集是 1、且該統計屬於另一支**,已撤下;
  更正全文見批次報告 §1)
- **新增 `craft_value_mapping`**:good/mixed/poor 的取值映射從「判讀者自選」變成條文
  (首批判讀實測到的信度殺手)
- **形狀表新增「索引/導覽型」**:R-003 判分類與導覽結構品質,**不歸零**
- H-004 查證後**刻意不修**(抽查 6/6 未標註 fence 是目錄樹/對話樣張/ASCII 圖,
  本就無語言可標;info 級不進 verdict),補 known_false_positives

### 工具(0.1.0 → 0.2.0)

- **標題抽取支援 ATX + setext + HTML 三語法,並先遮罩 fence 與 frontmatter**——
  修掉「一個根因、三個面向」:torvalds/linux(ATX 0/setext 15)曾讓 H-002/H-003/
  own-anchor 同時出錯;amplication 的 bash 註解曾被當 H1(**它以前因錯誤的理由通過
  H-002,修後如實轉未過**,logo 型交 LLM 複核)
- **`github_slug()` 空白逐個換 `-`**(GitHub 不折疊連續空白):`Art & Design` →
  `art--design`。12 個真實 anchor 誤報全數解析;slug 前先取渲染文字
  (連結取 text、圖片取 alt、剝 tag)
- **`broken_links` 認 `<a name=>` / `id=` 具名錨**;fence 內連結不再誤掃
- **H-005 稀疏 root 警示**:root 無子目錄且檔案極少時,note 明說「相對路徑死鏈
  可能是單檔抽樣的假陽性」(2026-09-02 實測:16 個命中全部無效的教訓)
- `HYGIENE_SEVERITY` 提到模組層,drift-guard 逐條與 rubric 對帳(craft 維度鍵也對)
- evals:五案例補 R-005;**案例宣告 dims 必須五維俱全**(否則新維度從 evals
  消失不會轉紅);兩個 fixture 補求助/維護段以行使 good 路徑
- 新增 `scripts/resimulate_18.py`:18 份重模擬的分佈數字由它重算並斷言,掛 CI

### 驗證

- **9 個突變逐個打,9/9 轉紅,復原後全綠**(slug 折疊、setext、HTML 標題、fence 遮罩、
  frontmatter、具名錨、H-002 severity drift、R-005 鍵 drift、evals 缺維)。
  ⚠️ 自跑突變只涵蓋自己想得到的形狀
- 18 份重模擬:needs-revision 11→10(唯一翻正:torvalds/linux,repo 內相對路徑
  是機械同步);R-005 造成兩個 approved → approved-with-notes(claude-code-warp、
  ai/size-limit——兩份都無可指認的求助管道)。**重模擬不是校準,判讀者同一人**

---

### 同日稍早的判讀語料與來源查證(本版的觸發來源,PR #1)

#### 雙抽樣框 12 份真實 README

首批 6 份**全是 skill/plugin 相關,形狀偏斜**。本輪按兩個獨立抽樣框各抽 6 份非 Claude 生態的
README,用**同一套 rubric 0.1.0** 判。全文:`reviews/2026-09-02-two-frame-comparison.md`。

- **A 框**(`matiassingers/awesome-readme` 人工策展):approved 1 / with-notes 2 / needs-revision 3
- **B 框**(GitHub 星數排序):approved 0 / with-notes 1 / needs-revision 5
- ⚠️ **兩框差異更可能是形狀的、不是品質的** —— B 框 3 份清單型、A 框 0 份;n=6 vs 6;
  判讀者仍是我。**三個限制寫在結論之前。**

**撈到的東西**(全部入 `misjudgments.md`,待處理 6→12,**達批次門檻上緣**):

- ⭐ **R-004 事實上是個二元開關。** `decision_order` 順序 2 對真實 README 幾乎不可能成立,
  於是只剩 1 與 3;實測 R-004 的 12 個標記是 **good 4 / mixed 1 / poor 7**。
  **兩批合計 12 個 poor,10 個出自 R-004**,而它是唯一能單獨翻 verdict 的維度。
- ⭐ **三個程式缺陷,全部有實測與 ground truth**:
  (a) `HEADING_RE` 只認 ATX —— **setext 與 HTML `<h1>` 全盲**,`torvalds/linux`
      (ATX 0、setext 15)因此讓 H-002 / H-003 / own-anchor 集合**同時**出錯,一個根因三個面向;
  (b) `github_slug()` 把連續空白折成單一 `-`,GitHub 是逐個換 —— `Art & Design` 應為
      `art--design`,本批 12 個 anchor 死鏈**全部**是這個形狀;
  (c) `broken_links` 不認 HTML 具名錨。⇒ **H-005 本批 8 次開火,0 個確認的真陽性。**
- **R-001 首次產生 poor**,機制可指認:第一屏被贊助商/自家產品廣告佔滿
  (`public-apis` 的 H1 是贊助商產品標題;`sindresorhus/awesome` 前 78 行是作者自家 app 廣告)。
  **判準不是只有 R-004 會說「不」。**
- **抽樣陷阱**:只下載 README、未 clone repo ⇒ H-005 的相對路徑那一半(16 個命中)**全部無效**,
  且讓 `linux` 的 R-002 判不了。**一個捷徑,兩處後果。**

#### `triangulation_sources` 三個來源逐條查證(該步零判準變更)

該步 `rubric_version` 維持 0.1.0(改的是來源查證狀態;**同日稍後的批次處理才升 0.2.0**)。

| 來源 | 狀態 | 查到的**反證** |
|---|---|---|
| GitHub Docs — About READMEs | ✅ | 五項內容中「去哪求助」「誰維護」**本 rubric 零維度承載** |
| Standard Readme `spec.md` | ✅ | Title 規則**與 H-002 直接矛盾**;本 repo README 違反其 Short Description 三條 |
| `matiassingers/awesome-readme` | ✅ **新增** | 六條收錄理由**零次**提及 R-004 或前置條件 |
| Make a README / Diátaxis | ⏳ 未查 | — |

⚠️ **查證來源不等於驗證權重。** 三份逐字引用改變的是「我們說某來源講了什麼」的可信度,
**不改變**「權重是選的、不是量出來的」——證據性質段一字未動。


---

## [0.1.0] — 2026-09-01

首個版本。比照姊妹專案 `skill-quality-research` 的 `skill-reviewer` 架構,
但**證據性質不同**:那邊的 packaging 權重來自 97-repo 星數梯度,
**本專案沒有那個東西**,來源是 triangulation。條文與 README 都如此標明。

### 判準(rubric 0.1.0)

- **craft_llm 四維(主判)**:R-001 第一屏 / R-002 最短可執行路徑 /
  R-003 寫作品質 / R-004 限制誠實
- **hygiene 五條**:H-001 存在性(唯一 error 級)、H-002 標題、H-003 安裝或使用段、
  H-004 code fence 標語言(門檻 70%,**是選的**)、H-005 相對連結與 anchor 不死
- **security 三條**:`curl|sh`(medium)、真實憑證(error/低信心)、服從遠端輸出(低信心)
- **形狀表七種**:library / CLI / 應用 / 研究 / awesome / monorepo / 模板

### 第一天就有的守衛(從姊妹專案的實測缺陷直接繼承)

- **`mixed` 從第一天就計費**。那邊的 craft verdict 原本只有 `poor` 觸發,實測結果是
  **連續 41 個對象 41/41 全 approved** —— 一個從來不說「不」的判準跟橡皮圖章無法區分。
  ⚠️ 但 `≥2` 這個門檻**是借來的**,本專案尚無自己的觸發率實測(已記入 misjudgments 的「待測」)
- **取值域用集合相等**,不是逐個 `in`(`'approved' in 'approved-with-notes'` 恆真)
- **drift-guard 三層**:剝整行註解 + 以 `- id:` 切塊 + 欄位錨行首。
  缺任一層,談論舊值的註解就可能被讀成值
- **預期行為住在案例檔**:`expect_block` / `expect_block_reason` / `hygiene_pass` /
  `security[].review` 全部必填,程式端**無預設值**
- **所有 fixture 進版控**,不依賴外部 clone —— 只跑在未進版控語料上的斷言在 CI 會 skip

### 突變驗證抓到的三個自身缺陷(當天修掉)

1. **兩條恆真斷言** —— `OBEY_KNOWN_UNCOVERED` / `SECRET_KNOWN_UNCOVERED` 的夾具
   **不含觸發語**,`not ...hits(u)` 永遠成立;拿掉否定詞消音或佔位符過濾都不會轉紅。
   已改為夾具必須自證行使該路徑(加前置斷言)。
2. **回歸夾具沒有鑑別力** —— F1(註解遮蔽)的夾具把註解放在真值**之前**,
   而本解析器逐行 finditer、後者覆蓋前者 → 真值蓋掉註解,斷言恆真。已改為註解在**後**。
   重測:只拿掉剝註解 🟢、只放寬行首錨 🟢、**兩層同時拿掉才 🔴**(兩層各自獨立有效)。
3. **契約覆蓋缺口** —— `c_fixture_behaviour` 原本只驗 `blocks` 與 `H-001`,
   於是把 fixture 的安裝段標題改壞**不會轉紅**(H-003 是 warning)。
   已補 `hygiene_pass` 逐條釘住。

### 首次 CI 紅燈:我自己的註解在說謊

`windows` job 的步驟註解寫著「刻意用 `PYTHONUTF8=0` 驗證 lint 自己 reconfigure 得起來」,
而 **`lint_readme.py` 裡根本沒有 reconfigure** —— CI 步驟是從姊妹專案抄來的,
對應的實作沒跟著抄。結果:首次 CI `windows` job 直接 `UnicodeEncodeError`(cp1252)。

**註解宣稱了一個程式沒有的行為**,正是本工具自己在抓的形態,而它出現在 day 0 的自己身上。

⇒ 已補上 stdout/stderr 的 `reconfigure(encoding="utf-8")`。
本機用 `PYTHONIOENCODING=cp1252` 重現:**修前 rc=1、修後 rc=0**。

### ⚠️ 更正:`08e9e01` 的 commit 訊息宣稱了沒發生的事

該 commit 的訊息寫「README 的信任度表與 CHANGELOG 同步更新」,
而 **README 一個字都沒動**(`git show --stat` 只有 CHANGELOG / misjudgments / reviews 三檔)。

成因:批次改檔的腳本在 README 那一段 `assert` 失敗、整段中止(anchor 用半形逗號,
檔案是全形),而**我沒有檢查 `--stat` 就 commit 並 push**。

**這是本 repo 到目前為止最嚴重的一次。** 前面幾條是程式與註解不符;
這一條是 **commit 訊息與 diff 不符,而且已經推出去了**。
commit 訊息改不了,以本節與 `misjudgments.md` 為準。README 已於下一個 commit 補上。

⇒ 教訓:**批次改多檔的腳本失敗時會靜默留下半套** ——
commit 前一律看 `git show --stat` 對照訊息宣稱的檔案清單。

### 首批 craft 判讀(2026-09-02):判準會說「不」,但成因集中

**主判的第一次實測。** 6 份真實 README,23 個已判維度標記:good 15 / mixed 5 / poor 3。
verdict:**approved 2 / approved-with-notes 1 / needs-revision 3(50%)**。

⇒ **姊妹專案 41/41 那個失敗模式沒有重演。** `mixed` 從第一天計費的設計在第一批就產生輸出。

⚠️ **但 3 個 `poor` 全部出自 R-004,沒有一個來自其他三維** ——
而條文裡本來就寫著「本條若過度觸發,先懷疑它,不要先調 rollup 門檻」。**第一批就撞上了。**

⚠️ **判讀者是我,而我寫了 rubric**,且我知道 41/41 的教訓 —— **有動機讓它開火**。
全文與污染聲明見 `reviews/2026-09-02-first-craft-batch.md`。
**本批只證明了這條路徑會輸出 needs-revision,沒有證明它判得準。**

判讀過程撞到三個條文缺口,全部入 misjudgments(現 5 條,已達批次下緣):
`pass_criteria` 沒映射到取值域、形狀表缺「索引/導覽型」、
R-004 的 `decision_order` 看不到「機械同步」這種驗證形式。

### 第三次 CI 紅燈:寫者側修好不等於讀者側也好了

`UnicodeDecodeError`(decode,不是 encode)。`subprocess.run(text=True)` 在 Windows
用 **locale 編碼**解子行程的 stdout,而子行程寫的是 UTF-8 → `r.stdout` 變 None →
`json.loads(None)` 拋 TypeError。

**同一根因(Windows locale 編碼)的第三種面貌**:encode(stdout)、decode(subprocess)、open()。

⇒ 停止逐個修。列出**整個編碼邊界**,守衛一次涵蓋三類。

⚠️ **守衛自己連踩三個自我指涉**:偵測器的字面字串命中自己 → 加逐行標記卻漏了訊息字串 →
改用起訖 sentinel,而**連 sentinel 的偵測行都含 sentinel 字串**。
**靜態掃自己是條爛路。** ⇒ 最終設計:守衛**不掃自己那一支**,
因為那一支有更強的驗證 —— CI 的 windows job 在 `PYTHONUTF8=0` 下**直接執行**它。
**行為驗證比 grep 自己的原始碼可靠。**

負向驗證:五種突變(subprocess 拿掉 encoding / reconfigure 換 pass / 改 `errors=` /
open 拿掉 encoding / 整段刪掉)**全數轉紅**。

### 第二次 CI 紅燈:修的是那一支,不是那一類

補完 `lint_readme.py` 的 reconfigure 後 CI 再紅一次,失敗步驟換成 `Eval regression`
—— `run_evals.py` 同樣印中文、同樣沒有 reconfigure。**我只修了報紅的那一支,
本機也只重現了那一支**,所以看不到。

⇒ 改為系統性檢查:selftest 新增一條守衛,掃全 repo 的 Python 進入點,
凡「會印非 ASCII 且是進入點」就必須有 `reconfigure(encoding=...)`。

⚠️ **守衛第一版自己也有同型缺陷**:它寫 `"reconfigure" not in _src`,
而**註解裡就有那個字** —— 它被自己的說明文字餵飽,突變不轉紅。
已改為比對**呼叫**並要求帶 `encoding=` 參數。
三種突變(換 `pass` / 刪整段 / 改成 `errors=`)全數轉紅。

### 首次自審撈到的(已入 misjudgments)

用它審自己的 README:H-004(fence 未標語言)與 H-005(死連結)是**真缺口,已修**;
**H-002 判 warning 很可能是條文太嚴** —— `H1 = 專案名` 是 GitHub 近乎普遍的慣例,
定位句放下一行才是常態。⚠️ n=1,**先不動條文**,記錄待批次處理。
