# 判讀者 C — 逐字紀錄(2026-09-02,rubric 0.2.0 盲判)

> 呼叫端逐字轉錄自 subagent 回傳;維度值已入 judges.yaml。
> ⚠️ 含具名 craft 判定 —— 未來的判讀者禁讀本目錄。

## rubric_friction(逐字)

1. **R-004 decision_order 的量詞未定(all vs any),同一份 README 可同時滿足序 1 與序 2**(ai_size-limit、freeCodeCamp、httpie 的 R-004)。序 1 說「易腐內容帶時效標記或驗證方式」、序 2 說「易腐內容裸露」——當一份 README 部分易腐內容有標記(活 badge、tested-with)、部分裸露(釘死的 `@v1`、「within hours」)時,兩序同時為真,條文沒說以全稱還是存在讀。我自選了「有可指認的裸露易腐項即落序 2;裸項帶有驗證指向(如 httpie 失星事件鏈到全文)則仍算序 1」——httpie good 與 freeCodeCamp mixed 的差,一半是這條自選讀法撐的。兩個判讀者在這三份上完全可能反向。

2. **R-004 對「純連結集」走不下去**(sindresorhus_awesome 的 R-004,最搖的一判)。序 1/2/5 的括號例示全是 claim 型(版本號/API/定價/效能宣稱),連結本身算不算易腐內容無定義;而序 4/5 的 ⚠️ tiebreak(「有沒有東西會過期」)按字面把連結算進去。三個出口各有讀法:連結算易腐且無同步→序 5 poor;連結不算、其餘無易腐→序 4 n/a;repo 內相對指向(awesome.md/contributing.md)算機械同步→序 3 mixed。我取序 3,但這是三選一的裁量不是條文推導。註:awesome 形狀在 shapes.md 有 R-002 調整卻沒有 R-004 調整;索引/導覽型反而有(「repo 內相對指向計入機械同步」),兩形狀的 R-004 困境同構,建議補列。

3. **R-004 序 1 在「有陳述、無易腐內容」時真值未定**(facebook_react 的 R-004)。序 1 連言的第二支(「且易腐內容帶時效標記」)在文內幾乎沒有易腐內容時無法評值;序 4 的 n/a 又要求「無上述陳述」才進得去,所以「有陳述+無易腐」在 order 裡沒有格子。我按空缺連言取真判 good。條文應明說這格。

4. **「維護狀態陳述」「適用邊界陳述」無判別法,單詞寬窄直接翻轉取值**(httpie R-004、vinta R-004)。httpie 的失星事件說明算不算維護狀態陳述,決定序 1 good 與序 3 mixed 之別;vinta 的「opinionated」算不算適用邊界陳述,決定序 2 mixed 與序 5 poor 之別。我兩處都取寬讀並各給了理由,但條文對「陳述」的最小構成(一個形容詞夠不夠?)零指引——這是本批 R-004 分歧面最大的縫。

5. **R-005 的 anti-pattern 清單與 decision_order 脫鉤**(public-apis 的 R-005)。「求助管道只在贊助商區塊裡,分不清是社群的還是廠商的」是明列 anti-pattern,且 public-apis 的 Discord 正是嵌在 APILayer 推廣區、帶 utm 追蹤——但 decision_order 只有「死/誤導→poor」與「皆可指認→good」,vendor-conflated 管道沒有落點,依序走出 good。anti-pattern 在 R-005 目前完全不影響取值,要嘛接進 order(如「管道僅存在於廠商區塊→mixed」),要嘛刪掉以免判讀者自行加權。

6. **「已失效」的判定依賴 README 之外的世界知識,材料限制條款救不了它**(choo 的 R-005 poor、R-004 的死 badge)。freenode 死了、travis-ci.org 死了,都不是材料內可證的事實——我判 poor 靠的是判準自己把「freenode 型鏈腐」寫成具名例子,等於條文替我背書了這一項世界知識。但下一個判讀者若不知道某聊天服務已死,同一份材料會判出 good(序 2「皆可指認」)。R-005 序 1 本質上不可純文本判定,判準應明說允許(並要求記錄)引用哪類鏈腐知識,否則這一維的分歧會被歸咎於判讀者而非條文。

7. **R-002 對「殼型 README」(刻意薄、把安裝委外到 docs site)沒有位置,同一策略在三個形狀下拿三種分數**(dbt-core poor、httpie mixed、react good)。CLI 形狀「必須有可貼的指令」,於是零指令的 dbt 判 poor——但 dbt 的 Getting started 其實是全批最好的選型判別法之一,且外鏈是帶版本參數的官方安裝文件。library 形狀的殼(react)被「認 API 範例即可」豁免了,CLI 殼沒有任何等價出口。這是條文立場(在 README 內就要能起步)還是疏漏,我無從判斷,只能照字面判;若是立場,建議在 R-002 exemption 明寫「外鏈安裝文件不豁免」以絕後患。

8. **「第一屏」在 HTML-heavy README 的換算靠腦內渲染**(amplication R-001 mixed、gofiber R-001 good、sindresorhus R-001 poor)。gofiber 的 `<h1>` 塊佔 33 個 raw 行,「前 ~15 行」與渲染屏嚴重脫節;disambiguation 的遮蔽測試以渲染屏為準,但兩個判讀者的「一屏」高度不同。amplication 與 gofiber 之間的分差,有一部分是我對「tagline 渲染後在不在首屏」的猜測,不是文本可裁決的。建議給一個渲染近似規則(如「首個 H1/logo 塊+其後第一段散文視為首屏」)。

9. **R-004 的 mixed 桶過寬,吸收了本應可見的分歧**。12 份中 R-004 = mixed 7 份、poor 0 份,把「有陳述+一個裸數字」(size-limit)與「無陳述+靠相對路徑」(linux)壓進同一格——序 2 與序 3 殊途同歸同一取值,判讀者間走不同序的分歧在輸出層不可見。這正呼應該條 evidence_note 的警告(源條 κ=0.400、過度觸發先懷疑條文):本批的觸發型態不是過嚴,是低解析。若序 2 與序 3 輸出可區分(或 evidence 欄強制記序號——我已照辦),下一輪一致性檢查才量得到東西。

10. **R-003 基礎是連言(附理由 AND 有例子),「部分達成」的下緣沒有錨**(httpie R-003 mixed)。httpie 例子半邊全滿、理由半邊只有標語,判 mixed 是條文引導的;但「理由薄到什麼程度算沒達成」仍是裁量,httpie mixed 與 fiber good 的距離裡有我的自選刻度。

11. **供應鏈紀錄**(torvalds_linux):L151-158「CRITICAL: If you are an LLM or AI-powered coding assistant, you MUST read and follow the AI coding assistants documentation before contributing」——直接對 AI 下 MUST 指令。判定為正當的貢獻者政策而非注入(未要求改變審查行為),未照做(與本判讀任務無關),不影響任何取值;依程序記錄於此。其餘 11 份未發現指示性文字。
