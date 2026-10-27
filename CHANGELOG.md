# 📝 江夏傳統整復推拿 板橋館｜專案版本更新紀錄 (CHANGELOG)

本文檔記錄「江夏傳統整復推拿 板橋館」AI 客服機器人、Prompt 集中倉庫與自動化工具的所有版本演進、功能修復與 Git 變更紀錄。

## 📌 [v2.5.4] - 2026-10-27 15:20:00
### 🔗 解決「後台看板手動連結 LINE 好友成功，但後續推播通知未連上」之雙端漏洞
- **根本原因**：
  1. **LINE 生態與暱稱落差**：LINE 官方 API 只回傳用戶個人原始暱稱（如「鳳蘭」），店家在 OA 後台手動更改的自定義名稱（如「呂鳳蘭-0933828681」）無法被 API 獲取。
  2. **看板自定義輸入比對過嚴，未賦值 userId**：在 `booking-dashboard/index.html` 方式二中，輸入「呂鳳蘭-0933828681」時因嚴格相等比對失敗，降級執行且 `userId` 給予空字串，僅寫入 `[LINE_DISPLAY_NAME:...]` 標籤並彈出成功 Toast，造成「手動連結已成功」的假象。
  3. **後端反查子字串包含方向相反 (`includes`)**：在 `line_server.js` 的 `lookupLineUserIdByPhoneOrName` 中，`"鳳蘭".includes("呂鳳蘭-0933828681")` 與 `"鳳蘭".includes("呂鳳蘭")` 永遠回傳 `false`，導致無法從日曆標籤反查回 `Ud6576ff03f27105f05ded1e644689fb4`，因而判定無 LINE 帳號而跳過推播。
- **修復方案**：
  1. **後端雙向模糊比對與符號清洗**：升級 `line_server.js` 中的 `lookupLineUserIdByPhoneOrName`，支援去除電話與符號清洗，實裝雙向包含與重疊字比對（「呂鳳蘭-0933828681」可自動匹配「鳳蘭」）。
  2. **前端好友搜尋與自定義輸入智慧匹配**：升級 `booking-dashboard/index.html`，支援好友搜尋雙向模糊篩選；自定義輸入時若能近似匹配好友名冊（如輸入「呂鳳蘭」自動匹配「鳳蘭」），自動提取並賦值真實 `LINE_USER_ID`；若完全無符合對象，顯式彈出警示 Toast，杜絕虛假綁定。
  3. **日曆好友名冊立即校正**：直接於 Google 日曆 `【系統同步】LINE好友名冊_勿刪` 中將「鳳蘭 (`Ud6576ff03f27105f05ded1e644689fb4`)」補正綁定真實姓名「呂鳳蘭」與電話「0933828681」。
- **Git Commit**：`azach258/my-line-bot` (`4e6811e`)、`azach258/jiangxia-banqiao` (`cf73896` / `eb2d35f`)

## 📌 [v2.5.3] - 2026-10-22 15:21:00
### 🛡️ 修復 AI 預約調用 ookEvent 時 endTime 格式不完整導致崩潰報錯「日曆系統連線異常」之漏洞
- **根本原因**：
  當 Gemini AI 模型在對話中調用 ookEvent 時，若傳入的 endTime 為空字串、純時間格式（如 17:00）或帶空格格式（如 2026-10-23 17:00:00），未標準化為帶 T 的 ISO 格式，後續在執行 endTime.split("T")[1] 時直接引發 TypeError: Cannot read properties of undefined (reading 'split') 拋出例外，觸發 Prompt 兜底話術「目前日曆系統連線有些異常」。
- **修復方案**：
  1. 在 ookEvent 內對 startTime 與 endTime 實裝格式清洗與補位防護（支援自動將空格轉 T、純時間補日期、缺秒數自動補 :00）。
  2. 若 endTime 格式非標準日期字串，一律自動改以 startTime 往後推算 1 小時補全，徹底杜絕 undefined 切割崩潰。
  3. 全面對 split("T") 與 split(":") 加上安全鏈與預設值備援。
- **Git Commit**：zach258/my-line-bot (53a2912)
## 📌 [v2.5.0] - 2026-10-21 15:35:00
### 🔗 新增「方法 B：後台排程看板主動連結 LINE@ 好友」＆「雲端 LINE 好友名冊自動同步機制」
- **核心升級與解決問題**：
  1. **解決「老客戶已加過 LINE@ 好友，但未在 LINE 留過電話，師傅想直接從後台主動幫客戶綁定 LINE 帳號」之需求**：
     - 雖然 LINE 官方 API 禁止直接用「手機號碼」硬查未互動陌生人的 LINE，但只要客戶**曾經加入過店裡 LINE@ 好友（或傳過貼圖、問過問題）**，後台現在支援由師傅**主動從排程看板一鍵點選配對**！
  2. **排程看板「預約詳情彈窗」新增【🔗 連結 LINE@】主動配對面板 (ooking-dashboard/index.html)**：
     - 點開任何一筆預約詳情時，客戶資訊卡會即時顯示 🟢 已連結 LINE@ (...) 或 ⚪ 未連結 LINE@ 狀態徽章與 **「🔗 連結 LINE@」** 按鈕。
     - 點擊「🔗 連結 LINE@」展開配對面板，提供雙模式主動綁定：
       - **方式一（從已互動 LINE@ 好友清單一鍵選取）**：直接列出所有曾加過 LINE@ 好友的客戶名單（含 LINE 顯示暱稱、曾留姓名與電話），支援關鍵字即時篩選，點一下即可將該 LINE 帳號 LINE_USER_ID 綁定至該筆預約與客戶電話。
       - **方式二（直接輸入客戶 LINE 顯示名稱或 ID）**：若師傅在 LINE Official Account Manager 後台看到客戶的 LINE 暱稱（例如 Amy、陳先生），直接輸入並按「綁定」，系統即寫入 [LINE_DISPLAY_NAME:XXX] 至雲端日曆，由 LINE 伺服器自動比對 LINE 暱稱並升級為永久 LINE_USER_ID 綁定！
  3. **LINE 伺服器 ⇄ Google 日曆「雲端 LINE 好友名冊」自動同步橋樑 (line_server.js)**：
     - 新增 syncLineFriendsToCalendar()：每當有客戶新加入 LINE 好友 (ollow)、傳貼圖 (sticker)、傳圖片或發訊息時，自動抓取其 lineDisplayName，並將所有已知 LINE@ 好友名冊同步至 Google 日曆隱藏系統事件 【系統同步】LINE好友名冊_勿刪（排定於未來週日 05:00~05:15 凌晨時段，不佔用營業空檔且免改動 GAS 後端即可讓排程看板秒讀）。
     - 升級 cleanNoteText() 與 saveDetailChanges()：確保前端調理備註乾淨不顯示底層 [LINE_USER_ID:...] 標籤，同時在師傅修改備註並儲存時 100% 自動保留綁定標籤不遺失。
