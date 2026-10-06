# 💆 江夏傳統整復推拿（板橋館）｜預約系統儀表板完整提示詞 (Master Prompt)

> 💡 **使用說明**：  
> 將下方 `--- [PROMPT START] ---` 到 `--- [PROMPT END] ---` 之間的完整內容，直接複製貼給任何強大 LLM（如 Gemini 2.5/3.0 Pro, Claude 3.7 Sonnet），即可 100% 一次性生成一套現代感十足、具備 Google Calendar API 連動能力、可即刻部署到雲端的單頁 HTML 預約儀表板。

---

```markdown
--- [PROMPT START] ---
# Role & Project Identity
你是一位世界級的高級前端架構師與 UI/UX 專家。請為台灣知名整復名店「江夏傳統整復推拿 板橋館（賴師傅）」打造一套高顏值、現代大氣、具備生產級實用性的「預約管理系統儀表板 (Single-Page Booking Dashboard)」。

門店資訊：
- 店名：江夏傳統整復推拿 板橋館（賴師傅）
- 地址：新北市板橋區館前西路 152-1 號
- 營業時間：每日 10:00 - 21:00 (每時段預約制)
- 服務項目：
  1. 全身整復放鬆調理 (60 分鐘 / 定價 $1,200)
  2. 局部加強筋骨舒緩 (30 分鐘 / 定價 $700)
  3. 深度經絡調理放鬆 (90 分鐘 / 定價 $1,800)
- 法規合規原則：民俗調理保健舒緩，禁用醫療用語（如治療、骨盆矯正、復健）。

---

## 🎨 1. 視覺設計與 UI/UX 風格規範
- **色彩語彙 (Aesthetic)**：
  - 以「現代養生沉穩木質調與科技深色 (Dark Mode Elegance)」為基調：
    - 主背景：深墨黑/硯台黑 `#0f172a` (Slate-900) 搭配細緻漸層與琉璃光暈。
    - 卡片表面：半透明毛玻璃質感 (`backdrop-blur-md bg-slate-800/80 border border-slate-700/60`)。
    - 點綴主色：江夏古典朱砂紅 `#e11d48` (Rose-600) 與 沉穩翡翠琥珀金 `#d97706` (Amber-600)。
    - 狀態色彩標籤：
      - `已確認`：翡翠綠 Emerald (`bg-emerald-500/10 text-emerald-400 border-emerald-500/30`)
      - `已到店`：科技藍 Sky/Cyan (`bg-cyan-500/10 text-cyan-400 border-cyan-500/30`)
      - `已完成`：典雅紫 Violet (`bg-purple-500/10 text-purple-400 border-purple-500/30`)
      - `已取消`：石板灰 Slate (`bg-slate-500/10 text-slate-400 border-slate-500/30`)
- **響應式排版 (RWD)**：
  - 手機端 (< 768px)：底部常駐導航切換（日曆/列表/新增）、單欄直式時段卡片。
  - 電腦端 (>= 1024px)：左側統計指標與快速日曆切換，右側寬幅時間軸或週曆網格。
- **技術棧要求**：
  - 單一獨立 `index.html` 檔案，包含 HTML5 + TailwindCSS (CDN: `https://cdn.tailwindcss.com`) + 現代 Vanilla JS (ES6+)。
  - 圖標引入：Lucide Icons (CDN: `https://unpkg.com/lucide@latest`)。
  - 無需 npm build，可直接在瀏覽器雙擊開啟，亦可直接推送至 GitHub Pages / Cloudflare Pages / Vercel 部署。

---

## ⚡ 2. 核心功能模組與交互規格

### A. 頂部狀態列 (Top Navigation Header)
1. **門店品牌識別**：江夏傳統整復推拿 板橋館 Logo、標題與「賴師傅預約總台」字樣。
2. **連線狀態指示燈 (Live Status Indicator)**：
   - 顯示「🟢 Google Calendar 已連線」或「🟡 離線展示模式 (Mock Data)」。
3. **快捷按鈕群**：
   - 「⚙️ API 設定」：彈窗設定 Google Apps Script Web App URL 與 Secret。
   - 「🔄 立即同步」：旋轉動畫並即刻向 API 重新拉取日曆事件。
   - 「➕ 快速預約 (New Booking)」：突出的朱砂紅色 CTA 按鈕。

### B. 關鍵指標卡片列 (Summary Metrics Cards)
- 今日總預約數 (含環比標示)
- 待到店人數
- 今日已完成數
- 今日剩餘空檔時段數 (自動依 10:00-21:00 扣除預約計算)

### C. 雙視圖切換 (Calendar Timeline vs. List Table)
1. **時間軸視圖 (Day Timeline View)**：
   - 支援日期間「前一天 / 今天 / 後一天」快速切換與日期選取器 (Datepicker)。
   - 縱向時間軸（10:00 至 21:00，每小時一列標籤）。
   - 空檔時段顯示虛線框「＋ 點擊預約此時段」，點擊自動將預約彈窗的時間帶入該時段。
   - 已預約區塊依服務長度（30分佔半格、60分佔滿格、90分佔一格半）自適應高度，顯示：顧客姓名、遮罩電話 (0912-***-456)、項目名稱、狀態徽章。
2. **預約清單檢索視圖 (List / Table View)**：
   - 即時關鍵字搜尋（可搜尋姓名、手機末碼、備註）。
   - 狀態篩選 Tabs（全部、已確認、已到店、已完成、已取消）。
   - 表格欄位：預約時間、顧客、聯絡電話、服務項目、時長、狀態、操作按鈕（修改、變更狀態、刪除、LINE 確認複製）。

