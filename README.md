# readme-reviewer

> **這是一個審查 GitHub README「寫得好不好」的工具。**
> LLM 讀 README 判**第一屏定位 / 最短可執行路徑 / 寫作品質 / 限制誠實 / 求助與維護**
> ——**那是主判**；lint 只負責 hygiene 門檻與安全紅旗，**它的輸出不是品質結論**
> （[判準與信任邊界](#哪一段能信到什麼程度)）。
>
> **這份判準的權重是「選的」，不是「量出來的」。** 來源是 triangulation
> （公開規範 + 質化樣態），**不是**星數梯度——[為什麼這樣還值得做](#證據性質必讀)。

## 安裝

**Claude Code plugin（推薦，一行）**

```text
/plugin marketplace add astroicers/readme-reviewer
/plugin install readme-reviewer@readme-reviewer
```

⚠️ **這兩行的證據強度**：格式與命名慣例照 `installed_plugins.json` 的真實 key
（`<plugin>@<marketplace>`）與 8 個運作中的 marketplace 對過，
**但沒有在乾淨環境端到端跑過**。裝不起來請開 issue——我們不替沒跑過的事背書。

**或裝成 skill**（symlink，repo 更新自動生效）：

```bash
git clone https://github.com/astroicers/readme-reviewer.git
cd readme-reviewer && ./install.sh --symlink
```

<details>
<summary><b>其他 harness</b> —— 只寫實測過的</summary>

**實測過的只有 Claude Code。** 其他 harness **不宣稱整合**。

可陳述的事實：`readme-reviewer/scripts/lint_readme.py` 是**零依賴 Python CLI**（3.9+），
任何能跑 shell 的 agent 都能呼叫；`SKILL.md` 是純 markdown，無 Claude 專屬語法。
要不要接、接得順不順，**請你自己驗**。
</details>

## 30 秒上手

**主判 —— craft 判讀**（在 Claude Code 對話中）：

```text
用 readme-reviewer 審查 <repo 路徑或 URL>
```

**過濾器 —— deterministic lint**（可單獨跑，但它**不是評價**）：

```bash
python3 readme-reviewer/scripts/lint_readme.py <repo 目錄> --json
```

⚠️ 只跑第二個，你會拿到一份 hygiene 與安全結果，而 `craft_verdict` 會是 **`null`**——
**那個留白是設計出來的**，提醒你只做了一半。

輸出三段式：**craft verdict** / **形狀與缺口** / **分維度 findings**。
`craft verdict` 取三個值：**`approved` / `approved-with-notes` / `needs-revision`**
（六條依序判的規則見 [`rubric.yaml`](readme-reviewer/references/rubric.yaml) 的
`craft_verdict_rollup`——**canonical 只有那一份**）。

## 判準：五個維度

| id | 維度 | 判什麼 |
|---|---|---|
| **R-001** | 第一屏 | 遮住第 15 行之後，讀者知不知道「這是什麼、我是不是目標讀者」 |
| **R-002** | 最短可執行路徑 | 指令可貼嗎？**前置條件說了嗎**？成功長什麼樣？ |
| **R-003** | 寫作品質 | 關鍵選擇附理由嗎？有具體例子/輸出樣張，還是只有形容詞？ |
| **R-004** | 限制誠實 | 說了什麼時候**不該**用嗎？易腐內容有時效標記**或機械同步**嗎？ |
| **R-005** | 求助與維護 | 卡住了知道去哪求助嗎？知道由誰維護嗎？（**缺席最多 mixed**，poor 只給「寫了但已失效」） |

**形狀先於準則。** library / CLI / 應用 / 研究 / awesome 清單 / monorepo / 模板
各有不同的例外條款——把一種形狀的標準套到另一種，是最常見的誤判來源
（姊妹專案在 22 個樣本中出現 6 次）。形狀表見 [`SKILL.md`](readme-reviewer/SKILL.md) 步驟 3。

## 證據性質（必讀）

**這份 rubric 沒有星數梯度背書。**

姊妹專案 [`skill-quality-research`](https://github.com/astroicers/skill-quality-research)
的 packaging 權重來自 97 個 repo 的星數梯度，有 bootstrap CI 可查。**本專案沒有那個東西。**

來源是 **triangulation**：公開規範 + 該專案 54 份質化筆記收斂的寫作工藝樣態。
**2026-09-02 起三個來源已逐條開啟原文核對並附逐字引用**
（GitHub Docs ✅ / Standard Readme `spec.md` ✅ / `matiassingers/awesome-readme` ✅）；
**Make a README 與 Diátaxis 仍未查**，引用它們時只有中等證據強度
（[查證狀態逐條寫在條文裡](readme-reviewer/references/rubric.yaml)）。

⚠️ **查證來源不等於驗證權重。** 那三份查證改變的是「我們說某來源講了什麼」的可信度，
**不改變**上面那句「權重是選的、不是量出來的」。而且查到的三件事**都是反證**：
規範要求的兩個內容面本 rubric 零維度承載、Standard Readme 的 Title 規則與 H-002 直接矛盾、
人工策展的收錄理由零次提及 R-004。

**那為什麼還值得做？** 因為那個專案跑完六個 phase 的結論是
**「星數關聯的是打包面，不是內容工藝——craft 才是主判」**。
craft-first + triangulation 是**遵循那個結論**，不是繞過它。

- **可以說**「這條規則的依據是 X」
- **不可以說**「資料顯示這樣寫會更受歡迎」——我們沒有那個資料

<sub>⚠️ 引用規範不等於全盤採納：本 README 的定位句放在 blockquote 裡，
違反 Standard Readme「Short Description **must not start with `> `**」等三條規則。
**那是刻意的分歧**（GitHub Docs 無此規定），既然引用了該 spec 當來源，分歧就寫在這裡。</sub>

## 哪一段能信到什麼程度

| 輸出 | 信任度 | 為什麼 |
|---|---|---|
| hygiene（H-001 存在性） | **可當硬門檻** | 確定性判定，無爭議 |
| hygiene（H-002~005） | **當提示** | 有已知假陽性：logo 圖片取代 H1、awesome 清單無安裝段；H-002 只報結構事實（0.2.0 起） |
| security 紅旗 | **必須人工複核** | `confidence` 標低者假陽性高；S-003 有具名的極性反轉前科 |
| **craft verdict** | **信「有沒有問題」，不信刻度** | 主判。兩批 18 份真實 README 實測 **11/18 needs-revision**——它會說「不」；但**成因高度集中於 R-004**，見下 |

> ⚠️ **`≥2 mixed → needs-revision` 這個門檻是借來的。**
>
> 它繼承自姊妹專案的一個實測缺陷：那邊的 craft verdict 原本只有 `poor` 觸發，
> 而 `poor` 罕見——結果是**連續 41 個對象 41/41 全 `approved`**，
> 史上零次由 craft 說「不」。**一個從來不說「不」的判準，跟橡皮圖章無法區分。**
>
> **2026-09-02 兩批共 18 份真實 README 實測（rubric 0.1.0）：11/18 needs-revision
> ——那個失敗模式沒有重演。**
>
> ⚠️ **但當時 12 個 `poor` 裡有 10 個出自 R-004** ——條文裡本來就寫著
> 「本條若過度觸發，先懷疑它」，實測確認它的 `decision_order` 事實上只有兩個出口。
> **已於同日的誤判批次處理改寫**（rubric 0.2.0：`mixed` 從兩側可達、
> 機械同步計為驗證形式），18 份重模擬後 R-004 三個實值出口都有人住、
> needs-revision 11→10。數字由 [`scripts/resimulate_18.py`](scripts/resimulate_18.py)
> 重算並斷言（掛 CI），全文見
> [`reviews/2026-09-02-misjudgment-batch-1.md`](reviews/2026-09-02-misjudgment-batch-1.md)。
>
> ⚠️ **兩批的判讀者都是我，而我寫了這份 rubric**——我知道 41/41 的教訓，**有動機讓它開火**；
> 重模擬也是同一人判的，**不是校準**。全文與污染聲明見
> [`reviews/2026-09-02-first-craft-batch.md`](reviews/2026-09-02-first-craft-batch.md)（6 份）與
> [`reviews/2026-09-02-two-frame-comparison.md`](reviews/2026-09-02-two-frame-comparison.md)（12 份，兩個抽樣框）。
> **它只證明了這條路徑會輸出 needs-revision，沒有證明它判得準。**

## 判錯了怎麼辦

在 [`misjudgments.md`](misjudgments.md) 加一行，累積 5–10 條再一次批次處理。
**先去查，不要憑印象推翻**——「rubric 判對而你不喜歡結果，也是一種結論」。

## 開發

```bash
python3 readme-reviewer/scripts/lint_readme.py --selftest   # 純函式 + drift-guard
python3 readme-reviewer/evals/run_evals.py --ci             # 行為契約(committed fixtures)
```

`--selftest` 含 **drift-guard**：硬編的 severity/confidence 與
`references/rubric.yaml` 不一致即 fail。解析 rubric 時先剝整行註解、以 `- id:` 切塊、
欄位錨行首——**三層缺一，談論舊值的註解就會被讀成值**。

**每個守衛都做過突變驗證**（改壞它，確認會轉紅）。過程中抓到自己兩條**恆真斷言**
與一個**沒有鑑別力的回歸夾具**，都已修正並在 CHANGELOG 記錄。

## 授權

MIT