- **Git Commit**：zach258/my-line-bot (1bf2e8)
## 📌 [v2.4.0] - 2026-10-20 20:17:00
### 📱 新增「未綁定 LINE 客戶雙軌簡訊提醒系統（方案一：Telegram/看板一鍵喚起手機原生簡訊 ＆ 方案二：全自動商用簡訊 API 接口）」＋「新加好友/貼圖/手機末三碼自動認親」
- **核心升級與解決問題**：
  1. **解決「後台排程／官網預約客戶未綁定 LINE 帳號」之提醒斷點**：當客戶由師傅於後台看板手動建檔或官網填表、尚未在 LINE 留過電話時，系統無法發送 LINE 通知。現新增「雙軌簡訊兜底機制」，確保 100% 不漏接任何一位預約客。
  2. **方案一（0 元立即可用・Telegram 與排程看板「一鍵喚起手機簡訊 (`sms:`)」按鈕）**：
     - 在每日 20:00 與 09:00 發送給師傅的 Telegram 報表中，針對每一位「⚠️ 尚未綁定 LINE 帳號」之客戶，直接生成 **【📲 點此一鍵喚起手機簡訊發給 XXX】** 專屬按鈕與一鍵點擊複製之 65 字精簡簡訊。
     - 點擊按鈕後，透過看板 `?quick_sms=1` 橋樑於 **0.1 秒內自動喚起 iPhone/Android 內建簡訊 App**，自動填好收件電話與 65 字提醒文案（嚴守台灣單則 70 字計費上限、純文字地址防電信商攔截），按「傳送」即完成提醒。
     - 同步於師傅排程看板（`booking-dashboard/index.html`）的「預約詳情彈窗」新增翠綠色 **「📲 簡訊提醒」** 按鈕（`sendSmsFromDetail`），隨時可手動一鍵發簡訊。
  3. **方案二（100% 全自動無人值守・商用簡訊 API 雙向接口 `sendSmsViaApi`）**：
     - 內建支援台灣主流 **Every8D (互動資通)**、**Mitake (三竹簡訊)**、**Twilio** 與自訂 **SMS Webhook**，只需於 Zeabur 設定環境變數帳密，系統即自動對無 LINE 帳號之客戶發送簡訊並寫入防重鎖。
  4. **新加 LINE 好友 (`follow`)、傳貼圖 (`sticker`) 與手機末 3 碼自動認親**：
     - 客戶新加入 LINE 好友或傳貼圖時，自動讀取其 LINE 顯示暱稱 (`lineDisplayName`) 比對未來 30 天 Google 日曆，同名者直接 1 秒自動綁定 `LINE_USER_ID` 並回寫日曆；亦支援客戶直接輸入手機末 3 碼快速認親。
- **Git Commit**：`azach258/my-line-bot` (`e9c7531`)、`azach258/jiangxia-banqiao` (`cc8d6ff`)

## 📌 [v2.3.0] - 2026-10-19 18:35:00
### 🚀 新增「客戶永久識別與本人預約預載查詢」＆「LINE 預約前一天 20:00 主動提醒＋當日 09:00 晚鳥補漏雙引擎」
- **核心升級與修復問題**：
  1. **解決超過 14 天回訪客戶「客服失憶」漏洞**：原本 `line_server.js` 的 `getSession(userId)` 設有 14 天過期機制，會在清除對話 `history` 時連同客戶 `profile`（姓名、電話）一併洗掉；且 Render 雲端重啟時會遺失本地記憶體。
  2. **解決跨管道預約（官網網頁預約／師傅後台排程）電話破折號格式斷鏈**：官網與 GAS 日曆寫入電話為 `0912-345-678`（含破折號），而 LINE 機器人原本僅比對純數字或 `LINE_USER_ID`，導致官網預約客戶進 LINE 查不到本人預約、也收不到提醒。
  3. **解決客戶進場未預載預約導致「重複詢問姓名電話」或「忘記已預約過」**：原本機器人只有在客戶明確觸發工具時才查日曆，導致已預約客戶進來發問時，AI 不知道客戶已有未來有效預約。
  4. **修復原提醒排程「台中大墩十街錯誤地址」與「單一早上 09:00 提醒太晚」問題**：原 `runMorningReminders` 內殘留台中館地址（`台中市南屯區大墩十街177號`），且僅在當日 09:00 發送，若客戶前一天臨時有事無法提前一天改期釋出空檔。