### D. 預約操作彈窗 (Booking Modals)
1. **新增預約彈窗 (Create Booking Modal)**：
   - 顧客姓名 (必填)
   - 聯絡電話 (必填，自動驗證格式)
   - 預約日期與開始時間 (Time Slot Picker)
   - 服務項目（下拉選單：全身 60m、局部 30m、深度 90m；選擇後自動聯動計算結束時間）
   - 師傅選擇（預設：賴師傅）
   - 症狀/備註（如肩頸僵硬、久坐腰痠）
   - **防呆衝突檢測**：點擊儲存前，若該時段與現有預約重疊，跳出警示提示並拒絕重複預約（除非勾選強制覆蓋）。
2. **預約詳情與狀態流轉彈窗 (Detail Modal)**：
   - 點擊卡片查看完整資訊。
   - 預約操作模組：新增預約、查看預約詳情、快速標記「已到店 / 已完成」、一鍵複製 LINE 確認通知文案、取消/刪除預約。

### F. 到店顧客自述與調理紀錄卡模組 (Customer Care Record Modal)
> ⚠️ **衛生局法規合規與避坑鐵律**：
> 依法非醫療院所，嚴禁在系統字面上使用「病人」、「病歷」、「處方」、「治療」等醫療專用名詞。全面改採合規且專業的：**「顧客」**、**「不適部位與自述困擾」**、**「調理紀錄卡 (Care Record)」**、**「調理手法」**。

1. **紀錄卡觸發時機**：
   - 當顧客到店（狀態變更為「已到店」或點擊預約卡片）時，提供醒目的「📋 填寫/檢視調理紀錄卡」按鈕。
2. **顧客自述困擾 (Customer Concerns & Symptoms)**：
   - **身體部位快速標籤勾選**（一鍵高亮選取，適合師傅快速點擊）：
     - 頸部僵硬、斜方肌緊繃、膏肓不適、肩胛內側、久坐腰痠、腰肌勞損、骨盆周圍沉重、媽媽手/手腕痠痛、膝部沉重、小腿緊繃。
   - **緊繃與不適程度等級 (NRS 1-10 刻度)**：1 (輕微疲勞) ~ 10 (極度僵硬卡死)。
   - **誘發情境快速選擇**：長期久坐辦公、重度體力勞動、劇烈運動後、睡眠障礙。
   - **急性症狀安全警示**：若勾選「近期急性紅腫發炎/扭傷外傷」，跳出安全提示「建議先前往醫院檢查，暫緩大幅度整復推拿」。
3. **師傅調理手法與重點紀錄 (Practitioner Adjustment Notes)**：
   - **常用手法快捷標籤**：傳統筋膜放鬆、經絡循行推拿、深層斜方肌舒緩、骨盆肌群平衡放鬆、胸椎關節活動度舒展、熱敷循環加強。
   - **調理後改善度評估**：顯著放鬆 (70%以上)、中度舒緩 (40-60%)、輕微緩解 (20-30%)。
   - **客製化居家保養建議**：避免翹二郎腿、定時起身拉伸、多飲溫水促進代謝、48小時內避免劇烈碰撞。
4. **顧客歷史調理時光軸 (Customer History Timeline)**：
   - 自動依據顧客聯絡電話，彙整該顧客過去在江夏的所有到店調理紀錄。
   - 師傅可橫向或縱向查閱歷次調理日期、當時主訴與調理手法，精準掌握老顧客身體狀況。
5. **雲端同步與保存**：
   - 調理紀錄卡儲存時，自動序列化存入 Google Calendar 事件的詳細描述 (Description) 擴充區塊，並同步寫入 Google Sheets 備份試算表。
   - 本地提供 LocalStorage 離線快取，無網路也能隨查隨記。

---

### E. Google Calendar API 對接邏輯 (Google Apps Script Integration)
1. **API 配置面板 (Settings Modal)**：
   - 支援輸入：`Google Apps Script Web App URL` 與 `API Secret`。
   - 提供「測試連線 (Test Ping)」按鈕，連線成功提示綠色 Toast 並儲存於瀏覽器 `localStorage`。
2. **資料拉取與同步 (Sync Mechanism)**：
   - 若未設定 API URL，預設載入高品質的 Mock Data（模擬今日與未來一週預約）。
   - 若已設定 API URL，啟動時透過 `fetch(API_URL + '?action=getEvents&start=...&end=...&secret=...')` 獲取日曆真實事件。
   - 新增、修改狀態、取消預約時，發送 POST 請求至 GAS API，後端自動更新 Google Calendar。
   - 完整錯誤捕捉與優雅退場（當網路離線時提示快取模式）。

---

## 📦 3. 代碼結構與交付物標準
- 產出一份完整、沒有任何 `// TODO`、沒有省略程式碼的 `index.html`。
- 內部架構分為：
  1. `<head>` 引入 Tailwind CDN、Google Fonts (Noto Sans TC)、Lucide Icons。
  2. `<body>` 現代美學布局（頂部導航、數據指標、主日曆/列表切換、浮動按鈕、多個 Modal 視窗）。
  3. `<script>` 封裝清晰的 JS 模組：
     - `State`：管理當前預約清單、當前選定日期、視圖模式、API 設定。
     - `MockService`：提供預設展示資料。
     - `ApiService`：封裝 GAS Web App 的 GET/POST 調用。
     - `UI`：負責 DOM 渲染、日曆網格繪製、Toast 提示、Modal 開關。
     - `Event Handlers`：所有按鈕點擊與表單驗證事件。
--- [PROMPT END] ---
```
