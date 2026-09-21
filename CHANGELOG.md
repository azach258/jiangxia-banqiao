# 📝 江夏傳統整復推拿 板橋館｜專案版本更新紀錄 (CHANGELOG)

本文檔記錄「江夏傳統整復推拿 板橋館」AI 客服機器人、Prompt 集中倉庫與自動化工具的所有版本演進、功能修復與 Git 變更紀錄。

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