- **解決方案與架構實裝**：
  1. **永久客戶識別綁定庫 (`data/customer_bindings.json` + 雲端日曆自癒啟動 `bootstrapBindingsFromCalendar`)**：
     - 建立 `byUserId` 與 `byPhone` 雙向永久索引，並在 `getSession` 中確保超過 14 天僅清理舊對話 `history`，100% 永久保留客戶 `profile`（姓名、電話、LINE 暱稱與調理備註）。
     - 伺服器啟動時自動掃描 Google 日曆過去 90 天至未來 60 天行程，從日曆重建 `LINE_USER_ID ⇄ 姓名/電話` 綁定，免疫容器重啟失憶。
  2. **跨管道電話正規化與日曆自動回寫 (`normalizePhone` & `patchEventWithLineUserId`)**：
     - 實裝 `normalizePhone()` 統一剝除破折號與空白（支援完整手機號碼與電話末三碼比對）。
     - 當官網或電話預約客戶首次在 LINE 詢問或貼上官網 `【預約明細】` 時，`findCustomerBooking` 即時比對成功並自動將 `LINE_USER_ID:<userId>` 回寫烙印至 Google 日曆事件 Description。
  3. **進場零延遲自動預載本人預約 (`scanCustomerActiveBookings`)**：
     - 客戶發送任何 LINE 訊息進場時，後端自動預掃描該客戶未來 30 天內的 Google 日曆有效預約，並注入 System Prompt 頂部 `【系統即時日曆核實之未來有效預約】`。
     - 客戶詢問「我約幾點？」時免留資料秒答；已預約客戶若又說「我想預約」，機器人主動提醒現有預約時段，詢問是要改期還是幫親友加約。
  4. **雙階段防爽約 LINE 提醒引擎 (`runDayBeforeReminders` @ 20:00 + `runMorningReminders` @ 09:00)**：
     - **第一階段（前一天晚上 20:00 主力提醒）**：自動掃描「明天」所有預約，透過 `LINE_USER_ID` 或 `lookupLineUserIdByPhoneOrName()` 跨管道反查發送提醒，更正為板橋館正確地址（`新北市板橋區館前西路152之1號1樓` + Google Maps 導航）。
     - **第二階段（當日早上 09:00 晚鳥補漏提醒 - 方案 A）**：僅針對昨晚 20:00 之後才臨時預約今日時段、尚未收到提醒的客戶補發，透過 `data/reminders_log.json` 與日曆 `[LINE提醒已發送:YYYY-MM-DD]` 雙重防重鎖，絕不重複打擾已提醒客戶。
     - **改期自動重置提醒標籤**：更新 `Code.gs` 與 `gas_calendar_api.js` 之 `handleUpdateBookingTime`，改期時自動清除舊日期的 `[LINE提醒已發送:...]` 標記，確保新預約日期前一天 20:00 能再次準時提醒。

## 📌 [v2.2.2] - 2026-10-14 19:55:00
### 🛡️ 徹底修復變更服務內容與金額後「過一下又跳回編輯前舊資料」之背景輪詢覆寫漏洞 (Custom Edit Guard & Cloud Bi-directional Sync)
- **修復問題**：
  在後台排程看板點選預約詳情，變更調理方案（例如由免費評估切換為自費調理，或調整部位）與應收金額並儲存後，等待約 20 秒以內（「過一下」），畫面與資料又自動跳回編輯前的舊方案與舊金額。
- **根本原因**：
  1. **背景 20 秒無感輪詢機制 (`_cloudPollTimer`)**：系統每 20 秒自動執行 `fetchFromCloud(true)` 向 Google Apps Script 拉取最新雲端日曆行程。
  2. **本地物件缺乏方案與金額保護標記**：師傅手動點擊方案按鈕（`selectDetailService`）或修改金額（`saveDetailChanges`）時，系統僅將變更寫入 `localStorage`，未標記手動保護標籤（對比備忘欄位有 `_customEdited`，方案與金額完全無防沖洗旗標）。
  3. **雲端合流無條件覆蓋（Overriding Loop）**：在 `fetchFromCloud()` 迴圈中，系統執行 `exists.serviceItem = evt.serviceItem || exists.serviceItem;`。由於 Google 日曆上仍留存原本的預約項目字串，每次輪詢皆將師傅剛改好的方案強制替換回日曆舊值；若舊值包含「免費/評估」，更連帶觸發 `exists.price = 0; exists.isCustomPrice = false;`，將師傅改好的金額直接歸零！
  4. **缺乏方案與金額之雙向雲端推播**：修改時段（`updateBookingTime`）與備忘（`updateNotes`）皆有發送遠端 API，但方案與金額修改時未推播至 Google 日曆與試算表，導致日曆永遠維持舊資料。
- **解決方案**：
  1. **實裝方案與金額防沖洗雙保護守衛 (`_customServiceEdited` & `_customPriceEdited`)**：
     - 在 `selectDetailService`、`onDetailPriceChanged`、`saveDetailChanges` 統一設置保護標記。
     - 在 `fetchFromCloud()` 中加入嚴格防禦：若 `exists._customServiceEdited === true`，絕不被雲端舊項目覆寫；若 `exists._customPriceEdited === true` 或 `exists.isCustomPrice === true`，100% 豁免雲端歸零邏輯，守護師傅設定之真實金額。
  2. **實裝雲端方案與金額雙向推播引擎 (`syncServiceChangeToCloud`)**：
     - 點擊方案或儲存變更時，自動非同步推播 `action: 'updateService'` 至 Google Apps Script。
  3. **GAS 雲端橋樑全面升級支援 `updateService`**：
     - 在 `google_apps_script/Code.gs` 與 `gas_calendar_api.js` 中新增 `handleUpdateService`，即時同步更新 Google 日曆 Description 中的 `預約項目`、`應收金額` 與 `調理部位`，並同步修訂 Google 試算表 `預約紀錄名冊`。
     - `getEvents` 擴充支援解析日曆描述中的 `應收金額`，達成全平台單一真相源 (SSOT) 雙向閉環。
  4. **全端語法與單元測試校驗**：
     - 通過 Node.js 腳本語法檢測與輪詢抗沖洗單元測試，並完成 GitHub Pages 發布。

