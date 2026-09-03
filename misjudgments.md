# 誤判記錄

> **一行一則,不要寫成報告。** 累積 5–10 條再一次處理。
>
> 為什麼是這個形式:姊妹專案 `skill-quality-research` 的 15 節自審 + 兩輪一致性量測的
> **每一個發現**,都來自「拿工具去用真實對象」或「獨立第三方指出來」,**零個來自更多分析**。
> 而那個專案已用數字證明:再多量測也解析不出判準修訂的效果(每維度需 n≈404,母體差 7.6 倍)。
>
> **所以這個檔案是這個專案往後唯一被證明會產出東西的管道。** 保持它輕。

## 格式

```
| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
```

「我認為應該是什麼」寫你的直覺就好,不用先查證 —— **查證是處理時才做的事**,
現在要的是不要讓那個瞬間的違和感消失。

## 處理紀律(累積後才做,不是每次)

1. **先去查,不要憑印象推翻。** 姊妹專案記錄過至少五次「用間接訊號代替直接查證」而判錯,
   其中三次是 **rubric 判對、審查者錯**。
2. **rubric 判對而你不喜歡結果,也是一種結論。**
3. 真的要改條文 → 遞增 `rubric_version`;理由寫在 CHANGELOG 與處理報告,
   **rubric 內只留最小事實陳述**(理由段會污染下一輪判讀)。
4. **分清「待處理」「待測」「已處理」。** 儀器做不到的東西不佔待處理額度 ——
   那不是還沒做,是目前做不了。放「待測」。

---

## 待處理

**目前 0 條。** 批次 #3 的 11 條已於 2026-09-02 處理完畢;fresh 小輪那條 lint fails-open 已於 2026-09-03 即修(儀器 bug 不佔批次額度,verified 即修有先例)。

| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
|------|------|------|----------|------------------|
| 2026-09-02 | 本 repo(fresh 小輪) | `lint_readme.py` 輸入驗證 | 吃 repo_dir,README 不存在時照常輸出 | **靜默 fails-open**:餵檔案路徑(非目錄)→ 不報錯、輸出缺席型 findings(無 H1/無安裝段),五份輸出完全相同才被識破;單份語料時空讀會被當真。**已修(2026-09-03)**:非目錄 rc=2 硬失敗;真目錄無 README 明示「缺席型」警告;selftest 三負向 case(檔案路徑/不存在路徑/空目錄)。詳 `reviews/2026-09-02-fresh-wave-mini.md` |
(**11 修 0 不修**),見 [`reviews/2026-09-02-misjudgment-batch-3.md`](reviews/2026-09-02-misjudgment-batch-3.md)。
⇒ rubric **0.4.0** / 工具 **0.4.0**。批次 #1/#2 見已處理表。

| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
|------|------|------|----------|------------------|
|（空）| | | | |

## 待測(儀器目前做不到,**不佔處理額度**)

| 日期 | 對象 | 規則 | 卡在哪 | 解除條件 |
|------|------|------|--------|---------|
| 2026-09-01 | 本 repo | `craft_verdict_rollup` 的 `≥2 mixed` 門檻 | **這個數字是借來的。** 它來自姊妹專案對 54 份質化筆記的觸發率模擬(1.9–3.7% → 20.4% → 5.6–11.1%),**本專案沒有自己的模擬語料**。 | **需要一批真實 README 的 craft 判讀結果**才能算觸發率。Phase 6 的實測就是第一批;**若第一批全 approved,先懷疑門檻而不是慶祝**(姊妹專案 41/41 的教訓)。 |
| 2026-09-01 | 本 repo | `triangulation_sources` | 五個來源是**憑既有知識引用的,本輪未逐條開啟原文核對** | 逐條開啟原文、記錄查證日期與引用位置。在那之前,任何「規範 X 說 Y」的引用只有**中等**證據強度 —— rubric 內已如此標記。⚠️ **2026-09-02 部分解除**:GitHub Docs / Standard Readme `spec.md` / `matiassingers/awesome-readme`(新增來源)三個已逐條查證並落檔,含逐字引用與**對本 rubric 的三處反證**。**2026-09-02 稍後全數解除**:Make a README(R-005 的第三個獨立來源 + Project status 佐證 R-004)與 Diátaxis(四象限成立;⚠️ 無 README 專屬指引,適用為間接推衍)皆已逐字查證 —— 六來源查證完畢。⚠️ **查證來源不等於驗證權重**:證據性質段的「權重是選的、不是量出來的」**原封不動** |

