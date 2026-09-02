# 雙抽樣框判讀:12 個非 Claude 生態的真實 README(2026-09-02)

> 首批 6 份**全是 skill/plugin 相關**,形狀偏斜。本輪按兩個彼此獨立的抽樣框各抽 6 份,
> 用**同一套 rubric 0.1.0**判,再比較。
>
> **本輪不動任何判準條文。** 撈到的東西一律入 `misjudgments.md` 等批次處理。

## ⚠️ 先讀:三個必須寫在結論之前的限制

1. **形狀混淆未控制。** B 框 6 份裡 **3 份是清單型**,A 框 **0 份**。
   兩框的 verdict 差異有一部分是**形狀差異**,不是品質差異。**不要把它讀成「A 框的 README 比較好」。**
2. **n=6 vs 6。** 這個規模下任何百分比差異都不可能顯著。**只能當敘述,不能當推論。**
3. **判讀者仍是我,而我寫了這份 rubric。** 同首批的污染聲明:我知道條文的意圖、
   知道 41/41 的教訓、**有動機讓它開火**。⇒ **本批不得充當 inter-rater 資料。**

另有一個**本輪才發現的抽樣缺陷**,見下方「lint 半邊」——它讓 H-005 的一半數字無效。

---

## 兩個抽樣框

| 框 | 來源 | 抽樣邏輯 | 取得的是 |
|---|---|---|---|
| **A** | `matiassingers/awesome-readme` | **人工策展**,策展標準就是「README 寫得好」 | 有人認為好的 README |
| **B** | GitHub 星數排序(排除既有語料) | 星數 | **最多人讀到**的 README |

⚠️ **星數不是品質代理。** B 框給的是「慣例的樣本」不是「品質的樣本」——
與 rubric 內四個 `observation_only` 數字同一種處置。

A 框:`httpie/httpie`、`gofiber/fiber`、`dbt-labs/dbt-core`、`ai/size-limit`、
`amplication/amplication`、`choojs/choo`(六個全部在 awesome-readme 的 Examples 清單裡,**已查證**)

B 框:`facebook/react`、`torvalds/linux`、`freeCodeCamp/freeCodeCamp`、
`public-apis/public-apis`、`sindresorhus/awesome`、`vinta/awesome-python`

**刻意保留 B 框的清單型**——那才是「高星 repo」的真實組成(星數前 15 名裡 8 個是清單/課程型)。

---

## craft 判讀結果

verdict **全部由 `craft_verdict_rollup()` 純函式算出**,無一手推。

| 框 | repo | 形狀 | R-001 | R-002 | R-003 | R-004 | verdict |
|---|---|---|---|---|---|---|---|
| A | `httpie/httpie` | CLI | good | mixed | good | **poor** | needs-revision |
| A | `gofiber/fiber` | library | mixed | good | good | good | approved-with-notes |
| A | `dbt-labs/dbt-core` | 應用/服務 | good | mixed | good | good | approved-with-notes |
| A | `ai/size-limit` | 工具/library | good | good | good | good | **approved** |
| A | `amplication/amplication` | 應用/服務 | mixed | good | mixed | **poor** | needs-revision |
| A | `choojs/choo` | library | good | mixed | good | mixed | needs-revision |
| B | `facebook/react` | library | good | good | good | **poor** | needs-revision |
| B | `torvalds/linux` | 路由/索引 | good | n/a¹ | good | **poor** | needs-revision |
| B | `freeCodeCamp/freeCodeCamp` | 應用+內容 | good | mixed | good | good | approved-with-notes |
| B | `public-apis/public-apis` | 清單 | **poor** | n/a | mixed | **poor** | needs-revision |
| B | `sindresorhus/awesome` | 清單 | **poor** | n/a | good | **poor** | needs-revision |
| B | `vinta/awesome-python` | 清單 | good | n/a | good | **poor** | needs-revision |

