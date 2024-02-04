from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import time

# WebDriverの設定（Chromeを使用）
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)

# 結果を保存するリスト
data = []

try:
    # ウェブサイトにアクセス
    base_url = "https://www.sakai-tcb.or.jp/"
    browser.get(base_url)

    # ナビゲーションメニューのリンクを取得（仮のセレクタ）
    nav_links = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav a"))
    )

    # 各ナビゲーションリンクに対して処理
    urls = [link.get_attribute("href") for link in nav_links]
    for url in urls:
        try:
            # 各ページに移動
            browser.get(url)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)  # JavaScriptがロードされるのを待つ

            # ページの全テキストを取得
            text = browser.find_element(By.TAG_NAME, "body").text

            # 結果をリストに保存
            data.append(
                {
                    "url": url,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": text.strip(),
                }
            )
        except Exception as e:
            print(f"Error accessing {url}: {e}")

    # JSONファイルに保存
    with open("website_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

finally:
    # ブラウザを閉じる
    browser.quit()