## 已處理

(處理後從上表移到這裡,附處置與 commit)

| 日期 | 對象 | 規則 | 處置 |
|------|------|------|------|
| 2026-09-02 | **批次 #3(11 條:實驗室縫 8 + 真實使用 3)** | 見 [`reviews/2026-09-02-misjudgment-batch-3.md`](reviews/2026-09-02-misjudgment-batch-3.md) | **11 修 0 不修**,rubric 0.3.0→0.4.0、工具 0.3.0→0.4.0。code:emoji slug 不再 strip(23→0)、S-001 補行程替換與 irm\|iex 兩形(AI-SOP 0→7)、static 假 badge 出 scope。criteria:文件前門型列+artifact 限縮、載重統計三裁定、宣稱即陳述合體裁定、badge 出 scope、應用/索引 delegation、旗艦範例缺件不豁免(裁定推翻多數實踐,依機制)、R-003 連言與清單門檻、R-005 雙向管道+href 匿名。3 突變轉紅;縫 3/4/5 單一出口推導有污染,驗證等真實使用 |
| 2026-09-02 | **批次 #2(10 條:盲判收斂 9 + verbatim 補登 1「主體指認邊界」A#7/B#6)** | 見 [`reviews/2026-09-02-misjudgment-batch-2.md`](reviews/2026-09-02-misjudgment-batch-2.md) | **9 修 / 1 刻意不修**,rubric 0.2.0→0.3.0、工具 0.2.0→0.3.0(純條文,零程式行為變更)。修:R-004 `scope_of_perishable`(載重宣稱;範例 pin/修辭形容/外部連結本體不算)+ `statement_test`(排除力判別法;清單型認收錄立場)+ 序 1 空缺連言明定 + 序號必記;R-005 anti-pattern 專屬格位(序 2 → mixed)+ 世界知識具名規則 + 主體指認三形式;craft_value_mapping 瑕疵位置;R-002 `delegation_stance`(CLI 外鏈不豁免/library 豁免安裝/hosted 擇一);形狀表 + hosted 服務門面列 + 「形狀由 artifact 決定」;R-001 渲染近似規則。刻意不修:**R-004 序 3 封頂 mixed**(B#3 反直覺成立,但機械同步只解決鮮度、不回答「何時不該用」——rationale 已寫進條文一行)。rollup 門檻不動 |
| 2026-09-02 | **批次 #1(12 條)** | 見 [`reviews/2026-09-02-misjudgment-batch-1.md`](reviews/2026-09-02-misjudgment-batch-1.md) | **8 修 / 2 刻意不修 / 2 記分歧**,rubric 0.1.0→0.2.0、工具 0.1.0→0.2.0。修:H-002 撤 bare-name 扣分降 info;R-004 三出口→五出口(+機械同步 equivalent_forms);craft_value_mapping;形狀表+索引/導覽型;HEADING_RE 三語法+fence 遮罩;slug 逐空白;HTML 具名錨;H-005 前提文件化+稀疏 root 警示;**R-005 新增**(缺席不設 poor;內部工具 n/a)。刻意不修:H-004(抽查 6/6 輸出型,info 級);rollup `≥2 mixed` 門檻(重模擬無調整依據)。分歧:本 repo README 的 blockquote 定位句與 Standard Readme 相左,已於 README 註明。18 份重模擬:needs-revision 11→10、R-004 poor 10→7,數字由 `scripts/resimulate_18.py` 斷言並掛 CI。9/9 突變轉紅 |
| 2026-09-02 | 本 repo(流程) | commit 訊息宣稱了沒發生的事 | **已公開更正。** `08e9e01` 的訊息寫「README 的信任度表與 CHANGELOG 同步更新」,而 **README 一個字都沒動** —— 批次改檔的腳本在 README 那一段 `assert` 失敗、整段中止,但我**沒有檢查 `git show --stat` 就 commit 並 push**。成因是 anchor 用半形逗號而檔案是全形。⚠️ **這是本 repo 到目前為止最嚴重的一次**:前面幾條是程式與註解不符,這一條是**commit 訊息與 diff 不符,而且已經推出去了**。⇒ 教訓:**批次改多檔的腳本失敗時會靜默留下半套**,commit 前一律看 `--stat` 對照訊息宣稱的檔案清單 |
| 2026-09-02 | 本 repo(可攜性) | `subprocess text=True` 吃 locale 編碼 | **已修,這是第三次紅燈、同一根因的第三種面貌。** 前兩次修的是**寫者側**(stdout encode);這次是**讀者側** —— `subprocess.run(text=True)` 在 Windows 用 cp1252 解子行程的 UTF-8 stdout → `UnicodeDecodeError` → `r.stdout` 變 None → `json.loads(None)` TypeError。⇒ 不再逐個修,改為**列出整個編碼邊界**(encode / decode / open)並加守衛。⚠️ 守衛自己連踩三個自我指涉:偵測器字面命中自己、逐行標記漏了訊息字串、**連 sentinel 的偵測行都含 sentinel**。**靜態掃自己是條爛路** ⇒ 改為不掃自己那一支,因為它有更強的驗證(CI 在 `PYTHONUTF8=0` 下直接執行它)。五種突變全數轉紅 |
| 2026-09-02 | 本 repo(可攜性) | reconfigure 只補了報紅的那一支 | **已修,但這是第二次紅燈。** 第一次修完 CI 再紅一次,失敗步驟換成 `Eval regression` —— `run_evals.py` 同樣印中文、同樣沒有 reconfigure,而我**只修了報紅的那一支、也只重現了那一支**。⇒ 改為對全 repo 的 Python 進入點做系統性檢查,並加一條 selftest 守衛。⚠️ 守衛第一版寫 `"reconfigure" not in _src` —— **註解裡就有那個字**,於是它被自己的說明文字餵飽、突變不轉紅。已改為比對**呼叫**且要求帶 `encoding=` 參數。三種突變(換 pass / 刪整段 / 沒 encoding)全數轉紅。⚠️ **教訓:修的是那一支,還是那一類?** 以及**守衛不要用字面字串比對它自己會提到的詞** |
| 2026-09-02 | 本 repo(CI 註解) | `windows` job 的「驗證 reconfigure」 | **已修。註解宣稱了程式沒有的行為。** CI 步驟從姊妹專案抄來、寫著「刻意用 `PYTHONUTF8=0` 驗證 lint 自己 reconfigure 得起來」,而 `lint_readme.py` **根本沒有 reconfigure** —— 首次 CI 的 windows job 直接 `UnicodeEncodeError`。⇒ 補上 stdout/stderr 的 `reconfigure`;本機用 `PYTHONIOENCODING=cp1252` 重現,修前 rc=1 修後 rc=0。⚠️ **教訓:抄 CI 步驟時要一起抄它所驗證的實作** —— 否則那個步驟驗的是一句空話 |
| 2026-09-01 | 本 repo(selftest) | `OBEY_KNOWN_UNCOVERED` / `SECRET_KNOWN_UNCOVERED` | **已修。突變測試抓到兩條恆真斷言。** 兩組夾具都**不含觸發語** —— `not obey_remote_hits(u)` 與 `not secret_hits(u)` 因此永遠成立,拿掉否定詞消音/佔位符過濾都不會轉紅。已改為「必須同時含觸發語與否定詞」「必須讓 `REAL_SECRET` 真的命中」,並加**前置斷言**強制夾具自證有行使該路徑 |
| 2026-09-01 | 本 repo(selftest) | F1 回歸夾具(註解遮蔽) | **已修。夾具沒有鑑別力。** 本解析器逐行 `finditer`、**後者覆蓋前者**,而第一版把註解放在真值**之前** → 真值蓋掉註解,斷言恆真。已改為註解在**後**。重測確認:只拿掉剝註解 🟢、只放寬行首錨 🟢、**兩層同時拿掉才 🔴** —— 兩層防護各自獨立有效 |