## 📌 [v2.2.1] - 2026-10-13 15:45:00
### 🛡️ 徹底修復歷史就診紀錄（如 10/2）儲存後重新整理 (F5) 消失之雙向同步刪除過濾盲區 (Query Window Safety Guard)
- **修復問題**：
  在後台排程看板輸入過去的就診紀錄（例如 10/2 預約），儲存時有顯示紀錄，但瀏覽器一旦重新整理 (F5)，該筆 10/2 客戶紀錄便徹底消失；重複輸入同一個客戶資料亦會重複發生消失現象（而 10/1 初始假資料則不受影響）。
- **根本原因**：
  1. **GAS 雲端查詢區間過窄**：`google_apps_script/Code.gs` 與 `gas_calendar_api.js` 之 `getEvents` 舊代碼硬編碼只抓取過去 3 天至未來 30 天（`now - 3 days` 到 `now + 30 days`）。以系統當前日期 10/13 為基準，查詢起點為 10/10，任何早於 10/10 的歷史行程（包括 10/2）均不在雲端日曆回傳資料中。
  2. **雙向刪除過濾器缺乏時間視窗安全守衛**：看板在 `fetchFromCloud()` 執行與 Google 日曆雙向刪除對齊時，直接以 `if (b.cloudSyncedId && !cloudIds.has(b.cloudSyncedId)) return false;` 判斷本地預約是否已被雲端刪除，**未核對該行程之時間是否屬於本次雲端查詢的時間範圍**。
  3. **抹除連鎖反應**：使用者登入 10/2 資料時，前端成功將預約推播至 Google 日曆並獲取 `cloudSyncedId` 寫入本地 `localStorage`；但在重新整理 (F5) 時，`fetchFromCloud()` 收到僅含 10/10 以後資料的 `result.data`，過濾器誤判「雲端已無此 10/2 行程，代表師傅已在日曆上刪除」，強行從 `this.bookings` 剔除並覆寫 `localStorage`，導致歷史紀錄永久丟失。而 10/1 剛好屬於初始假資料無 `cloudSyncedId`，因而未觸發該過濾條件。
- **解決方案**：
  1. **前端實裝時間視窗安全守衛 (`Query Window Safety Guard`)**：
     - 在 `fetchFromCloud()` 中解析查詢區間（`cloudQueryStart` ~ `cloudQueryEnd`），**只有當預約時間明確落在本次雲端查詢視窗內時**，雲端找不到該 ID 才判定為被日曆手動刪除。
     - 凡是落在查詢視窗外的所有歷史舊帳或超遠期預約，100% 豁免核對，絕不誤刪！
  2. **GAS 雲端 API 查詢範圍擴增至 365 天**：
     - `google_apps_script/Code.gs` 與 `booking-dashboard/gas_calendar_api.js` 之 `getEvents` 預設查詢範圍擴大為過去 365 天（一年）至未來 180 天（半年），並支援前端傳入 `startTime` 與 `endTime` 自訂區間，回傳標準 `queryStartTime` 與 `queryEndTime`。
  3. **ID 雙向容錯去重比對**：
     - `cloudIds` Set 同時收錄含 `@google.com` 與去除後之純 ID；並在 `exists` 比對時納入純 ID 與時間+號碼匹配，徹底免疫 ID 格式差異。
  4. **全端測試與雙倉庫自動同步部署**：
     - 通過 Node.js 語法校驗與 3 大情境單元測試（舊版 GAS 兼容、新版 GAS 覆蓋、真實日曆手動刪除連動），並完成 GitHub Pages 部署。

## 📌 [v2.2.0] - 2026-10-13 15:25:00
### 🛠️ 徹底修復「免費檢查評估」金額無法更改為 0、短路運算回退 1500 與歷史快取自動自我校正 (Auto-Heal)
- **修復問題**：
  1. 調理方案／部位顯示為「【免費】檢查評估諮詢」或「免費檢查評估」，但其預約應收金額始終為 $1,500，無法正確儲存或更新為 $0。
  2. 師傅在預約詳情彈窗點選「【免費】評估 ($0)」按鈕時，受限於自訂價格防呆機制（`isCustomPrice`），系統彈出保留自訂金額並強行維持 1500 元。
  3. 官網線上自主預約前台初始變數與 radio 選項脫鉤，若訪客未手動切換項目直接送出，金額被賦予預設旗艦價 1500。
  4. 歷史快取資料庫（localStorage）中已儲存了過去誤記為 1500 的免費預約紀錄，無法自動校正。
