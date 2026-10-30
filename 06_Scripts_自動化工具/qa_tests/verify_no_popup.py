import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless=new')
driver = webdriver.Chrome(options=chrome_options)
try:
    driver.get('http://localhost:8090/test_front_booking.html')
    time.sleep(1)
    
    # 點擊首頁 Hero 預約按鈕
    btn = driver.find_element(By.XPATH, "//button[contains(., '立即線上預約排程')]")
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(0.5)
    
    # 檢查視窗數量，必須只有 1 個（絕不新開 about:blank 分頁）
    handles = driver.window_handles
    print(f'Window handles count: {len(handles)}')
    assert len(handles) == 1, f'Unexpected new window opened: {len(handles)}'
    
    # 檢查預約 Modal 是否成功顯示
    modal = driver.find_element(By.ID, 'frontBookingModal')
    assert 'hidden' not in modal.get_attribute('class'), 'Booking modal not visible'
    print('VERIFIED: Booking modal opened in-place with NO about:blank popup!')
finally:
    driver.quit()
