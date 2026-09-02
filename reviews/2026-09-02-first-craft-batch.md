# 第一批 craft 判讀:6 個真實 README(2026-09-02)

> **這是本工具主判的第一次實測。** 在此之前只驗過 lint 半邊,
> 而 lint 恰好是本工具自己說「不是品質結論」的那半。

## ⚠️ 污染聲明(先讀這個,它決定結論怎麼折扣)

**判讀者是我,而我寫了這份 rubric。** 具體的污染來源:

1. **我知道條文的意圖**,不只是字面 —— 遇到模糊處我會往「我當初想抓什麼」靠
2. **我知道 41/41 那個教訓**(姊妹專案的 craft verdict 連續 41 次全 approved)
   —— 我**有動機讓它開火**,那是與「橡皮圖章」相反方向的偏誤,一樣是偏誤
3. **6 個樣本是我選的**,選樣時已知其中一個(`24kchengYe`)是姊妹專案判過的弱例

⇒ **本批不得充當 inter-rater 資料,也不得用來宣稱判準「校準好了」。**
它能回答的只有一個問題:**這條路徑會不會輸出 `needs-revision`。**

真正的校準需要**不知情的獨立判讀者**(不讀本檔、不讀 rubric 的意圖說明)。

---

## 結果

| repo | 形狀 | R-001 | R-002 | R-003 | R-004 | verdict |
|---|---|---|---|---|---|---|
| `visual-web-stack` | skill/工具 | good | good | good | good | **approved** |
| `claude-code-warp` | plugin/整合 | good | good | good | good | **approved** |
| `anthropics/skills` | collection | good | good | **mixed** | good | **approved-with-notes** |
| `superpowers-marketplace` | listing | good | good | **mixed** | **poor** | **needs-revision** |
| `Jeffallan/claude-skills` | collection | **mixed** | good | good | **poor** | **needs-revision** |
| `24kchengYe/human-skill-tree` | collection | **mixed** | **mixed** | 未判¹ | **poor** | **needs-revision** |

¹ 823 行,我只讀了第一屏、安裝段與標題清單,**不足以判 R-003 就不判**。
rollup 規則 3(任一 poor)已經決定 verdict,**R-003 的值不影響結果**,故結論仍成立。

**23 個已判維度標記:good 15、mixed 5、poor 3。**
**verdict:approved 2 / approved-with-notes 1 / needs-revision 3(50%)。**

### ⇒ 判準會說「不」。這是本批唯一站得住的結論。

姊妹專案的失敗模式(連續 41 個全 approved)**沒有重演**。
`mixed` 從第一天計費這個設計,在第一批就產生了輸出。

---

## ⚠️ 但「不」的成因高度集中,而那正是我預先標記過的那一條

**3 個 `poor` 全部出自 R-004(限制誠實),沒有一個來自其他三維。**

rubric 的 R-004 條文裡就寫著:

> 本條的形狀直接借自 skill-quality-research 的 L-004(anti-hallucination),
> 那一條是該專案跨兩輪一致性量測中**信度最低**的維度(κ=0.400)。
> ⚠️ **本條若過度觸發,先懷疑它,不要先調 rollup 門檻。**

第一批就撞上了。**這不是預言成真,是同一個設計缺陷被繼承過來。**

### R-004 的 `decision_order` 太容易走到 poor

現行順序:

```
1. 有明確的限制/非目標/適用邊界陳述        → 至少 mixed
2. 無上述,但也沒有易腐內容                → n/a
3. 無上述,而有易腐內容                    → poor
```

問題:**「有易腐內容」對任何 listing / collection 型 README 幾乎恆真**
(套件數、skill 數、支援清單、版本號)。於是這類 README 只要沒寫「已知限制」段,
**一律直達 poor** —— 而 poor 是 rollup 規則 3,單獨就翻 verdict。

`superpowers-marketplace` 與 `Jeffallan/claude-skills` 都是這樣被判掉的。
兩份都是**堪用甚至相當好**的 listing README。

### 而 Jeffallan 那個 poor 更可議

