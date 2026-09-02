# CHANGELOG

版本語意:`plugin.json` / `marketplace.json` 追的是**工具**版本;
`rubric_version`(見 `references/rubric.yaml` 檔頭)追的是**判準**版本。兩者刻意分開。

---

## [Unreleased]

(空)

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