¹ `linux` 的形狀最接近「monorepo / 根 README 只做路由」,而 rubric 對該形狀的處置是
「**以子文件抽樣**評分」。**本輪只下載 README、沒有 repo,那個抽樣做不到** ⇒ 判 `n/a` 並註明原因。
**「查不了」與「查過沒問題」是兩件事**,不用 good 混過去。

**A 框**:approved 1 / approved-with-notes 2 / needs-revision 3
**B 框**:approved 0 / approved-with-notes 1 / needs-revision 5

44 個已判維度標記:**good 26 / mixed 9 / poor 9**(另 n/a 4)。

### 兩框的差異能說什麼、不能說什麼

- **不能說**「策展框的 README 比較好」——n=6、形狀未控制。
- **可以說**:B 框的 5 個 needs-revision 裡,**3 個是清單型**,而清單型在本 rubric 下
  結構性地容易失分(R-002 被豁免掉一格 ⇒ 剩三維,其中 R-004 對清單型幾乎必觸發)。
  ⇒ **這個差異更可能是形狀的,不是品質的。** 這正是限制 1 說的事,而它在資料裡看得見。

---

## ⭐ 本輪最有解釋力的一條:R-004 的 `mixed` 幾乎不可達

本批 R-004 的 12 個標記:**good 4 / mixed 1 / poor 7**。

**9 個 poor 裡 7 個出自 R-004**(其餘 2 個出自 R-001)。
**兩批合計 12 個 poor,10 個出自 R-004** —— 而 R-004 只是四維之一。

成因不是「R-004 太嚴」這種模糊講法,是**兩條條文交互後的結構**:

```
decision_order:
  1. 有明確的限制/非目標/適用邊界陳述  → 至少 mixed
  2. 無上述,但也沒有易腐內容          → n/a
  3. 無上述,而有易腐內容              → poor
```

- 順序 2 幾乎不可能成立(**任何真實 README 都有易腐內容**),於是實際只剩 1 與 3。
- 而 `pass_criteria` 的讀法(首批採用、本批沿用)是「基礎達成 = good」。
  ⇒ 走到順序 1 的 → **good**;走不到的 → **poor**。
- **`mixed` 只在「有限制陳述、但易腐內容已實際腐壞」這種窄縫裡出現**
  (本批唯一一個:`choojs/choo`,Travis CI badge 與 freenode chat 連結都已名存實亡)。

⇒ **R-004 事實上是個二元開關**,而它是四維裡唯一能單獨翻 verdict 的那個(rollup 規則 3)。
這比首批記的「順序 3 太容易走到」更精確:**問題不只在順序 3,在整條路徑只有兩個出口。**

### 而「機械可查證的易腐內容」被判 poor,本批又多兩個實例

首批記過一個(`Jeffallan` 的 `<!-- SKILL_COUNT -->67<!-- /SKILL_COUNT -->` + CI 驗證)。本批:

- **`amplication`**:「You are using a supported node version(**check `engines` `node` in the
  [package.json](./package.json)**)」—— 把易腐數字**指向單一事實源**,不在 README 裡複製一份。
- **`torvalds/linux`**:全篇易腐內容**幾乎都是 repo 內相對路徑**
  (`Documentation/admin-guide/reporting-issues.rst` 等 30+ 條),隨 repo 一起版控、天然同步,
  而且 GitHub 會直接顯示斷連結。

**這三個是同一族:把易腐內容交給機器維護,而不是寫一句「截至 2026-08」。**
R-004 的高分要件明寫認可「驗證方式」,但 `decision_order` 順序 1 只認
「限制/非目標/適用邊界**陳述**」——**看不到機械同步這種形式**。
⇒ 既有那條 misjudgment 的 n 從 **1 升到 3**,而且三個實例的機械形式各不相同(HTML 註解標記 /
指向 manifest / repo 內相對路徑),不是同一招的重複。

---

## ⭐ R-001 第一次產生 poor,而且機制可指認

首批 3 個 poor 全在 R-004;本批 R-001 出現 **2 個 poor**,兩個的成因是同一個:

