# 💆 江夏傳統整復推拿（板橋館）｜預約管理系統儀表板

> **所屬專案**：[[江夏傳統整復推拿_板橋館]]  
> **門店位址**：新北市板橋區館前西路 152-1 號  
> **技術架構**：HTML5 + TailwindCSS + Vanilla JS (SPA) + Google Apps Script (GAS) API + Google Calendar API  
> **建立日期**：2026-09-08  

---

## 📌 1. 專案願景與核心解決痛點

本子專案旨在為「江夏傳統整復推拿（板橋館）賴師傅」建置一套輕量化、免伺服器維護費用的**雲端預約管理儀表板**：
1. **擺脫紙筆與零散對話**：將電話、LINE@ 官方帳號、現場預約集中於單一視覺化看板。
2. **Google Calendar 即時雙向同步**：預約即時寫入師傅的 Google 日曆，手機自動推播提醒，出門或在店都能隨時掌握時程。
3. **時段衝突自動防呆**：選取時間後，系統自動檢查 Google 日曆是否有重疊預約，杜絕重疊撞期尷尬。
4. **雲端零成本部署**：前端託管於 GitHub Pages / Cloudflare Pages / Vercel，後端 API 託管於 Google Apps Script，**維持 0 元運營成本**。

---

## 📂 2. 子專案目錄架構

```
booking-dashboard/
├── README.md                 # 專案總覽、設定教學與架構規格 (本文件)
├── PROMPT_MASTER.md          # 儀表板生成之完整提示詞 (Master Prompt)
├── index.html                # 預約管理儀表板單頁前端應用程式 (HTML/JS/CSS)
├── gas_calendar_api.js       # Google Apps Script 雲端日曆中繼 API 腳本
└── mock_data.json            # 本地測試與離線展示用預約資料
```

---

## 🔗 3. Google Calendar API 對接架構 (Google Apps Script)

為了讓前端 HTML 能安全、免費地直接存取 Google 日曆，我們採用 **Google Apps Script (GAS) Web App** 作為中繼層：

```
[前端儀表板 (HTML/JS)] 
       ▲
       │  HTTPS Fetch (JSON)
       ▼
[Google Apps Script Web App] ── (自有 Google 帳號授權) ──► [Google Calendar API]
       │
       └──────────────────────────────────────────────────► [Google Sheets 備份試算表]
```

### 部署 3 步驟：
1. 前往 [script.google.com](https://script.google.com/) 新建專案。
2. 將本專案中的 `gas_calendar_api.js` 貼入編輯器中，修改 `CALENDAR_ID`（通常是您的 Gmail 信箱，或專屬門店日曆 ID）。
3. 點擊「部署」➔「新增部署作業」➔ 類型選擇「網頁應用程式 (Web app)」：
   - **執行身分**：我 (您的 Google 帳號)
   - **誰可以存取**：任何人 (Anyone)
   - 複製產生的 `Current web app URL`，填入儀表板的「設定」中即可即時連線！

---

## 🚀 4. 前端儀表板雲端部署方式

- **方式 A (GitHub Pages - 最推薦)**：
  - 將本專案推送至 GitHub Repository。
  - 進入 Repo Settings ➔ Pages ➔ Source 選擇 `Deploy from a branch`。
- **方式 B (Vercel)**：
  - 綁定 GitHub 直接 Import 該目錄，Framework Preset 選 `Other`，一鍵自動發布並享有自訂網域。
- **方式 C (Cloudflare Pages)**：
  - 直接上傳資料夾或連結 Git，全球極速 CDN 與免費 SSL。

---

## 📱 5. 當前已完成核心功能清單 (2026-09-09 Checkpoint)

- [x] **全響應式 RWD 深度適配**：
  - 手機端 (<640px) 底部快捷導航列 (Mobile Bottom App Bar) ＋ 中央懸浮「➕ (新增預約 FAB)」
  - 預約清單雙模自適應（桌面寬表格 vs. 手機雙排圓角卡片流）
  - 全屏抽屜式 Modal 彈窗（Sticky 頂欄 ＋ Sticky 底部儲存列 `pb-safe`，虛擬鍵盤防遮蔽）
  - iOS Safari 16px 字體防放大鎖定與安全區相容
- [x] **合規顧客調理紀錄卡 (Care Record)**：
  - 避開《醫療法》第 84 條醫療用詞（顧客自述困擾、調理紀錄、手法）
  - 身體部位、誘發情境、手法快捷標籤點選、1-10分緊繃滑動軸、老顧客歷史就診時光軸
- [x] **收費結帳與小計自動連動**：
  - 主項目 (全身/局部/深度) ＋ 加購 (熱敷/刮痧拔罐/溫灸) 金額動態計算
  - 現金、LINE Pay、街口、轉帳、信用卡多元支付記錄
- [x] **營運統計報表中心 (Analytics)**：
  - 今日營收、本月累計、平均客單價 (AOV)、調理人次、項目排行長條圖與付款佔比
  - 一鍵匯出相容 Excel 的 UTF-8 BOM 營收 CSV 報表
- [x] **Google Calendar 雙向即時同步機制**：
  - 雙向即時讀寫 ＋ 30 秒自動輪詢與視窗喚醒
  - 一鍵連線診斷 Ping 檢測（延遲 ms、日曆名稱、時區、行程筆數）

---

## 🎯 6. 明日持續推進待辦 (Next Action Items)

1. **Google Apps Script 雲端部署**：
   - 將 `gas_calendar_api.js` 部署至賴師傅或門店的 Google 帳號，發布為 Web App。
   - 取得正式 Web App URL 並於儀表板「設定」面板中完成首次真機連線綁定與診斷測試。
2. **靜態單頁免費雲端上線**：
   - 透過 GitHub Pages 或 Cloudflare Pages 將 `index.html` 正式上線發布。
3. **LINE@ 官方帳號對接與現場使用驗證**：
   - 整合預約確認訊息一鍵複製文案至門店 LINE@。
   - 師傅現場手機 / 平板實際流程試跑。

