---
title: "Google Ads API 權限與身分驗證障礙排除 SOP｜江夏傳統整復推拿 板橋館"
date: 2026-07-30
status: 進行中
category: API除錯 / 權限驗證
tags:
  - 專案/江夏傳統整復推拿
  - 技術/GoogleAdsAPI
  - 除錯/權限修復
---

# 🛠️ 10. Google Ads API 權限與身分驗證障礙排除 SOP｜江夏傳統整復推拿 板橋館

當 Google Ads 提示 **「沒有權限」** 或 `PERMISSION_DENIED` / `DEVELOPER_TOKEN_NOT_APPROVED` 時，通常是由於以下三大原因：

---

## 🔍 原因分析與排查清單

### 1. 廣告主身分驗證未完成（Google 政策強制要求）
* **現象**：Google 政策規定台灣廣告帳戶必須完成「廣告主身分驗證」才能投放廣告或調用 API。
* **解法**：
  1. 登入 Google Ads 後台。
  2. 點擊頂部 **「設定與帳單」 $\rightarrow$ 「廣告主驗證 (Advertiser Verification)」**。
  3. 依提示上傳 **身分證** 或 **商業登記/稅籍證明** 完成實名驗證。

---

### 2. OAuth2 授權範圍 (Scope) 缺少 Google Ads 權限
* **現象**：在建立 OAuth 憑證時，如果沒有勾選 Google Ads API 的存取範圍，系統會提示「沒有權限 (User doesn't have access to this client)」。
* **解法（透過 OAuth 2.0 Playground 1 分鐘解套捷徑）**：
  1. 開啟 [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground)。
  2. 點擊右上角齒輪圖示 ⚙️ $\rightarrow$ 勾選 **「Use your own OAuth credentials」** $\rightarrow$ 輸入您的 `client_id` 與 `client_secret`。
  3. 在左側清單中找到 **「Google Ads API」**，勾選 `https://www.googleapis.com/auth/adwords`。
  4. 點擊 **「Authorize APIs」** 登入您的 Gmail 授權。
  5. 點擊 **「Exchange authorization code for tokens」** $\rightarrow$ 複製產生的 `Refresh Token` 即可！

---

### 3. 開發者權限令牌 (Developer Token) 權限等級
* **現象**：剛申請的 Developer Token 為「測試存取權 (Test Access)」，無法直接對正式投放帳戶寫入資料。
* **解法**：
  * **快速方案**：若使用 OAuth Playground 產生的權限權杖直接調用，可免去漫長的 API 審核流程。
  * **正式方案**：在 Google Ads API 中心點擊「申請基本存取權 (Apply for Basic Access)」，說明用途為店家自用行銷管理腳本，通常 1-3 個工作天通過。

---

## 🔗 相關筆記
- [[00_專案總覽]]
- [[08_Google_Ads_API_自動化與AI對接指南]]
- [[09_Python_Google_Ads_API_一鍵上架腳本與操作SOP]]
