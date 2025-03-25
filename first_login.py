from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle

from properties import driver_path, amazon_address, login_link, email_input_id, your_email, continue_button_id, password_input_id, your_password, login_button_id

# Chromeオプションの設定
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # エラーレベルのログのみ表示

# WebDriverのパスを指定
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Amazonのトップページにアクセス
    driver.get(amazon_address)
    time.sleep(2)

    #ログイン
    login_btn = driver.find_element(By.ID, login_link)
    login_btn.click()
    time.sleep(1)

    
    # ログイン情報を入力
    email_input = driver.find_element(By.ID, email_input_id)
    email_input.send_keys(your_email)
    driver.find_element(By.ID, continue_button_id).click()

    time.sleep(2)  # ページ遷移の待機

    password_input = driver.find_element(By.ID, password_input_id)
    password_input.send_keys(your_password)
    driver.find_element(By.ID, login_button_id).click()

    time.sleep(5)  # ログイン完了の待機

    # 2段階認証を手動で完了する
    input("2段階認証を完了したらEnterキーを押してください...")

    # クッキーを保存
    with open('cookies.pkl', 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

finally:
    # ブラウザを閉じる
    driver.quit()