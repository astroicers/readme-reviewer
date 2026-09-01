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

### 首次自審撈到的(已入 misjudgments)

用它審自己的 README:H-004(fence 未標語言)與 H-005(死連結)是**真缺口,已修**;
**H-002 判 warning 很可能是條文太嚴** —— `H1 = 專案名` 是 GitHub 近乎普遍的慣例,
定位句放下一行才是常態。⚠️ n=1,**先不動條文**,記錄待批次處理。
