import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_cloud_sync_feature():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        dashboard_url = "http://localhost:8090/booking-dashboard/test_dashboard_v2.html"
        print(f"[TEST 1] Visiting Dashboard: {dashboard_url}")
        driver.get(dashboard_url)
        time.sleep(1.5)

        # 1. 檢查導航列是否存在「雲端同步」與「雲端設定」按鈕
        btn_sync = driver.find_element(By.ID, "btnCloudSync")
        btn_settings = driver.find_element(By.XPATH, "//button[contains(@title, 'Google 雲端 API 設定')]")
        assert btn_sync.is_displayed(), "雲端同步按鈕未顯示"
        assert btn_settings.is_displayed(), "雲端設定按鈕未顯示"
        print("  -> 導航列雲端按鈕驗證通過")

        # 2. 點擊「雲端設定」打開 Modal
        btn_settings.click()
        time.sleep(0.5)
        modal = driver.find_element(By.ID, "cloudSettingsModal")
        assert "hidden" not in modal.get_attribute("class"), "雲端設定 Modal 未正常開啟"
        print("  -> 雲端設定 Modal 彈出驗證通過")

        # 3. 測試輸入自訂 GAS URL 與 Secret
        input_url = driver.find_element(By.ID, "settingGasUrl")
        input_secret = driver.find_element(By.ID, "settingGasSecret")
        test_url = "https://script.google.com/macros/s/AKfycb_test_endpoint_jiangxia/exec"
        input_url.clear()
        input_url.send_keys(test_url)
        
        # 點擊儲存
        save_btn = driver.find_element(By.XPATH, "//button[contains(text(), '儲存連線設定')]")
        save_btn.click()
        time.sleep(0.5)

        assert "hidden" in modal.get_attribute("class"), "儲存後 Modal 應自動關閉"
        
        # 驗證 localStorage 是否已更新
        saved_url = driver.execute_script("return localStorage.getItem('jiangxia_gas_api_url')")
        assert saved_url == test_url, f"localStorage 網址不符: {saved_url}"
        print(f"  -> 雲端設定成功存入 LocalStorage: {saved_url}")

        # 驗證頂部徽章文字更新
        status_text = driver.find_element(By.ID, "syncStatusText").text
        assert "Google 雲端雙向連線中" in status_text, f"狀態文字未切換為雲端連線: {status_text}"
        print(f"  -> 頂部連線狀態更新: {status_text}")

        # 4. 前往顧客前台測試
        front_url = "http://localhost:8090/test_front_booking.html"
        print(f"[TEST 2] Visiting Front: {front_url}")
        driver.get(front_url)
        time.sleep(1.5)

        # 驗證前台能正確讀取到後台所設定的 gasUrl
        app_gas_url = driver.execute_script("return window.frontApp.gasUrl")
        assert app_gas_url == test_url, f"前台未繼承雲端 API 網址: {app_gas_url}"
        print(f"  -> 前台成功自動繼承雲端 API 網址: {app_gas_url}")

        # 點擊預約按鈕打開彈窗
        driver.execute_script("frontApp.openBookingModal();")
        time.sleep(0.5)
        booking_modal = driver.find_element(By.ID, "frontBookingModal")
        assert "hidden" not in booking_modal.get_attribute("class"), "前台預約 Modal 未能開啟"
        print("  -> 前台預約 Modal 正常開啟")

        # 檢查可選時段
        slots = driver.find_elements(By.CSS_SELECTOR, "#frontSlotsGrid button")
        assert len(slots) >= 5, f"時段按鈕數量過少: {len(slots)}"
        print(f"  -> 時段按鈕渲染正常 ({len(slots)} 個時段)")

        print("\nALL STEP 3 CLOUD INTEGRATION QA TESTS PASSED! 100% OK")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_cloud_sync_feature()
