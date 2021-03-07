from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import os , bs4 , time , threading , redis , requests

load_dotenv(encoding="utf-8")
url = 'https://shopee.tw/ryan941'
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2,
         'permissions.default.stylesheet': 2,
         "profile.default_content_setting_values.notifications" : 2}  ## 設置Chrome不加載圖片 & CSS
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path="C:/chromedriver.exe", chrome_options=chrome_options)
driver.get(url)
# 先登入 手機帳號 在執行下列取得cookies
driver.get_cookies()
# 將cookeies 資料貼到 發送聊聊程式裡的cookies