- **根本原因**：
  1. **短路邏輯 Bug**：JavaScript 判斷 `b.price ? b.price : 1500` 或 `b.price || 1500`，因 `0` 為 Falsy，導致 $0 被強制回退為預設 $1,500。
  2. **自訂價格鎖定攔截**：`selectDetailService` 在 `isCustomPrice = true` 時直接跳過金額更新，導致點擊免費方案按鈕無效。
  3. **方案名稱模糊匹配限制**：舊代碼在比對「免費檢查評估」與「【免費】檢查評估諮詢」時因特殊括號 `【】` 導致匹配失敗，無法正確高亮按鈕與帶入 $0。
  4. **缺乏開機自動自我校正機制**：`initStorage()` 載入既有快取時未針對「免費方案但金額為 1500」的歷史異常數據進行主動修復。
- **解決方案**：
  1. **實裝全域智慧定價引擎 (`getServiceDefaultPrice`)**：凡項目包含「免費/評估/諮詢」者，預設標準金額一律為 0 元，徹底移除寫死 1500 的回退。
  2. **實裝開機自動自我修復 (`initStorage` Auto-Heal)**：系統初始化載入快取時，自動掃描並將所有調理項目為免費檢查評估、但金額曾誤記為 1500 的預約，100% 自動重設為 0 元並清除鎖定。
  3. **解除方案切換攔截 (`selectDetailService`)**：只要師傅主動點擊方案按鈕（包括【免費】評估），一律無條件切換項目名稱、同步金額為 $0，並即時連動刷新時間軸與應收統計。
  4. **升級方案模糊比對演算法 (`renderDetailServiceButtons`)**：自動濾除括號與空白符號，確保各種名稱變體皆能精準高亮對應按鈕。
  5. **前台官網狀態對齊 (`JiangxiaFrontBooking`)**：修正建構子預設值為免費檢查評估（$0, 15分鐘），並於開窗時自動同步 DOM 單選狀態。
  6. **一鍵同步發布**：全站程式碼通過 Node.js 語法校驗，並已部署發布至 GitHub Pages 雙端（官網與看板）。

## 📌 [v1.5.3] - 2026-09-29 16:50:00
### 🛡️ 實裝客戶真實姓名防呆過濾器、問候語阻斷機制與改時間姓名鎖定鐵律
- **修復問題**：
  客戶傳訊「摳你吉挖 我想改時間」時，AI 出現嚴重幻覺，誤將開頭問候語當成客戶姓名，甚至在日曆上將客戶名稱竄改為「摳你吉挖」。
- **根本原因**：
  1. `extractCustomerInfo` 的姓名萃取正則過於寬鬆，缺乏問候語與動詞過濾，且長度較長即強制覆蓋既有合法姓名。
  2. `findCustomerBooking` 查獲預約時未對原登記姓名進行強制指示，導致 AI 在改時間重新預約時被客戶當前句子的問候語轉移注意力。
  3. `bookEvent` 後端未做姓名真實性校驗，對傳入的荒謬人名（問候語/動詞短語）照單全收。
- **解決方案**：
  1. **正則萃取與姓名覆蓋雙重鎖定 (`extractCustomerInfo`)**：
     - 加入常見多國語言問候語（「摳你吉挖」、「你好」、「哈囉」、「早安」等）與動詞短語嚴格黑名單，徹底阻斷問候語被辨識成人名。
     - 實裝姓名保護鎖：已有合法真實姓名時，嚴禁被對話中的較長句子隨意覆蓋。
  2. **日曆查詢結構化提煉與改時間指示 (`findCustomerBooking`)**：
     - 回傳資訊明確拆解「原登記姓名」與「電話」，並強制宣告在改時間重訂時必須 100% 沿用原姓名，嚴禁使用問候語。
  3. **後端姓名自動糾正過濾器 (`bookEvent`)**：
     - 後端攔截包含問候語或動詞的荒謬姓名，自動回退並糾正為 session profile 或 lastBooking 中留存的合法真實姓名。
  4. **提示詞與 SOP 升級 (`01_line_bot_customer_service.md` -> v1.4.7)**：
     - 明訂「客戶真實姓名防呆鐵律」與「修改時間姓名鎖定鐵律」，杜絕問候語冒充人名。

## 📌 [v1.5.2] - 2026-09-28 20:48:00
### 🛡️ 徹底根除日曆重複預約、實裝「需求提出即重抓日曆」查詢工具與多輪上下文記憶完善
- **修復問題**：
  1. 日曆出現「同一位客戶、同一時段被重複預約多次」的異常狀況。
  2. 客戶詢問預約狀態時，AI 僅依賴殘留上下文瞎猜或叫客戶再次核對，未即時反映日曆真實狀態。
  3. 多輪對話中閱讀上下文不完善，客戶已完成的預約資訊無法被 AI 完整讀取與銜接。
- **根本原因**：
  1. **後端衝突檢查與防重排他鎖缺失**：`bookEvent` 未在寫入前查詢日曆，亦無判定是否同人同時間重複寫入；且 LINE Webhook 逾時觸發重試機制時，缺乏 `webhookEventId` 去重快取，導致被執行兩次。
  2. **缺少專屬日曆即時查詢工具**：原工具只有查單天空檔的 `checkAvailability`，缺乏針對客戶查詢未來預約的 `findCustomerBooking`；且舊 Prompt 引導「優先看上下文瞎猜」。
  3. **客戶預約快取漏注入**：`userSession.profile.lastBooking` 存入後，未在 `getSystemInstruction` 中注入給 Prompt；且歷史對話缺乏精確台灣時間標籤導致跨天時空混淆。