- **`public-apis/public-apis`**:H1 是 `# APILayer Unified Suite in now Live! 🎉 🥳`
  ——**贊助商的產品標題**。repo 自己的定位句在**第 24 行**。
  遮住第 15 行後,讀者會以為這是 APILayer 的產品 repo。
  (順帶:該標題有 typo「in now Live」,且贊助段把 mediastack 列了兩次、一次拼成「Markestack」)
- **`sindresorhus/awesome`**:前 78 行是 logo + **作者自家 macOS app 的廣告**(Supercharge)
  + 贊助商 logo 牆。**整份 README 沒有一句「這是什麼」的散文**,
  定位外包給第 64 行的 `<a href="awesome.md">What is an awesome list?</a>`。

**判 poor 而非 mixed 的理由**:第一屏傳達的不是「定位缺席」,是**錯誤的定位**——
讀者拿到的是別的東西的定位。那比什麼都沒有更糟。

⚠️ **對 `sindresorhus/awesome` 要說清楚一件事**:「Awesome」是極高辨識度的品牌,
對已知者不需要定位。**但 rubric 明文禁止把知名度算進判定**(那正是「星數關聯打包面」的教訓)。
所以照條文判 poor,並在這裡註明我知道這個張力。

**這條的意義**:判準不是只有 R-004 會說「不」。R-001 有獨立的、可指認的觸發機制,
而且它抓到的東西(第一屏被行銷內容佔據)**恰好是兩個高星 repo 的真實缺陷**。

---

## lint 半邊:8 個命中,**目前零個確認的真陽性**

| 規則 | 過 | 未過 | 判讀 |
|---|---|---|---|
| H-001 README 存在且非空 | 12 | 0 | — |
| H-002 有文字 H1 且不只是 repo 名 | 5 | **7** | 5 個是**已文件化**的假陽性;**2 個是新缺陷**(見下) |
| H-003 有安裝或使用段落 | 7 | **5** | 3 個**清單型豁免**、1 個真、**1 個新缺陷** |
| H-004 ≥70% fence 標語言 | 12 | 0 | — |
| H-005 相對連結指得到東西 | 4 | **8** | **相對路徑那一半本批全部無效**;anchor 那一半 **12 個命中疑似全為缺陷** |
| security 紅旗 | — | — | **0**(12 份全乾淨) |

### ⚠️ 抽樣缺陷:H-005 的相對路徑那一半無效

**我只下載了 README,沒有 clone repo**,所有相對連結當然指不到東西 ⇒ 16 個相對路徑命中
**一律不採計**。這是**使用陷阱不是工具缺陷**,但它必須寫進文件:
`lint_readme.py` 的 H-005 需要**完整的 repo**,不是一個 README 檔。

同一個缺陷還讓 `linux` 的 R-002 判不了(見表格註 ¹)。**一個抽樣捷徑,兩處後果。**

### ⭐ 新缺陷 1:`HEADING_RE` 只認 ATX 標題 —— 一個根因、三個面向

```python
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
```

**setext 標題(`===` / `---` 底線)與 HTML `<h1>` 全盲。** 實測:

| repo | ATX | setext | HTML heading | 後果 |
|---|---|---|---|---|
| `torvalds/linux` | **0** | **15** | 0 | lint 看到**零個標題** |
| `choojs/choo` | 56 | 0 | 3(`<h1 align="center">Choo</h1>`) | H-002 誤報「無文字 H1」 |

`torvalds/linux` 是最乾淨的實例。它的 README 有 `Linux kernel` / `Quick Start` /
`Essential Documentation` 等 **15 個 setext 標題**,而 lint 認為它一個標題都沒有 ⇒

1. **H-002** 報「無文字 H1」——**假陽性**,它有 H1(`Linux kernel`)
2. **H-003** 報無安裝段——**假陽性**,它有 `Quick Start` 段且含 build 指引
3. **`broken_links` 的 own-anchor 集合為空** ⇒ 任何同檔 anchor 連結都會被報死鏈

