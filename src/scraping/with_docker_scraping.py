from selenium import webdriver

hub_url = "http://localhost:4444"

# WebDriverの設定
options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor=hub_url,
    options=options,
)

driver.get("https://www.sakai-tcb.or.jp/")
assert "堺観光ガイド" in driver.title

driver.quit()