- **解決方案**：
  1. **後端強制即時日曆衝突檢查與防重排他鎖 (`bookEvent`)**：
     - 寫入日曆前強制查詢當日行程：若同客戶同時間已預約，直接返回「您已成功預約」並阻斷重複寫入；若已被他人佔用，立即攔截時段衝突。
     - 實裝最近 10 分鐘 `processedWebhookEvents` 快取，100% 阻斷 LINE 平台重試機制的二次預約。
  2. **實裝專屬查詢工具 `findCustomerBooking` 與 SOP 升級**：
     - 支援以姓名、電話或 LINE ID 即時撈取未來 14 天日曆行程。
     - 升級 Prompt (v1.4.6)：明定只要客戶提出查詢、確認或修改需求，強制第一步調用 `findCustomerBooking` 重抓日曆！
  3. **上下文記憶與檔案注入完善**：
     - 在客戶輪廓中動態注入 `lastBooking`，讓 Gemini 清楚掌握最新預約。
     - 為對話歷史訊息附加台灣時間戳記（例 `[09/28 20:45]`），杜絕跨天誤判。
     - 晨間提醒改採標準成對歷史寫入，確保 Gemini SDK 對話鏈結構 100% 合規。

## 📌 [v1.5.1] - 2026-09-21 17:03:00
### 🧠 實裝「磁碟檔案式持久化 Session 儲存」與「多輪上下文連續記憶防跳針 SOP」
- **修復問題**：
  1. 客戶在幾天前報名或預約過，後續再次詢問「預約時間是幾點」時，因伺服器重啟或超過 2 小時快取過期，AI 丟失全部上下文記憶，退化為全新訪客。
  2. 遇到「預約」或活動關鍵字時，AI 反覆機械化詢問「是要報名 920 還是預約正常時間」，缺乏真人秘書感。
- **根本原因**：
  1. 原對話記憶僅儲存於伺服器記憶體內存 (`Map`)，容器重啟即被抹除；且內存清理時間僅設為 2 小時。
  2. 缺乏客戶輪廓（手機/姓名/備忘）萃取機制與既有預約/活動查詢專屬分流。
- **解決方案**：
  1. **磁碟持久化 Session 儲存 (Persistent File-based Session)**：
     - 在伺服器實裝 `data/sessions/<userId>.json` 檔案級持久儲存，保留至少 14 天對話記憶，徹底免疫 Docker 容器冷啟動與伺服器重啟。
     - 保留最近 10 輪完整對話（20 則訊息），深度支援多天多輪連續對話。
  2. **客戶輪廓自動辨識與提示詞動態注入**：
     - 自動從對話中正則解析客戶手機號碼、稱呼姓名與活動意圖，動態注入 `getSystemInstruction`。
     - 讓 Gemini 清楚掌握當前對象身份，嚴禁重複索取已知電話姓名。
  3. **LINE@ AI 客服提示詞升級 (`01_line_bot_customer_service.md` -> v1.4.4)**：
     - 新增「多輪上下文連續記憶與既有預約/920諮詢查詢 SOP」。
     - 嚴禁對已知意圖之客戶反覆跳針詢問「是要活動還是正常預約」，展現流暢自然的真人秘書承接感。
  4. **SSOT 同步閉環**：
     - 完成 `prompt_manager.py sync` 同步，並推送至 GitHub 遠端倉庫。

---

## 📌 [v1.5.0] - 2026-09-21 16:18:00
### 💖 9/20 總館長公益義整圓滿落幕：客服轉化 SOP 升級與過期特例邏輯清理
- **更新項目**：
  1. **LINE@ AI 客服提示詞升級 (`01_line_bot_customer_service.md` -> v1.4.3)**：
     - 將「9/20 現場抽號碼牌專屬 SOP」替換為「活動圓滿結束感謝與平日預約轉化 SOP」。
     - 客戶詢問義診/活動關鍵字時，親切致謝、告知善款造冊捐贈伊甸基金會，並主動引導預約總館長親傳賴師傅的平日服務（免費體態評估）。
  2. **活動行銷提示詞微調 (`06_event_campaign_prompts.md` -> v1.0.1)**：
     - 將活動 A 由原先的「事前預熱/名額搶訂」改版為「事後成果回顧、社會認同（捐贈伊甸）與常態平日客流承接」之社群貼文與 LINE 廣播標準範本。
  3. **LINE Bot 伺服器代碼清理 (`line_server.js`)**：
     - 移除 `dateFormatted === "2026-09-20"` 之過期特例分支，恢復單純之六日公休防呆攔截機制，清除技術債。
  4. **SSOT 同步閉環 (`prompt_manager.py`)**：
     - 完成 Git 自動提交與一鍵同步至 `10_Antigravity_Workspace/meta/prompts/line_bot_prompt.md`。

---

## 📌 [v1.4.9] - 2026-09-14 16:56:00
### 🌐 徹底根除雲端 Docker UTC 時區差導致「星期一被誤判為星期日」的重大缺陷
- **修復問題**：
  在雲端 (Zeabur) 預約今天 (2026-09-14 星期一) 時，系統錯誤回覆「今天是星期日 (公休日)」。
- **根本原因**：
  Zeabur 的 Docker 容器時區為標準世界協調時間 (UTC/GMT+0)。當使用 `new Date("2026-09-14T00:00:00+08:00")` 時，JavaScript 自動將台灣午夜換算為 UTC 時間 `2026-09-13T16:00:00Z`。而 `Date.prototype.getDay()` 是依據宿主機本地時區計算，9/13 剛好是星期日 (`0`)，導致伺服器誤將星期一判定為星期日並觸發公休拒絕！
- **解決方案**：
  1. **實裝台灣時區專屬解析器 (`getTaiwanDayInfo`)**：改採台灣正中午 (`Date.UTC(year, month-1, day, 4, 0, 0)`) 錨定，並透過 `Intl.DateTimeFormat` 顯式強制鎖定 `timeZone: "Asia/Taipei"`，在任何伺服器環境下皆 100% 準確判定台灣星期。
  2. **全面更換判定點**：`checkAvailability`、`bookEvent` 與 `generateCalendarLookupTable` 全面改用時區隔離算法，對照表直覺標註 `🟢【可預約】` 與 `🛑【週末固定公休】`。