**這是本 repo 反覆撞到的同一種形態**(「修的是那一支,還是那一類?」):
一個 regex 的覆蓋缺口,順著三條路徑輸出三個看起來無關的錯誤。

### ⭐ 新缺陷 2:`github_slug()` 折疊連續空白,GitHub 不折疊

```python
return re.sub(r"\s+", "-", s.strip())      # 連續空白 → 單一 "-"
```

GitHub 是**逐個空白換一個 `-`**。含被移除標點的標題因此算錯:

| 標題 | GitHub 實際 anchor | 我們算出 |
|---|---|---|
| `Art & Design` | `art--design` | `art-design` ❌ |
| `Data Ingestion & ETL` | `data-ingestion--etl` | `data-ingestion-etl` ❌ |

本批 anchor 死鏈 **12 個命中,12 個都是這個形狀**
(`public-apis` 8、`awesome-python` 2、`choo` 1、`amplication` 1)。

**佐證強度**:那些 `#art--design` 連結是三個獨立、長期維護的高星 repo 寫的,
而 GitHub Docs 明說 anchor 可以從渲染後的標題直接複製
(“Hovering over a heading reveals a link icon… to display the anchor”)
⇒ **ground truth 是作者從 GitHub UI 抄來的**,不是我推的。

### 新缺陷 3:`broken_links` 不認 HTML 具名錨

`amplication` 的 `#contributing_anchor` 對應 `<a name="contributing_anchor"></a>`——
GitHub 認,我們不認 ⇒ 假陽性。

⇒ **H-005 在本批 8 次開火,`0` 個確認的真陽性。** 相對路徑那一半被抽樣廢掉,
anchor 那一半疑似全是上面兩條缺陷。

### H-002 的 7 次未過,拆開來看是三件不同的事

| 成因 | 數量 | repo | 性質 |
|---|---|---|---|
| logo 圖片取代 H1 | 5 | httpie / dbt-core / fiber / freeCodeCamp / sindresorhus-awesome | **條文已文件化**的假陽性,已交 LLM 複核 |
| HTML `<h1>` 有文字 | 1 | choo | **新缺陷** |
| setext H1 | 1 | linux | **新缺陷** |

⚠️ **本批不能拿來強化既有的 H-002 misjudgment**——那一條講的是
「H1 **等於 repo 名**時記 warning」,而**這一支本批零次觸發**
(我的抽樣目錄叫 `ai_size-limit` 而非 `size-limit`,比對根本沒對上)。
**7/12 說的是另一支。** 混為一談會讓證據說謊。

---

## 三個 triangulation 來源已逐條查證(2026-09-02)

| 來源 | 狀態 | 查到的關鍵事實 |
|---|---|---|
| **GitHub Docs — About READMEs** | ✅ | 五項內容清單 + 相對連結行為 + 自動 TOC + anchor 複製 |
| **Standard Readme `spec.md`** | ✅ | Title / Short Description 規則、必要 vs 選用章節與順序 |
| **`matiassingers/awesome-readme`** | ✅ **新增來源** | 120+ 人工策展,**逐條附收錄理由** |
| Make a README | ⏳ 未查 | — |
| Diátaxis | ⏳ 未查 | — |

### ⭐ 而 awesome-readme 的收錄理由裡,**零次**提到限制誠實或前置條件

A 框六個 repo 在 awesome-readme 裡的策展理由(逐字):

> `httpie` — "Description of what the project does. Demo screenshots. Project logo. TOC for easy navigation."
> `dbt-core` — "Project banner, super clear description (friendly to people brand new to the product)…"
> `size-limit` — "Project logo, clear description, screenshot, step-by-step installing instructions."
> `amplication` — "Clear project logo. Brief explanation. All features explained…"
> `choo` — "Badges, clean, clear. Beautiful little menu above the fold with useful links."
> `fiber` — "Clean project logo. Useful badges and links…"

**六條全部落在 R-001(定位/第一屏)與 R-003(具體例子/截圖)**,
**沒有一條提到 R-004 要的東西**(限制、非目標、易腐內容的時效標記),
也**沒有一條提到 R-002 的前置條件**。

