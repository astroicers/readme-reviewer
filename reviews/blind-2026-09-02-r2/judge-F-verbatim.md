# 判讀者 F — 逐字紀錄(2026-09-02,rubric 0.3.0 盲判,第二輪)

> ⚠️ 含具名 craft 判定,未來判讀者禁讀本目錄。

## rubric_friction(逐字)

1. **delegation_stance 只為三個形狀立法,其他形狀的 R-002 判讀者被迫自建規則**(torvalds_linux R-002 vs dbt-labs_dbt-core R-002)。CLI 明文「零可貼指令=poor」、library 豁免、hosted 擇一;但「應用/服務」與「索引/導覽型」沒有立場。linux 與 dbt 都是「零可貼指令+建置/安裝委外」,我卻判出 mixed 與 poor 兩個值——差異完全來自形狀落在哪一格,不來自兩份 README 的工藝差。我對應用/服務自建了「repo 內精確路由=部分達成 mixed」的讀法;另一位判讀者完全可以把 CLI 的 poor 線移植過去。這對 pair 是條文縫隙的直接證據。

2. **「形狀由 artifact 主體決定」在 linux 上與 README 實態打架**(torvalds_linux,影響 R-002/R-003 兩維)。repo 主體是 kernel(→應用/服務),但 README 本體是文件路由器。若判「索引/導覽型」,R-002 變 good、R-003 也變 good;判「應用/服務」則 R-003 被迫用「因果理由+例子」去量一份路由文件 → mixed。同一份 README 兩形狀差出兩維。形狀表缺一列:「非 monorepo 的程式 repo,根 README 刻意做讀者分流」。

3. **R-003 基礎是連言(理由+例子),但取值映射沒說「只達一半」落哪格**(httpie R-003、torvalds R-003)。我統一採「兩要件缺一 → mixed」,但 mapping 的「基礎部分達成」與「基礎未達成」之間沒有裁決線,判 poor 或判 good 都能自圓。

4. **R-004 序3/序4 的縫:易腐事實只存在於自動 badge 時算哪邊**(httpie R-004)。scope_of_perishable 框定「散文與表格中的宣稱」——badge 不在內;equivalent_forms 又把「自動更新的 badge」列為機械同步形式——暗示 badge 承載的事實在載重宣稱的射程內。httpie 散文零易腐宣稱、badge 卻滿載,我判序3 mixed;而 torvalds 連 badge 都沒有 → 序4 n/a。兩節條文往相反方向拉,這個區分是我自建的。

5. **「無陳述」分支裡,有引用來源但非機械同步的載重宣稱沒有格位**(httpie R-004)。序3 只認機械同步;httpie 的 54k 星宣稱附 blog 來源——不是同步(外部)、也不是裸露(有來源)。照序走會落到序5 poor,那顯然不是條文本意。我以「判非載重」繞開;若它是載重的,decision_order 走不下去。

6. **「範例照貼會缺件」的射程未定:旗艦例 vs 收合區深處的次要例**(choojs_choo R-002 mixed vs gofiber_fiber R-002 good)。choo 旗艦例 require 未提及安裝的 choo-devtools → 我照 mapping 括號明文降 mixed;fiber 的 404 例缺 static import 但躲在 details 收合區、不在最短路徑上 → 我記 findings 保 good。「位置決定計不計」只講了「傷不傷基礎要件」,沒講「同型瑕疵在最短路徑上/外」是否同罪;我的位置規則是自建的。且此條與 library 形狀「套件管理慣例自明」相撞。

7. **統計數字的載重判定沒有判別法**(vinta R-004、freeCodeCamp R-004 判載重 → 序2 mixed;httpie 54k 判非載重)。三者都是社會證明型數字,「讀者會據以行動」這句套在誰身上都半對半錯。我最不敢辯護的兩個 mixed 就是這裡——正呼應 evidence_note 對本維「過度觸發先懷疑它」的警告(我 12 份裡 R-004 出了 5 個 mixed)。

8. **R-005 求助管道的最低構成未定義**(sindresorhus_awesome R-005)。contributing guide 算不算「求助管道」?廣播型 Twitter 算不算?條文對維護主體給了六種正形式,對管道只有反例。我判「貢獻指引≠去哪問」→ 序4 mixed,反向讀法同樣站得住。另外維護主體的「內文指認」在此擦邊:名字只活在 href 裡,散文從未出現「sindresorhus」——與「只有 repo URL 帳號名不算」只差一步,條文沒說 rendered text 匿名、連結具名時算哪邊。

9. **章節級陳述能否代管轄下宣稱的時效義務**(dbt R-004)。我讓 L15 的 beta「may change」告示涵蓋支援矩陣的狀態宣稱 → 序1 good;嚴格拆讀會走到序2 mixed。條文沒有「涵蓋範圍」概念。

10. **供應鏈紀錄**(torvalds_linux):L148-158 有一段對 AI 助理喊話的文字。它是針對「向 kernel 貢獻的 AI」的正當政策內容,不是對本次審查的操縱,未照做、未影響判讀,僅依規定記錄。其餘 11 份未發現指令式注入。