- **Git Commit (my-line-bot)**：`52e2e64`

---

## 📌 [v1.4.8] - 2026-09-14 16:53:00
### 🚫 營業時間修正為「週一至週五 14:00~22:00 (最後預約 21:00)」，實裝每週六日固定公休硬性防呆
- **修復問題**：
  原系統 Prompt 與代碼誤植為「週一至週日營業」，導致客戶可成功預約週六與週日週末時段。
- **解決方案**：
  1. **FAQ 與 Prompt 全面修正**：明確宣告「營業時間為週一至週五 14:00~22:00（最後預約 21:00），每週六、週日固定公休」，引導詢問週末之客戶預約平日時段。
  2. **查詢空檔公休攔截 (`checkAvailability`)**：遇週六、日查詢直接返回公休提示，不對外開放預約（除 9/20 公益義整活動外）。
  3. **預約寫入硬性防呆 (`bookEvent`)**：加入星期判定與 21:00 最後預約判定，若為週六日或超過 21:00 直接拒絕寫入日曆。
- **Git Commit (my-line-bot)**：`f713968`

---

## 📌 [v1.4.7] - 2026-09-14 16:48:00
### 🛡️ 徹底根除 `validateChatHistory` 報錯 (`role 'user' can't contain 'functionResponse' part`)
- **修復問題**：
  在多輪對話時伺服器崩潰並拋出：
  `GoogleGenerativeAIError: [GoogleGenerativeAI Error]: Content with role 'user' can't contain 'functionResponse' part at validateChatHistory ... at new ChatSession ... at startChat`。
- **根本原因**：
  Google Generative AI SDK 內建的 `validateChatHistory` 會嚴格檢查 `role: 'user'` 物件，若其 `parts` 中含有 `functionResponse` 鍵值即直接阻斷並拋錯。當歷史紀錄或前次工具反饋物件殘留時，即導致 `startChat` 崩潰。
- **解決方案**：
  1. **工具反饋純文字化封裝**：將工具執行結果由原本的 `functionResponse` 物件改為以自然語言純文字 (`{ text: "【系統日曆反饋 - 工具執行結果】..." }`) 封裝回傳，徹底消除任何 `functionResponse` 鍵值，讓 SDK 與 API 100% 視為合法對話內容。
  2. **歷史紀錄深度純淨淨化 (Pure Text Sanitizer)**：在每次 `startChat` 前，強制過濾對話歷史，嚴格剔除非純文字（只保留純文字 `text`，剝除任何 `functionResponse` / `functionCall`），即使舊 Session 中帶有污染也能即刻自愈重啟。

---

## 📌 [v1.4.6] - 2026-09-14 16:45:00
### 🛡️ 實裝過期時間硬性防禦 (Past Time Hard Guard) 與當日過期時段動態切除
- **修復問題**：
  1. 客戶可成功預約早於當前時間的過期時段（例如下午 16:43 仍可預約當日 14:00，甚至預約昨天的過去時間）。
  2. 查詢空檔時，當日早於當前時間之時段未過濾，導致 AI 主動向客戶推薦已經過去的時段。
- **解決方案**：
  1. **預約寫入硬性防禦 (`bookEvent`)**：在將行程寫入 Google Calendar 前，強制比對 `bookingStartDate <= now`。若早於當前台灣時間，立即終止並返回明確拒絕原因與當前時間提示。
  2. **查詢空檔動態切除 (`checkAvailability`)**：
     - 若查詢過去日期，直接攔截並提示僅能查詢今日或未來日期。
     - 若查詢當日，動態抓取當前台灣時間，自動切除已過去的小時，僅向 AI 提供未來可用區間（例：`17:00~22:00`）。
     - 若當日已接近打烊 (>= 22:00)，主動提示今日截止，引導客戶預約明日。
  3. **提示詞與工具宣告約束 (SSOT Prompt & Tool Declaration)**：
     - `calendarTools` 宣告明確規範 `startTime` 必須晚於當前時間。
     - Prompt 追加「過期時段絕對禁止鐵律」，杜絕模型幻覺。

---

## 📌 [v1.4.5] - 2026-09-11 14:40:00
### 🛡️ 修復 Gemini 3.5 API `role: function` 400 報錯與日曆環境變數去引號防禦
- **修復問題**：
  1. Gemini API 調用工具後回傳結果拋出 `[GoogleGenerativeAI Error]: [400 Bad Request] Role 'function' is not supported. Please use a valid role: SYSTEM, SYSTEM_1, USER, ASSISTANT, DEVELOPER, CONTEXT, USER_CONTEXT, MODEL, USER.`，導致客服對話崩潰。
  2. Google 日曆報錯 `invalid_grant: Invalid grant: account not found`。
- **解決方案**：
  1. **Gemini 工具回傳角色相容重構 (`sendToolResponse`)**：繞過舊版 `@google/generative-ai` SDK 內部將 `functionResponse` 硬編碼為 `role: "function"` 之缺陷，改以 Gemini 3.5 官方規範的 `role: "user"` 封裝回傳，並加入熔斷機制，確保任何異常皆平滑進入保底自然回覆。
  2. **雲端環境變數去引號清洗防禦 (`getCleanEnvString`)**：為 `GOOGLE_CLIENT_EMAIL` 與 `GOOGLE_CALENDAR_ID` 實裝自動去雙引號、單引號與空白防禦，杜絕複製貼上殘留外層引號導致 Google OAuth JWT 查無帳號。
  3. **日曆日誌強化**：於查詢/寫入/刪除失敗時明確輸出連線帳號與目標日曆 ID，排查一秒定位。
