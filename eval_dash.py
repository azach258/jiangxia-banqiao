from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
try:
    driver.get('http://localhost:8090/booking-dashboard/test_dashboard_v2.html')
    time.sleep(1)
    driver.execute_script("app.runQATest('conflict');")
    time.sleep(0.5)
    dis = driver.execute_script("return document.getElementById('btnSubmitBooking').disabled;")
    box_text = driver.execute_script("return document.getElementById('conflictStatusText').textContent;")
    print('DISABLED_IS:', dis)
    print('BOX_TEXT_IS:', box_text)
    
    driver.execute_script("app.runQATest('crm');")
    time.sleep(0.5)
    hint_classes = driver.execute_script("return document.getElementById('phoneContextHint').className;")
    card_classes = driver.execute_script("return document.getElementById('customerContextCard').className;")
    print('HINT_CLASSES:', hint_classes)
    print('CARD_CLASSES:', card_classes)
finally:
    driver.quit()
