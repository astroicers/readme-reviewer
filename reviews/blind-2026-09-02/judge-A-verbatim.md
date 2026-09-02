# 判讀者 A — 逐字紀錄(2026-09-02,rubric 0.2.0 盲判)

> 呼叫端逐字轉錄自 subagent 回傳;維度值已入 judges.yaml。
> ⚠️ 含具名 craft 判定 —— 未來的判讀者禁讀本目錄。

## rubric_friction(逐字)

1. **R-004 order 1/2 與 3/5 的量詞缺失——「易腐內容帶時效標記」是全稱還是存在?**(gofiber R-004、size-limit R-004、httpie R-004)真實 README 幾乎都是「載重宣稱有標記+邊角裸露」的混合體:fiber 的 benchmark 有來源與 round 標記但 tagline「fastest」裸露;size-limit 的縮減數字全連 commit 但範例 workflow 釘著 @v1。我採「實質載重宣稱有標記即過、殘餘記瑕疵」讀法判 good;全稱讀法會判 mixed。這條逼我自選讀法,而且直接改分。

2. **「易腐內容」是否包含外部連結本體——同一份 README 在兩讀法下落在取值域兩端**(sindresorhus R-004)。rule 例示的易腐類是宣稱型(版本號/第三方 API/定價/效能數字),sindresorhus 一項都沒有 → order 4 應判 `n/a`;但 equivalent_forms 說「外部 docs 一樣會腐」,且清單型的本體就是 600 條外部連結 → order 5 應判 `poor`。**n/a 與 poor 是兩個極端**,條文沒有裁決。我依 order 4 註記「差別是有沒有東西會過期」採 poor,但這是全案最不穩的一格。加重因素:shapes.md 對 awesome 型調整了 R-001/R-002/R-003 卻對 R-004 沉默,缺口全砸在清單型上。

3. **R-005 order 1 的「已失效」在無網路環境下只能靠世界知識**(choo R-005)。我判 poor 依據的是「freenode 已亡」這件世界知識,不是連結查證——若世界知識不可採,choo 會落 order 2 判 good:**單一維度在兩讀法下 poor↔good**。patterns.md 自己拿「freenode 型鏈腐」當例,暗示預期判讀者認得,但條文沒明說世界知識是否可採、要不要標低信心。choo 的 R-004(travis-ci.org 已消失)同此問題。

4. **R-005 decision_order 沒有 anti-pattern 的著力點**(public-apis R-005)。「求助管道只在贊助商區塊裡,分不清是社群的還是廠商的」是明列 anti-pattern,而 public-apis 的唯一聊天管道正是這個形狀。但 order 只有「失效/誤導→poor」和「皆可指認→good」可落:查不出「誤導」就只能給 good,anti-pattern 完全沒有輸出格位。缺一格「皆可指認但命中 anti-pattern → mixed」。

5. **取值映射「達成但有可指認的瑕疵=mixed」按字面讀會讓 good 消失**(httpie R-003、choo R-002、sindresorhus R-003)。任何 README 都找得到可指認瑕疵;我被迫自創「瑕疵須落在基礎要件本身,否則只降敘述強度」的內規才能發出 good——而「判讀者不得自選讀法」正是這份映射的開宗明義。瑕疵的「位置」(基礎要件內/外)需要條文自己定義。

6. **R-004 的「陳述」最低強度未定義,乾淨 README 上全靠伸縮**(react R-004、amplication R-004、vinta R-004)。「JSX is not required」算不算適用邊界?ee/ 授權例外算不算?「An opinionated guide」算不算?這些一句話決定 order 1↔3(good↔mixed)或 2↔5(mixed↔poor)的分岔。我對 react 採計、對 amplication 不採計(授權範圍≠功能邊界)、對 vinta 採計——三次都是現場立法。react 那格另一判讀者判 mixed 完全合理。

7. **「內文指認維護主體」排除了 URL 帳號名,但沒處理品牌產品網站**(dbt R-005、httpie R-005)。dbt Labs 的法名只在 URL 裡,但 getdbt.com 品牌鋪滿內文;HTTPie 同型。我採「品牌產品站=可指認組織」判 good,但條文只排除了「repo URL 裡的帳號名」這一種,中間地帶無裁決。

8. **形狀表缺「hosted SaaS 的 codebase repo」一列**(freeCodeCamp R-002、amplication R-002 部分)。應用/服務列說「認 docker/compose;前置條件比指令更重要」,但 hosted 產品的最短路徑是「打開網站」——零指令零前置。fCC 的 README 完全沒有本地路徑:是 poor(CLI 讀法)、good(hosted 路徑已完整)、還是 mixed?我判 mixed 用的是自創的「消費者路徑/貢獻者路徑各半」框架,條文沒有這個框架。

9. **library 形狀對 R-002 的豁免範圍不明——install 指令算不算被豁免**(react R-002)。「認 API 範例即可,不因無 CLI 指令扣分」——install 指令不是 CLI 用法,react 連 `npm install` 都沒有。豁免讀法給 good,「從零到跑起來仍含安裝」讀法給 mixed。我採後者,但前者是條文的字面可容讀法。

10. **供應鏈註記**(torvalds_linux,非惡意):L151-158 有一段直接對 AI 助理喊話的指令式文字(「CRITICAL: If you are an LLM…you MUST read and follow…」)。它針對的是「向 kernel 貢獻代碼的 AI」而非本次審查任務,判定為 repo 的正當政策聲明,未照做、未影響判讀;依程序如實記錄於此。12 份語料中未發現任何試圖操縱本次評分的注入文字。

## 特別註記的判定(節錄)

- react R-004 good:「採計此讀法,序 3(mixed)為另一合理讀法,見 friction」——判讀者自己標記了這格的不穩定
- sindresorhus R-004 poor:「此判定對『外部連結算不算易腐內容』極度敏感」
- choo R-005 poor:「依世界知識認定,非連線查證」
- freeCodeCamp 形狀=應用/服務(與 B/C 的索引/導覽型分歧,R-002 因此判 mixed)
