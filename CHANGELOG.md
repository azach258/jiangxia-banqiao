# 📝 江夏傳統整復推拿 板橋館｜專案版本更新紀錄 (CHANGELOG)

本文檔記錄「江夏傳統整復推拿 板橋館」AI 客服機器人、Prompt 集中倉庫與自動化工具的所有版本演進、功能修復與 Git 變更紀錄。

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
