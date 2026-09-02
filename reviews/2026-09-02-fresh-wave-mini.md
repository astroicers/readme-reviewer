# fresh 波 readme 小輪(2026-09-02,5 份野生 README)

> rubric/工具 **0.4.0**。語料:skill-quality-research 熟成輪 F1 收集
> (`clone-manifest-fresh-wave.json` 的 readme_targets,2026-08 後新 repo、
> commit 已釘)。判讀紀律:R-004/R-005 記序號;verdict 走 rollup。
> ⚠️ 含具名 craft 證據。

## 總表

| README | R-001 | R-002 | R-003 | R-004(序) | R-005(序) | verdict |
|---|---|---|---|---|---|---|
| dmmulroy/anti-slop | good | good | good | good(序1) | mixed(序2) | **approved-with-notes** |
| EverMind-AI/SkillCorpus | good | good | good | good(序1) | good(序3) | **approved** |
| boyang-hu/website-rebuild-skill | good | good | good | good(序1) | mixed(序2) | **approved-with-notes** |
| Vincentwei1021/video-talkcraft | good | good | good | good(序1) | good(序3) | **approved** |
| leopard627/fire-your-seo-agency | good | good | good | **mixed(序2)** | **mixed(序2)** | **needs-revision** |

## 逐份要點(證據錨)

- **anti-slop**:R-004 序1 模範——「Analysis boundaries」節明說不做 type-checker 級
  推斷、enforcement intentionally local;「reflects my preferences rather than a
  universal standard」是罕見的誠實定位。R-005 序2:維護主體與 vendored 哲學極明確
  (「the vendored files are yours to maintain」),但**零求助管道**。
- **SkillCorpus**:R-004 序1 標竿——Results 表附 arXiv Table 1、±CI、z 值;
  Roadmap checkbox 誠實列未出貨項。R-005 序3(Discord 動態人數 badge + WeCom)。
  findings:Roadmap 內殘留 `<!-- TODO(@team): first pass — edit to match your plan -->`
  內部註解(不傷序,記瑕疵)。
- **website-rebuild-skill**:R-004 序1——「≈95%/≈98%/18-18/消失率 29%」全部
  附逐站實測錨(已驗證網站表);「關於版權:能不能做,和該不該公開,是兩回事」
  是 non-goals 的倫理級寫法。R-005 序2:version+CHANGELOG badge 是維護訊號,
  求助管道未見。
- **video-talkcraft**:R-005 序3 亮點——微信群(雙向)+ FAQ 分流 +
  **「二維碼過期後會不定期更新;也可通過上方社媒直接聯系作者」**(管道時效的
  誠實處置,首見)。R-004 序1(每卡「已知坑」;credits 全附連結)。
- **fire-your-seo-agency**:R-004 **序2**,裸露清單:[+85,578% MoM / 1.54M
  impressions / 7.4K clicks 社會證明統計組(出處僅 Threads broadcast 帳號,
  不可核驗到數字頁)、$400–2,500/month 市場價格帶、「half the Korean market」
  市占句]。R-005 序2:管道缺、主體僅 repo owner 隱含,Threads=broadcast 不算雙向。
  其餘三維紮實(五 lane 表、refuses 節、雙路安裝+scorecard 樣張)。

## 生態觀察

**R-005 是野生語料的主要失分維(3/5 非 good)**——B1(全自家 repo)一輪把管道
全補齊了,看不到這個分佈;缺求助管道是生態常態,rubric 在這一維的鑑別力
於野生語料首次實測活躍。R-004 序1 在 4/5 成立——高星野生 README 的宣稱
紀律比預期好(帶 CI 的 benchmark 表、逐站實測錨都出現了)。

## 儀器發現(→ misjudgments 蓄積 +1)

- **`lint_readme.py` 對不存在的 README 靜默 fails-open**:餵入檔案路徑
  (非 repo_dir)時不報錯,輸出缺席型 findings(無 H1/無安裝段)——五份輸出
  **完全相同**才被識破。若語料只有一份,這個空讀會被當真。修法方向:
  README 解析目標不存在時硬失敗。
- **協定註記**:README-only 語料(抓檔不 clone)使 H-005 死連結**不可判**——
  連結指向 repo 內存在的檔案。本輪 H-005 一律不計 repo 缺陷;
  與 skill 側 collection_sampling 單檔語料待測同構。