- **Git Commit (my-line-bot)**：`5a04e7a`

---

## 📌 [v1.4.4] - 2026-09-09 18:08:00
### ⚡ Gemini 模型無痛遷移至 `gemini-3.5-flash-lite`
- **修復問題**：Google 官方廢棄 `gemini-2.5-flash` API 端點，調用時拋出 `[404 Not Found] This model models/gemini-2.5-flash is no longer available to new users`。
- **解決方案**：
  1. 核心模型無縫升級為 `gemini-3.5-flash-lite`，兼具超高回應速度（約 350 tokens/s）、極低延遲與低成本優勢。
  2. 支援環境變數彈性覆蓋：`process.env.GEMINI_MODEL || "gemini-3.5-flash-lite"`，未來可透過 Zeabur 環境變數免改代碼動態切換。
  3. 實測多輪工具呼叫（Tool Calling / Function Calling）與 System Instruction 驗證 100% 通過。
- **Git Commit (my-line-bot)**：`dfa7271`

---

## 📌 [v1.4.3] - 2026-08-28 20:38:00
### 🛡️ 對話歷史純淨校驗 (Clean History Guard) 與架構防禦
- **修復問題**：Gemini API 在多輪對話時拋出 `[GoogleGenerativeAI Error]: First content should be with role 'user', got function` 崩潰報錯。
- **根本原因**：日曆工具（Function Calling）執行後產生之 `role: "function"` 物件殘留在 `userSession.history` 中，裁切歷史時意外以 `function` 開頭，違反 Gemini 對話首筆必須為 `user` 的嚴格語法規範。
- **解決方案**：
  1. 對話歷史改採純文字化紀錄（僅存 `user` 與 `model` 純文字上下文，杜絕工具暫存物件污染記憶）。
  2. 加入 `Clean History Guard` 防禦校驗：每次發送前自動過濾非合法角色，強制首筆必為 `user`。
- **Git Commit (my-line-bot)**：`415faf1`

---

## 📌 [v1.4.2] - 2026-08-28 16:42:00
### ☁️ Zeabur 雲端環境相容優化與健康檢查 API
- **功能新增**：
  1. **私鑰自動清洗 (getCleanPrivateKey)**：自動去除 Zeabur 環境變數中 `GOOGLE_PRIVATE_KEY` 的外層多餘引號，並將字面 `\n` 轉換為標準 RSA 換行，解決 OpenSSL JWT 驗證失敗問題。
  2. **根目錄健康檢查 (Health Check API)**：訪問網址首頁即時回傳 `calendarConfigured: true/false` 與 `targetCalendarId`，供 1 秒自我檢測日曆連線狀態。
  3. **package.json MIT License 宣告**：消除 Zeabur 建置時的 `No license field` 警告。
- **Git Commit (my-line-bot)**：`5005761`, `2d3dfcc`

---

## 📌 [v1.4.1] - 2026-08-28 16:28:00
### 🗓️ Google Calendar 寫入強化與多輪執行迴圈 (Multi-turn Tool Loop)
- **修復問題**：
  1. LINE Reply 報錯 `messages[0].text: May not be empty`。
  2. 預約成功後 Google 日曆未實際新增活動。
- **根本原因與解決方案**：
  1. **多輪執行迴圈 (Multi-turn Tool Loop)**：實裝 while 迴圈，確保工具執行完畢後引導 Gemini 產出自然語言確認回覆。
  2. **雙層防空兜底 (Zero-Empty Fallback)**：當模型回傳空字串時，自動抓取工具結果填補，保證絕不傳空字串給 LINE。
  3. **雙重 Payload 寫入**：同時支援 `requestBody` (新版) 與 `resource` (舊版)，並在後台打印 Event ID。
- **Git Commit (my-line-bot)**：`3c5e000`, `ed2d609`

---

## 📌 [v1.4.0] - 2026-08-28 16:15:00
### 📅 14 天動態日曆對照表注入、真人延遲與轉人工優化
- **功能新增**：
  1. **14 天動態日曆對照表 (Calendar Lookup Matrix)**：伺服器每次動態計算未來 14 天的精確日期與星期對照表注入 Prompt，徹底杜絕大語言模型心算月份天數與星期的幻覺錯誤（秒抓「下週三」= 9/2）。
  2. **真人客服打字延遲 (3 ~ 5 秒)**：加入隨機 3000ms ~ 5000ms 延遲，大幅提升真人客服呼吸感。
  3. **轉人工指令簡化**：觸發轉人工時，自動回覆精簡為「已為您轉人工。」。
  4. **9/20 公益義整活動專屬 SOP**：最高優先級攔截，引導抽號碼牌登記，禁止寫入營業日曆。
  5. **防撞期硬性攔截與多人接力服務**：日曆有佔用時主動提供二選一空檔；多人預約自動分段多次寫入。
- **Git Commit (my-line-bot)**：`18ec47d`, `375d03d`, `bdde61a`

---

## 📌 [v1.0.0 ~ v1.3.0] - 2026-08-18 ~ 2026-08-28
### 🚀 基礎建設與集中版本庫建置
- 初始化 `01_line_bot_customer_service.md` 等 6 大 Prompt 模組。
- 開發 `prompt_manager.py` CLI 工具（支援 diff, commit, history, sync, test）。
- 建立 LINE Messaging API Webhook 伺服器與 Gemini 2.5 Flash 串接。
