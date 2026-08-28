---
title: "Python Google Ads API 一鍵上架腳本與操作 SOP｜江夏傳統整復推拿 板橋館"
date: 2026-07-30
status: 進行中
category: API自動化 / Python腳本
tags:
  - 專案/江夏傳統整復推拿
  - 技術/Python
  - 自動化/GoogleAdsAPI
---

# 🤖 09. Python Google Ads API 一鍵上架腳本與操作 SOP｜江夏傳統整復推拿 板橋館

這份 SOP 將指引賴師傅如何透過 **Python 官方 `google-ads` SDK**，完成自動化權限設定，並執行一鍵自動布置廣告活動！

---

## 🔑 第一階段：申請 Google Ads API 四大金鑰（只需設定一次）

請依序準備以下 4 個字串/檔案：

1. **`developer_token` (開發者權限令牌)**：
   * 登入 Google Ads 後台 $\rightarrow$ 點擊頂部「工具與設定」 $\rightarrow$ 「API 中心 (API Center)」 $\rightarrow$ 複製「開發者權限令牌 (Developer Token)」。
2. **`client_id` 與 `client_secret`**：
   * 前往 [Google Cloud Console](https://console.cloud.google.com/) 建立專案 $\rightarrow$ 開啟 **Google Ads API** 服務 $\rightarrow$ 「憑證」 $\rightarrow$ 建立 **OAuth 2.0 用戶端 ID**（應用程式類型選擇「電腦應用程式」）。
3. **`refresh_token` (用戶授權金鑰)**：
   * 透過 Google 授權工具進行登入授權取得。
4. **`customer_id` (Google Ads 帳戶 ID)**：
   * Google Ads 頁面右上角的 10 位數數字（格式：`XXX-XXX-XXXX`）。

---

## 📄 第二階段：設定配置文件 (`google-ads.yaml`)

在您的電腦或伺服器專案目錄下建立 `google-ads.yaml` 檔案：

```yaml
developer_token: "YOUR_DEVELOPER_TOKEN"
client_id: "YOUR_CLIENT_ID.apps.googleusercontent.com"
client_secret: "YOUR_CLIENT_SECRET"
refresh_token: "YOUR_REFRESH_TOKEN"
login_customer_id: "YOUR_CUSTOMER_ID_WITHOUT_HYPHENS"
use_proto_plus: true
```

---

## 🐍 第三階段：自動上架 Python 腳本 (`deploy_google_ads.py`)

您可以在終端機安裝官方套件：
```bash
pip install google-ads
```

腳本會自動建立**「指定板橋區」、「精準關鍵字」、「15組標題與5組說明文」**全自動上架！

完整代碼請參考專案目錄下之 [deploy_google_ads.py](file:///c:/Users/love_/OneDrive/04_%E7%AD%86%E8%A8%98%E8%88%87%E7%9F%A5%E8%AD%98%E5%BA%AB/00_my_obsidian/01_Projects/%E6%B1%9F%E5%A4%8F%E5%82%B3%E7%B5%B1%E6%95%B4%E5%BE%A9%E6%8E%A8%E6%8B%BF_%E6%9D%BF%E6%A9%8B%E9%A4%A8/deploy_google_ads.py)。

---

## 🔗 相關筆記
- [[00_專案總覽]]
- [[06_Google廣告文案與標題庫]]
- [[07_Google廣告目標受眾訊號與關鍵字庫]]
- [[08_Google_Ads_API_自動化與AI對接指南]]
