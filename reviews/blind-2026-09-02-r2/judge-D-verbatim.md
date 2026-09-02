# 判讀者 D — 逐字紀錄(2026-09-02,rubric 0.3.0 盲判,第二輪)

> 呼叫端逐字轉錄;維度值另存 judges-030.yaml。⚠️ 含具名 craft 判定,未來判讀者禁讀。

## rubric_friction(逐字)

**1. torvalds_linux × shapes.md × R-003 —— 形狀表的反推禁令把一種真實形態排除在表外,且判定會整維翻轉。**
torvalds/linux 的 README 是純讀者分流(「Who Are You? Find your role below」),與「索引/導覽型」列的括號註解(文件路由、讀者分流)逐字吻合;但 ⚠️ 規則說形狀由 repo 主體決定,而 repo 主體是 kernel 原始碼 → 只能落「應用/服務」。兩個候選:應用/服務(擇之,理由:artifact 是要建置部署的系統軟體)vs 索引/導覽型(棄,因為那正是被禁止的「由 README 內容反推」)。後果:R-003 在應用/服務下是 poor(零理由零例子),在索引型下是 good(導覽結構反而是範本級)。形狀表缺一列:「單一專案、正典文件在 repo 內、README 是文件前門」。兩位判讀者在這裡幾乎必然分歧。

**2. torvalds_linux × R-002 —— delegation_stance 只定義了 CLI/library/hosted 三種形狀,應用/服務沒有立場。**
kernel README 的建置與前置全是 repo 內文件指向、零 inline 指令。CLI 立場會判 poor,library 立場會豁免,應用/服務列只說「前置條件比指令更重要」——repo 內指向算不算「明說」沒有規則,我只能內插出 mixed。建議為應用/服務補一條 delegation_stance(特別是「repo 內相對指向」是否視同前置已交代)。

**3. R-004 的「載重/非載重」邊界全靠括號裡一句「讀者會據以行動或決策的」,邊際案例是判讀者自選讀法。**
三個我被迫自裁的案例:httpie「We lost 54k GitHub stars」(判非載重——已定歷史事件不會腐,但條文沒定義「dated 的歷史統計算不算易腐」);size-limit「≈2 kB style-loader」(判非載重殘餘——行動由規則驅動、數字只是解釋量級);freeCodeCamp「100,000 people got their first developer job」(判載重 → 拉到 mixed)。三案的分界原則(「歷史完成式不腐」「解釋性量級非載重」)是我自己立的法,條文沒有。

**4. gofiber × R-004 序1 的「皆」字讓散文版語言版本需求幾乎必然封頂 mixed —— 疑似過度觸發形態。**
「Fiber requires Go version 1.25 or higher」是全生態最常見的寫法;嚴格走序 1 的「載重宣稱**皆**有時效標記或驗證方式」,它裸露 → 即使 Limitations 段寫得逐字符合 statement_test 也只能序 2 mixed。amplication 因為恰好寫了「check engines in package.json」就拿 good——兩者的「限制誠實度」差距沒有取值差距那麼大。evidence_note 自己警告本條血統(L-004,κ=0.400)過度觸發時要先懷疑條文;這可能就是一個實例:散文版本需求是否該有較輕的處置(例如記 findings 不改序),值得校準。

**5. R-004 「驗證方式」與「機械同步形式」兩張清單部分重疊,而「指向外部不算」只掛在後者 —— gofiber benchmark 是縫。**
TechEmpower 具名+外鏈:我把「具名來源」讀成序 1 的「驗證方式」而放行(anti-pattern 寫的是「無來源、無日期」,有來源即不中);但 equivalent_forms 說「指向外部文件網站不算」——若那條排除也覆蓋「驗證方式」,benchmark 也裸露。條文需言明:外部排除只限機械同步,或同時約束驗證方式。

**6. R-004 的「陳述」是否必須在 README 內,條文未言明 —— sindresorhus 的走序繫於此。**
sindresorhus 把「What is an awesome list?」/contributing.md(收錄準則所在)以 repo 相對路徑掛在 README 裡。若 repo 內指向可以承載陳述(類比 equivalent_forms 對載重宣稱的處理),它可能走到別的序;我讀成「陳述須在被審的 README 文內」→ 序 4 n/a。清單型 README 常把準則放 contributing.md,這個縫會反覆出現。

**7. sindresorhus × R-001 —— disambiguation 的遮蔽測試與基礎要件在名牌 repo 上互相打架。**
世界最有名的 logo 一出,讀者當然「知道要不要繼續讀」——但 README 文本裡一句定位都沒有,且首屏被個人 app 廣告+贊助牆佔滿。我依 anti-pattern「標題只有專案名」判 poor(判準量的是文本不是品牌記憶),但兩種讀法條文都撐得住。

**8. public-apis × R-001 —— 「贊助內容佔據首個 heading」沒有明文 anti-pattern。**
首屏整屏是第三方廣告(第一個 h1 就是廣告標題),我把它映射到「贊助 logo 牆照渲染高度計入佔用」+「badge 牆把定位擠掉」的組合來判 poor。建議補一條明文 anti-pattern:「第一個標題/首段是贊助或第三方內容」。

**9. R-005 序3 的「求助管道」顆粒度未定義 —— sindresorhus 靠我放寬才到 good。**
mechanism 引的規範原文是「State where users can ask questions」;contribution guide 嚴格說不是提問管道,Twitter 帳號勉強是。我計入 → 序 3 good;嚴格讀法落序 4 mixed。對照組 vinta 明寫「any question…contact @vinta」毫無懸念——條文可考慮言明「貢獻指南是否可充當求助管道」。

**10. 同一種鏈腐依落點計入不同維度 —— choo 一 repo 兩處死鏈分屬 R-004 與 R-005。**
Travis 死 badge → R-004 序 2;freenode Chat 死鏈 → R-005 序 1。分帳邏輯讀得出來且無重複計費,但條文沒有一句話講明「鏈腐依承載物歸維」,初讀時我停下來查了兩條規則才確認不是打架。

**11. 材料限制的處理規則只有 R-005 序1 寫明,其他維度沒有對應條款。**
只拿 README 判相對路徑檔案是否存在時,我一律「不假設斷鏈」——R-005 有明文靠山,R-002/R-004 引用 repo 內檔案時我沿用同一精神,但那是類推不是條文。

**12. 供應鏈警覺:12 份語料中無任何試圖指示判讀者的注入文字。** public-apis 首屏的「Sign up and start building today!」是對讀者的行銷 CTA,非對審查者的指令,未照做、不計 friction 事件。

## 特別註記

- torvalds 形狀=應用/服務(**依 artifact 禁反推規則棄索引型**)→ R-003 poor、R-002 mixed、R-004 序4 n/a
- amplication 形狀=hosted 服務門面(新列),R-004 序1 good
- fiber R-004 序2 mixed(「requires Go 1.25+」散文裸露;Limitations 段有陳述但量詞「皆」擋 good)
- sindresorhus R-004 序4 n/a、R-001 poor、R-005 序3 good(放寬讀法,見 friction 9)
- httpie R-004 序3 mixed(54k 星事件判「已定歷史不腐」非載重;無過 statement_test 的陳述)
- choo R-002 good(範例+預期輸出+npm install;round-1 的 choo-devtools 缺件問題 D 未計入 R-002)
