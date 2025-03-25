import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle

from properties import driver_path, invoice_dir, amazon_address, order_history_link
from logic.save_pdf import save_pdf

# Chromeオプションの設定
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # エラーレベルのログのみ表示

# WebDriverのパスを指定
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 保存先のディレクトリを指定
if not os.path.exists(invoice_dir):
    os.makedirs(invoice_dir)

try:
    # Amazonのトップページにアクセス
    driver.get(amazon_address)
    time.sleep(1)

    # クッキーを読み込む
    with open('cookies.pkl', 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    
    # クッキーを適用した後にページをリフレッシュ
    driver.refresh()

    time.sleep(2)
    
    # 注文履歴ページにアクセス
    order_history_btn = driver.find_element(By.ID, order_history_link)
    order_history_btn.click()

    time.sleep(2)  # ページが完全にロードされるのを待機
    

    while True:

        # 注文履歴を取得
        orders = driver.find_elements(By.CSS_SELECTOR, 'li.order-card__list')
    
        for order in orders:
            # print()
            try:
                # 注文IDを取得
                order_id_element = order.find_element(By.CSS_SELECTOR, '.yohtmlc-order-id span[dir="ltr"]')
                order_id = order_id_element.text.strip()

                # 注文日を取得
                try:
                    order_date_element = order.find_element(By.CSS_SELECTOR, '.a-size-base.a-color-secondary.aok-break-word')
                    order_date = order_date_element.text.strip()
                except Exception as e:
                    print(f"Error finding order date: {e}")
                    order_date = "unknown_date"

                # 「領収書等」リンクを探してクリック
                # receipt_link = order.find_element(By.XPATH, '//a[contains(@href, "invoice.html")]')
                receipt_link = order.find_element(By.LINK_TEXT, '領収書等')
                receipt_link.click()

                time.sleep(1)  # ページ遷移の待機

                # ポップアップ内の特定の「領収書／購入明細書」リンクをクリック
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'a-popover-inner'))
                    )
                    # invoice_link = driver.find_element(By.XPATH, '//div[@class="a-popover-inner"]//a[contains(@href, "print.html")]')
                    invoice_link = driver.find_element(By.LINK_TEXT, '領収書／購入明細書')
                    invoice_link.send_keys(Keys.CONTROL + Keys.RETURN)

                    # 新しいタブに切り替え
                    driver.switch_to.window(driver.window_handles[-1])
                except Exception as e:
                    print(f"Error finding invoice link: {e}")
                    continue

                time.sleep(2)  # ページ遷移の待機

                # PDFを保存
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )
                save_pdf(driver, order_date, order_id)

                # 新しいタブを閉じて元のタブに戻る
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error processing order: {e}")
                continue
        
        try:
            # 次のページに移動
            next_page_link = driver.find_element(By.CSS_SELECTOR, '.a-pagination .a-last a')
            next_page_link.click()
            time.sleep(2)  # ページ遷移の待機
        except:
            # 「次へ」ボタンがない場合は終了
            break
        

finally:
    # ブラウザを閉じる
    driver.quit()