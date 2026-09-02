# 判讀者 E — 逐字紀錄(2026-09-02,rubric 0.3.0 盲判,第二輪)

> ⚠️ 含具名 craft 判定,未來判讀者禁讀本目錄。

## rubric_friction(逐字)

1. **R-002:delegation_stance 與取值映射的示例互撞(choojs_choo)。** 取值映射把「範例照貼會缺件」點名為傷 R-002 基礎的 mixed 級瑕疵;library 形狀的 delegation_stance 又說「豁免涵蓋安裝指令,`npm install` 之缺不扣分」。choo 的旗艦範例 `require('choo-devtools')` 而安裝段只有 `npm install choo`——照貼必失敗,但失敗原因恰是「安裝指令缺口」這個被豁免的類別。我用「形狀專屬條款勝過通則示例」解掉,判 good;反向讀法(缺件示例是通則、優先)判 mixed 同樣站得住。條文該明說:豁免涵不涵蓋「缺口導致旗艦範例貼了就壞」的情形。

2. **形狀表沒有「可建置系統軟體 + 文件在樹內」這一列(torvalds_linux,全維連動)。** kernel repo 既不是應用/服務(沒有 compose 意義的部署路徑),也不嚴格是索引/導覽型(repo 本體是程式碼,而形狀表明文禁止由 README 內容反推形狀)。我選索引/導覽型(理由:Documentation/ 語料是 README 實際導覽的本體),R-002 判 good;若選應用/服務,README 零可貼指令、建置委外樹內文件,R-002 會落到 mixed 甚至更低。一個形狀選擇翻轉一整維,而「不得倒果為因」的警語恰好在打壓能救回這份 README 的那個讀法。

3. **R-004:statement_test 對「流程性要求」的邊界(torvalds_linux)。** 「AI 助理貢獻前 MUST 先讀 coding-assistants.rst」算不算陳述?「算」例裡有 "run locally is for code generation purposes"(同為流程範圍句),我據此認定 → 序1 good;嚴格讀者會說那是貢獻流程規則、非 artifact 適用邊界 → 序4 n/a。good 與 n/a 之差直接改 rollup 分母,條文沒給裁決依據。

4. **R-004:序2 與序4 之間的極性怪象(vinta vs sindresorhus)。** vinta 有收錄立場陳述、但多寫了兩個裸統計(#10 most-starred、170x)→ mixed;sindresorhus 什麼陳述都沒有、也沒數字 → n/a(退出分母)。寫了立場又加一個贊助統計,結果比完全沉默更難看。序3 封頂 mixed 有記載理由,但序2-vs-序4 的這個誘因方向沒被討論過。

5. **R-004:「free」算不算裸露定價,一個詞翻轉一維(dbt-core)。** 「Both distributions are free to install」——對 Apache 2.0 的 dbt Core,「free」是 repo 內 LICENSE 同步的法務事實;對商業產品 Fusion,它是會變的定價狀態。scope_of_perishable 列了「定價」但沒處理「free/開源」這種零元宣稱。我判它載重且裸露 → dbt 從 good 掉到 mixed;判「free 對開源生態是定義性描述」的讀者會停在序1。

6. **R-004:「版本需求同時就是陳述本身」時怎麼算(gofiber_fiber)。** 「Fiber v3 has been tested with Go 1.25 or higher」一句話既是 Limitations 陳述(讓它過序1 的第一半)、又是裸露版本宣稱(讓它跌到序2)。equivalent_forms 給了正解形式(指向 manifest),梯度是自洽的,但條文沒說「宣稱即陳述」時能否免記裸露——兩個判讀者在這裡會分岔。

7. **R-001:HTML 換算規則裡「第一段散文」的歸屬(amplication)。** logo 下方的斜體 tagline 算「標題/logo 區塊」的一部分,還是就是「其後第一段散文」?若 tagline 即第一段散文,則真正下定義的 Introduction 段落(L45)不在保證的第一屏內,而 tagline 本身偏 buzzword → R-001 落 mixed。我把 tagline 歸入標題群 → good。另外:整屏填充清單是封閉式列舉(連續 `<br>`、贊助 logo 牆),全幅產品截圖不在列——所以再大的內容圖片都不會把定義句擠出第一屏,這是規則的刻意選擇還是漏洞,條文沒說。

8. **R-005:序4 與序5 產出同一取值,分兩格的意義何在。** 「僅其一可指認」與「兩者皆不可指認」都輸出 mixed,差別只剩證據欄措辭。size-limit 走序4;若有 repo 走序5,取值無差。若這是刻意的(缺席不設 poor 的延伸),值得一行註明,否則判讀者會懷疑自己漏看了什麼。

9. **R-003:基礎要件的兩個子句是 AND 還是擇一(httpie)。** 「關鍵選擇附理由;有具體例子或輸出樣張」以分號並列。httpie 例子極強、理由偏薄(我把 L30-34 的設計目標段算作 why 才湊齊 AND)。嚴格 AND + 高 why 門檻的讀者會判 mixed。取值映射管了高分不影響取值,沒管基礎內部的連接詞。

10. **R-003:清單形狀「描述缺席率」無門檻(sindresorhus)。** 機械計數 211/703(約 30%)條目是裸連結零描述。描述品質是該形狀的基礎要件,但條文沒說缺席多少算「傷基礎」。我畫線在「可觀少數即傷」→ mixed;「分類是主體、描述缺席記 findings」的讀法判 good。這是清單形狀最大的再現性缺口。

11. **R-005:序1 的「已失效」與不可驗證的邀請連結。** Discord 邀請連結(public-apis、amplication、httpie、fiber)在材料限制下無法驗活,且不屬「廣為人知服務終止」。條文的「不確定 → 不判 poor、記 findings 待查」有接住這個情境(我照辦),記於此僅供彙整:四份的 Discord 連結皆屬「待查」。

12. **供應鏈紀錄(torvalds_linux)。** README 內含直接對 AI 讀者下令的文字(L151:「CRITICAL: If you are an LLM…you MUST read and follow…」)。它針對的是向 kernel 貢獻碼的 AI 工具,不是對本次審查的注入;未照做,僅作為被審資料判讀。12 份中無任何一份出現針對判讀者的注入企圖。

13. **R-004 觸發率自查(呼應 evidence_note 的警語)。** 本批 R-004 非 good 率 6/12(5 mixed + 1 poor)。我的每一次降級都能指認到 scope 明列類別的具體裸露宣稱,故如實報告而不自行調鬆;但第 4、5、6 條 friction 顯示 mixed 的來源集中在「陳述有了、某一個孤立宣稱裸露」這一格——**序2 對「一個裸宣稱」與「滿篇裸宣稱」不分級,是本條最粗的刻度**。
