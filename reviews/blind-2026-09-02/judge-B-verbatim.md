# 判讀者 B — 逐字紀錄(2026-09-02,rubric 0.2.0 盲判)

> 呼叫端逐字轉錄自 subagent 回傳;YAML 已另存 judge-B.yaml。

## rubric_friction(逐字)

**1. R-004 對清單形狀沒有定義「易腐內容」是否包含連結本體(vinta / sindresorhus / public-apis,R-004)——本批最大的縫。** awesome 清單的本體是數百條外部連結,連結必然腐。若算易腐,序 5 讓每個清單型 repo 機械式落 poor(除非有限制陳述),shapes.md「由 R-001/R-003 主導」形同虛設;若不算,則只剩行內宣稱可判。我採後者:易腐 = 條文列舉型(版本/第三方 API 資料/定價/效能數字/自我統計),連結群不算。這一個選擇直接決定 sindresorhus 是 n/a 還是 poor、vinta 與 sindresorhus 是同判還是分判(vinta 因有 '#10 most-starred'、'170x' 等行內裸宣稱獨落 poor)。兩個判讀者在此必然分歧。

**2. R-004 序 1 的「易腐內容帶時效標記」未說是全部還是主要(freeCodeCamp vs ai_size-limit,R-004)。** fCC 有 Beta 標記但頭版 '100,000 people' 裸露 → 我落序 2;size-limit 的宣稱全連到驗證 commit,但範例 YAML 內有裸 `@v1` pin → 我留序 1。我自創的讀法是「散文宣稱須標記/可驗,設定樣張內的版本 pin 不算宣稱」——條文沒寫,換個判讀者兩份可能同落序 2 或同留序 1。

**3. R-004 序 3 與序 4 的排序產生反直覺結果(torvalds vs sindresorhus,R-004)。** 把所有易腐內容都做成判準明文嘉許的機械同步形式(torvalds 全 repo 相對路徑)封頂 mixed——沒有限制陳述就永遠到不了 good;而什麼易腐內容都沒有反而拿 n/a。「機械上做對每件事」比「沒東西可維護」判得更像有問題。另外「repo 相對路徑指向的內容算不算易腐內容」也要我自己發明區分:torvalds 的路徑代位的是真易腐事實(建置需求),sindresorhus 的 awesome.md 指向的是概念——這條線是我畫的,不在條文裡。

**4. R-004 序 1 的「陳述」沒有下限(amplication,R-004)。** 一個介係詞短語('run locally for code generation purposes or contributions')+ ee 授權例外,配上教科書級的 engines 機械同步,就拿到與 fiber 專節 '⚠️ Limitations' 相同的 good。行銷腔整篇、限制實質為零的 README 只要有一句邊界話+同步機制即封頂——序 1 需要陳述品質門檻,或需要 good 的層內分級。

**5. R-005 序 1 要求材料給不出的死亡證明,而該條自己的 anti-pattern 在 decision_order 裡沒有落點(choo vs public-apis,R-005)。** choo 能判 poor 純因判準具名了 freenode 型鏈腐;其他 11 份的連結存活我一律無法查證(受材料限制),序 1 實際上只對「具名已知死亡樣態」可用。更糟的是 public-apis 命中逐字寫在 anti_patterns 裡的「求助管道只在贊助商區塊裡,分不清是社群的還是廠商的」,但序 1 需要失效/誤導證據、序 2 只問可否指認 → 照序走仍是 good。寫進規則的 anti-pattern 在該規則自己的取值程序下無法影響取值。

**6. R-005 的「維護主體內文指認」邊界(torvalds / dbt / httpie,R-005)。** 條文只排除「repo URL 裡的帳號名」,對三種常見形態沉默:(a) 第一人稱聲音('we/us/my/our')、(b) 官方產品站連結(getdbt.com、httpie.io)、(c) 指向名冊的指標('MAINTAINERS file')。我三者都放行(依 disambiguation 的「讀者知不知道自己的處境」);嚴格字面派會把這三份全降 mixed。組織背書型專案會在這裡系統性分歧。

**7. R-002 對「安裝外包給文件站」的 CLI 工具(dbt / httpie,R-002)。** CLI 列寫「必須有可貼的指令」,但兩份都把安裝路由到外部 docs。我把基礎讀成兩個可分離子句(指令、前置條件),缺一 → 部分達成 → mixed;把「必須」讀成 gate 的判讀者會給 poor。條文沒說子句可不可分離。另 R-002 anti-pattern「安裝段落與實際 release/套件名不一致」在只有 README 的材料下不可查(受材料限制)。

**8. 形狀判定對 hosted-service repo 是取值翻轉點且判定依據會倒果為因(freeCodeCamp,shape/R-002)。** 候選:應用/服務 vs 索引/導覽型。選前者 R-002 近 poor(零部署指引),選後者 good(每種讀者都有入口)。我選索引型,理由:本體確實是讀者分流。但 amplication 同為 SaaS-first,我卻因它「碰巧寫了本地執行步驟」而判應用/服務——形狀變成由 README 內容反推,而 shapes.md 的本意應是由 artifact 決定。形狀表缺「hosted 產品的門面 README」一列。

