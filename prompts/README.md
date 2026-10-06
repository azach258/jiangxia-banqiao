# 📚 江夏專案 Prompt 提示詞倉庫 (Prompts Registry)

本目錄為「江夏傳統整復推拿 板橋館」全方位 AI 提示詞的單一真相源 (Single Source of Truth, SSOT)。
所有提示詞均納入 **Git 版本控制**，支援透過 `prompt_manager.py` 進行版本升級、差異比對 (Diff) 與除錯。

---

## 🗂️ 提示詞清單 (Prompts Index)

| 檔案名稱 | 提示詞名稱 | 用途與端點 | 目標模型 / 服務 |
| :--- | :--- | :--- | :--- |
| [`01_line_bot_customer_service.md`](file:///c:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/prompts/01_line_bot_customer_service.md) | LINE@ AI 智慧客服 | 門市客服、預約登記、法規過濾 | Gemini 2.5 Flash / LINE Webhook |
| [`02_meta_ads_copywriter.md`](file:///c:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/prompts/02_meta_ads_copywriter.md) | Meta 廣告文案專家 | 6 大情緒矩陣、A/B 測試文案 | Antigravity / Gemini Pro |
| [`03_meta_ad_buyer_strategy.md`](file:///c:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/prompts/03_meta_ad_buyer_strategy.md) | Meta 廣告投手策略 | 5KM 半徑、受眾漏斗、數據診斷 | Meta Ads API / Antigravity |
| [`04_visual_creative_generator.md`](file:///c:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/prompts/04_visual_creative_generator.md) | 廣告素材視覺生圖 | Nano Banana / Flux / PIL 出圖規範 | fal.ai / Flux / Pillow 腳本 |
| [`05_google_ads_copywriter.md`](file:///c:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/prompts/05_google_ads_copywriter.md) | Google 關鍵字廣告 | RSA 搜尋廣告標題說明、否定關鍵字 | Google Ads API / Python 上架腳本 |
| [`06_event_campaign_prompts.md`](file:///c:/Users/love_/OneDrive/04_筆記與知識庫/00_my_obsidian/01_Projects/江夏傳統整復推拿_板橋館/prompts/06_event_campaign_prompts.md) | 活動與促銷宣傳 | 0920 義整、門市好評促銷文案 | FB / LINE 廣播 / Threads |

---

## 🛠️ 管理指令速查 (CLI Quickstart)

```bash
# 1. 檢視所有 Prompt 版本與狀態
python prompt_manager.py list

# 2. 比對 Prompt 與 Git 上一版的差異 (除錯/調優比對)
python prompt_manager.py diff 01_line_bot

# 3. 提交新版本並自動遞增版本號
python prompt_manager.py commit 01_line_bot -m "優化無預約紀錄時的柔性緩衝語句"

# 4. 查看特定 Prompt 的修訂演進歷史
python prompt_manager.py history 01_line_bot

# 5. 一鍵同步 Prompt 到 LINE Bot 服務路徑 (SSOT)
python prompt_manager.py sync

# 6. 法規紅線與關鍵字快速除錯測試
python prompt_manager.py test 01_line_bot --query "我有脊椎側彎可以幫我矯正嗎？"
```