這是我目前唯一能查證的**外部人類策展標準**,而它與本 rubric 主要的失分來源**完全不重疊**。

⚠️ **這不足以推翻 R-004,理由要說清楚**:awesome-readme 的理由**高度偏視覺/打包面**
(logo、banner、badge、screenshot 出現在六條裡的每一條),
而姊妹專案六個 phase 的結論正是**「打包面關聯星數,不關聯工藝」**。
⇒ 一個偏打包面的策展標準不提 R-004,**既可能是 R-004 過重的證據,
也可能是那個策展標準本身沒在看工藝**。兩種讀法都成立,資料分不開。

**能寫下的只有**:R-004 的權重目前**沒有任何外部支持**,而它承擔了 10/12 的 poor。
兩件事放在一起,構成下一輪批次處理的優先項——**但不是這一輪的修改理由**。

### 本 repo 的 README 違反 Standard Readme 的 Short Description 規則

spec 明文:"Must not have its own title" / "Must be less than 120 characters" /
**"Must not start with `> `"** —— 而 `readme-reviewer/README.md` 的定位句就在 blockquote 裡。

⚠️ **這是分歧不是錯誤**:那是該 spec 的規定,不是普世真理(GitHub Docs 沒這條)。
但既然引用它當來源,**分歧就要註明**。已入 misjudgments。

### GitHub Docs 五項中有兩項無維度承載

| GitHub Docs | 本 rubric |
|---|---|
| What the project does | R-001 ✅ |
| Why the project is useful | R-001 ✅ |
| How users can get started | R-002 ✅ |
| **Where users can get help** | **無** |
| **Who maintains and contributes** | **無** |

Standard Readme 獨立佐證同兩項(Contributing 要求 "State where users can ask questions";
Maintainers 要求 "along with one way of contacting them")。

**兩個獨立來源都要求、而本 rubric 一個維度都沒有** —— 這是目前證據最強的一條缺口。
順帶:本批 12 份裡有 **10 份**寫了可指認的求問管道
(沒寫的是 `sindresorhus/awesome` 與 `ai/size-limit`),**判準對此完全看不見**。
(⚠️ 原版寫 11 份且稱 awesome 是唯一——size-limit 也沒有,批次處理的獨立複審
F-07 抓到後更正;它指向 estimo 的 issue 連結是別的 repo 的,不算自己的求助管道。)

---

## 我刻意沒做的事

- **沒有修任何一條**,包括三個已用實測確認的程式缺陷(setext/HTML 標題、slug 折疊、HTML 具名錨)。
  紀律是累積後**一次**處理;而**在量測的同一輪修判準會污染下一輪量測**
  (姊妹專案 `docs/llm-judge-contamination.md` §3 的具名教訓)。
  ⇒ 待處理達批次門檻上緣,下一個動作就是批次處理。(⚠️ 原版寫「現已 10 條」,實際登記完成後是 **12 條**——`misjudgments.md` 與 CHANGELOG 記 6→12 為準;複審 F-15 抓到三處不一致,以此更正。)
- **沒有挑掉 B 框的清單型**讓它「看起來公平」——那會把抽樣框改成不是它自己。
- **沒有宣稱兩框比較有統計意義**。
- **沒有用「A 框是策展的所以比較好」來解釋差異** ——資料顯示差異更可能來自形狀。

## 下一步(按證據強度排序)

1. **批次處理 misjudgments(10 條)**,優先序:
   (a) 三個程式缺陷(有實測、有 ground truth、修法明確);
   (b) R-004 的二元開關結構(10/12 的 poor + 零外部支持);
   (c) 「去哪求助 / 誰維護」兩個內容面(兩個獨立規範都要求)
2. **派不知情的獨立判讀者重跑這 12 份**——仍是唯一能把「會開火」升級成「判得準」的動作
3. 查證剩下兩個來源(Make a README、Diátaxis)