它的易腐數字寫成 `<!-- SKILL_COUNT -->67<!-- /SKILL_COUNT -->`
—— **機械同步的標記**,而姊妹專案實測過它有 CI 驗證 count consistency。

**那其實是一種「驗證方式」**,而 R-004 的高分要件正是「易腐內容帶時效標記**或驗證方式**」。
但 `decision_order` 的順序 1 只認「限制/非目標/適用邊界**陳述**」,
**看不到機械同步這種形式**。⇒ 條文把一個真的好做法判成了 poor。

---

## 三份 approved / approved-with-notes 的證據(判 good 也要附證據)

**`visual-web-stack`(approved)**
- R-001:「把跨套件整合的踩坑知識固化,讓第一版 scaffold 就符合架構規範」
  —— 一句話說清是什麼**與解決什麼問題**
- R-002:clone + `install.sh`,**並解釋替代路徑的 why**
  (「若目標已是目錄,`ln` 會把連結建到目錄**裡面**而非取代它」),還有驗證步驟
- R-004:**套件版本對照表 + 撰寫基準 2026-06 + `.asp-fact-check.md` 查證紀錄**
  —— 這是高分要件「易腐內容帶時效標記或驗證方式」的教科書例

**`claude-code-warp`(approved)**
- R-002:`Requirements` 段明列三項前置(含 `jq` 怎麼裝)、**安裝後要 restart 的警告**、
  預期結果(「you'll see a confirmation message」)
- R-003:`How It Works` 解釋 OSC 777、payload 結構、六個 hook 各自何時觸發、
  protocol version 協商 —— **真的 why,不是功能清單**
- R-004:`Legacy Support` 段講舊版 Warp 的降級行為 —— 那是適用邊界

**`anthropics/skills`(approved-with-notes)**
- R-004 good:**有明確 Disclaimer** —— 「provided for demonstration and educational
  purposes only… behaviors you receive from Claude may differ… Always test thoroughly」
- R-003 mixed:有 template 具體範例,但**幾乎沒有 why**
  —— 沒解釋為什麼 skill 要這樣設計、什麼時候該拆 references。是索引型文件,不是教學

---

## 判讀過程撞到的條文缺口(全部已入 misjudgments)

1. **`pass_criteria` 沒說「基礎達成但高分未達成」是 good 還是 mixed。**
   四個維度都寫成「基礎:… 高分:…」,但**沒有把它映射到取值域**。
   我採用的讀法是「基礎達成 = good;基礎部分達成或有可指認瑕疵 = mixed;基礎未達成 = poor」
   —— 那是**我選的,條文沒說**。另一個判讀者可以合理地選別的,結果會不同。
2. **形狀表沒有「索引/導覽型」這一列。** `anthropics/skills` 與
   `Jeffallan/claude-skills` 的 README 本體是**指向別處的目錄**,不是教學也不是清單。
   R-003 的「規則附因果理由」對它們幾乎不適用 —— 它們沒有規則要解釋。
3. **R-004 的 `decision_order` 看不到「機械同步」這種驗證形式**(見上)。

---

## 我刻意沒做的事

- **沒有為了讓判準開火而調鬆判讀。** 三個 poor 我都逐條對回條文的 `decision_order`,
  而且對其中兩個明白寫下「條文判它 poor,但我認為條文有問題」——
  **rubric 判對而我不喜歡結果,與 rubric 判錯,是兩件不同的事,不能混。**
- **沒有動任何條文。** 待處理累積到 5 條,仍未達 5–10 批次門檻的處理時機
  (紀律是累積後**一次**處理,不是邊判邊改)。
- **沒有宣稱這批驗證了判準。** 見污染聲明 —— 它只驗證了「這條路徑會輸出 needs-revision」。

## 下一步(按證據強度排序)

1. **派不知情的獨立判讀者重跑這 6 份** —— 這是唯一能把「會開火」升級成「判得準」的動作
2. 批次處理 misjudgments(現 5 條),重點是 R-004 的 `decision_order`
3. 擴大樣本到非 Claude 生態的 README(現有 6 份全是 skill/plugin 相關,**形狀偏斜**)
