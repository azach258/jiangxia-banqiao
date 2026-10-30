# 江夏傳統整復推拿（板橋館）- Google 日曆與試算表橋樑 3 分鐘部署指南

> **目的**：將官網線上自主預約與師傅排程看板，無縫直連至賴師傅的 **Google 日曆** 與 **Google 試算表**。<br>
> **費用**：**完全 0 元**（利用 Google 官方內建的免費 Apps Script 與 Cloud 配額）。

---

## 📌 超簡單 5 步驟部署流程

### 步驟 1：建立 Google 試算表
1. 請在瀏覽器登入賴師傅（或門店管理用）的 Google 帳號。
2. 前往 [Google 試算表 (Google Sheets)](https://sheets.new)，建立一份新試算表。
3. 將試算表命名為：**`江夏板橋館_雲端預約名冊`**。

---

### 步驟 2：開啟 Apps Script 編輯器
1. 在試算表上方選單列，點選 **「擴充功能 (Extensions)」** ➔ **「Apps Script」**。
2. 進入編輯器後，將預設的 `function myFunction() {}` 全部反白刪除。

---

### 步驟 3：貼上橋樑代碼並儲存
1. 開啟本專案的 [`google_apps_script/Code.gs`](file:///C:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/google_apps_script/Code.gs)。
2. 將全部代碼複製，貼入 Apps Script 編輯器中。
3. 點擊上方的 **「磁碟片圖示 (儲存)」** 或按下鍵盤 `Ctrl + S`。

---

### 步驟 4：發布為網頁應用程式 (重要關鍵)
1. 點擊右上角藍色按鈕 **「部署 (Deploy)」** ➔ 選擇 **「新增部署 (New deployment)」**。
2. 在彈出視窗左上角的「齒輪圖示 ⚙️」旁，選擇 **「網頁應用程式 (Web app)」**。
3. 填寫以下設定（**請務必完全依照此設定**）：
   - **說明**：`江夏板橋館預約日曆橋樑 v1`
   - **執行身分 (Execute as)**：**`我 (Me / 您的 Google 帳號)`**
   - **誰可以存取 (Who has access)**：**`任何人 (Anyone)`** *(⚠️ 重要！顧客在前台自主預約才能免登入直接寫入日曆)*
4. 點擊右下角 **「部署 (Deploy)」**。
5. **首次授權提示**：
   - 系統會跳出「需要授權」視窗，點擊「核准存取權 (Authorize access)」。
   - 選擇您的 Google 帳號。
   - 若出現「Google 尚未驗證這個應用程式」，請點擊左下方 **「進階 (Advanced)」** ➔ 點擊 **「前往『未命名專案』(安全)」** ➔ 點擊 **「允許 (Allow)」**。

---

### 步驟 5：複製網址並填入看板
1. 部署成功後，畫面會顯示 **網頁應用程式網址 (Web app URL)**（結尾為 `/exec`）。
   - 例如：`https://script.google.com/macros/s/AKfycbx.../exec`
2. 點擊「複製」該網址。
3. 回到本機看板 [http://localhost:8090/booking-dashboard/test_dashboard_v2.html](http://localhost:8090/booking-dashboard/test_dashboard_v2.html)：
   - 點擊頂部 **「雲端設定」** 按鈕。
   - 將剛複製的網址貼入 **「Google Apps Script Web App 網址」** 欄位。
   - 安全金鑰維持預設：`jiangxia_banqiao_2026`。
   - 點擊 **「測試連線 (Ping)」**。
   - 看到綠色 **🟢 連線成功！** 即代表全通路正式打通！