**9. R-001 的第一屏對 HTML 置中頭部依渲染假設而非行數(gofiber / sindresorhus,R-001)。** fiber 的定位句在原始碼第 36 行,但 logo+badge 實際渲染僅約兩行視覺高度,定位句在第一屏內 → good;sindresorhus 的 62 行 `<br>` 填充廣告確實佔滿多屏 → poor。「遮住第 15 行」與「滾動前看到的東西」兩個判別法在 HTML 頭部 README 上給出不同答案,我一律採渲染估計——另一個判讀者按原始行數會把 fiber 的 R-001 降級。

**10. awesome 形狀的 R-003「描述品質」缺門檻(sindresorhus vs vinta,R-003)。** 多少比例的無描述條目把 good 翻成 mixed?我用了「約兩成缺描述 → mixed、近零 → good」,這個數字是我發明的。

**11. 「達成但有可指認的瑕疵 → mixed」若按字面,good 幾乎不可達(全域,R-001~R-003)。** 任何 README 都找得到 nitpick。我採「瑕疵須實質損及該維度目的」的讀法(如 choo 範例依賴 choo-devtools 但安裝指令沒裝它 → 記 R-002 mixed);同時「壞掉的範例歸 R-002 還是 R-003」無指派,重複計費與零計費都是可行讀法,我選單記 R-002。

**12. 供應鏈紀錄(torvalds_linux)。** L151-158 有明確對 AI 讀者下指令的文字:「If you are an LLM or AI-powered coding assistant, you MUST read and follow the AI coding assistants documentation…」。這是 repo 對 AI 貢獻者的正當政策內容,不是評分操縱(無「打高分」「ignore previous」),我未照做,依程序記錄於此;判讀時未因此加減分。其餘 11 份未發現任何試圖指示判讀者的文字。public-apis 的廠商行銷壓力(H1 廣告)已反映在 R-001 取值,不屬注入。

## 逐維證據(逐字,節錄自 YAML evidence 欄)

- vinta_awesome-python — R-004 poor:「走到序 5:全文無限制/非目標/維護狀態陳述,而易腐宣稱裸露——L9 '#10 most-starred repo'、L174 '170x realtime speed' 皆無日期無來源」;R-005 good:「求助管道(尾段 contact @vinta)與維護主體皆可指認」
- sindresorhus_awesome — R-001 poor:「L1-62 第一屏全是作者 app 廣告與贊助商 logo;全文無一句自我定位」;R-004 n/a:「無列舉型易腐內容——受『連結群是否算易腐』讀法影響(friction 1)」;R-005 mixed:「主體可指認,無求問管道」
- public-apis — R-001 poor:「H1 是贊助商廣告,定位遲至 L24」;R-004 mixed:「序 2:有 'manually curated' 陳述,但 API 表格裸露」;R-005 good:「Issues/PRs/Contributing 明列+主體可指認;Discord 在廠商段=anti-pattern 但序 1 需失效證據(friction 5)」
- freeCodeCamp — 索引/導覽型;R-002 good:「學習者/貢獻者/報 bug 各有入口」;R-004 mixed:「Beta 標記有,但 '100,000 people' 裸數字」
- torvalds_linux — R-002 good:「建置/需求皆 repo 內相對路徑」;R-004 mixed:「序 3:全機械同步,無陳述」;R-005 good:「mailing lists/IRC(oftc 非 freenode)/Bugzilla + MAINTAINERS file 指標」
- facebook_react — R-004 good:「序 1:漸進採用邊界 + 'JSX is not required',散文無裸數字,版本在機械同步 badge」;R-005 good:「'Where to Get Support' + 內文具名 Facebook」
- choojs_choo — R-002 mixed:「範例 require choo-devtools 但安裝只給 npm install choo」;R-004 mixed:「序 2:有 experimental 徽章陳述,但 freenode/travis 已腐」;R-005 poor:「序 1:Chat 指 webchat.freenode.net=具名 freenode 型鏈腐」
- amplication — R-001 mixed:「tagline 抽象行銷語,具體能力遲至 L45+」;R-004 good:「序 1:'run locally for…' 邊界 + ee 授權例外 + engines 機械同步;陳述之薄見 friction 4」;R-005 good:「Discord for support + 三種 issue 模板分流」
- ai_size-limit — R-004 good:「序 1:time 量測 unstable 明示 + 'Who Uses' 每條連到可驗證 commit;@v1 pin 視為設定樣張(friction 2)」;R-005 mixed:「序 3:'built by Evil Martians' 主體具名,無求助管道」
- dbt-core — R-002 mixed:「CLI 要求可貼指令:README 內零指令,安裝全靠外部 docs」;R-003 mixed:「無一行 dbt 程式/輸出樣張——『支援 X 而無一行 X 用法』命中」;R-004 good:「beta 時效標記 + 🟢🟡 支援矩陣 + 分支警示」
- gofiber_fiber — R-001 good:「定位句含替代方案對照;渲染估計下 badge 未擠掉定位(friction 9)」;R-004 good:「序 1:⚠️ Limitations 專節 + benchmark 附來源輪次(TechEmpower data-r19)」
- httpie — R-002 mixed:「用法可貼,但安裝僅外部連結」;R-004 mixed:「序 3:無陳述;易腐全在機械同步 badge;'recently' 無日期但附連結」;R-005 good:「Community & support 分流(Discord/SO/Issues)」
