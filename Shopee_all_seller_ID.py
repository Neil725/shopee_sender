#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import os , bs4 , time , threading , redis

load_dotenv()
redis_r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_POST'), db=os.getenv('REDIS_DB'),
                            decode_responses=True)
seller_id_list = []  # 放置抓到的賣家ID 用來比對是否重複
threads = []  # 放置多開瀏覽器
ts = int(os.getenv('ts'))  # time.sleep等待秒數
Chrome_count = int(os.getenv('Chrome_count'))

def Run_driver():  ## 設置啟動driver至蝦皮首頁
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,
             'permissions.default.stylesheet': 2}  ## 設置Chrome不加載圖片 & CSS
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe", chrome_options=chrome_options)
    driver.get(os.getenv('Shopee_URL'))
    return driver


def Get_html_sourse(driver):  ##抓到driver的page_sourse
    shopee_page_source = driver.page_source
    shopee_html = bs4.BeautifulSoup(shopee_page_source, "html.parser")
    return shopee_html


def Crawler_Product(URLS):
    driver_session = Run_driver()
    for URL in URLS:
        Number_of_pages = int(os.getenv('Number_of_pages')) # Chrome一次打開網頁的數量
        Number = int(os.getenv('Number'))
        loop = int(os.getenv('loop'))
        while loop > 0:
            while Number < Number_of_pages:
                Product_href = 'https://shopee.tw{}?page='.format(URL.get("href"))
                shopee_Product_URL = "window.open(\'{}\')".format( Product_href + str(Number) )
                driver_session.execute_script(shopee_Product_URL)
                Number = Number + 1
                time.sleep(0.3)
            ## handles 將目前瀏覽器分頁數印出用於操控分頁
            handles = driver_session.window_handles[1:]
            handles.reverse()
            for i in handles:
                driver_session.switch_to.window(i)
                time.sleep(ts)
                Product_Content = Get_html_sourse(driver_session).find_all("script",type="application/ld+json")# 商品資料含賣家ID
                for i in Product_Content: ## 處理賣家ID
                    Product_Content_dict = eval(i.string) ## 字串轉成dict
                    if Product_Content_dict.get('@type') == 'Product':
                        product = str(Product_Content_dict['url'])
                        product_sellerID = product.split('-i.')[1].split('.')[0]
                    else: continue
                      # 過濾重複賣家  未重複寫入redis裡
                    if product_sellerID in seller_id_list :
                        continue
                    else :
                        redis_r.lpush("Shopee_seller_id",product_sellerID)
                        seller_id_list.append(product_sellerID)
            Number_of_pages += 20
            loop -= 1
            handles_quit = driver_session.window_handles
            handles_quit = handles_quit[1:]
            for i in handles_quit:
                driver_session.switch_to.window(i)
                driver_session.close()
            driver_session.switch_to.window(driver_session.window_handles[0])
    driver_session.quit()
    return seller_id_list

if __name__ == '__main__':
    ### Step1
    #### 找到所有蝦皮分類商品
    Run_driver_one = Run_driver()
    shopee_Product_list = Get_html_sourse(Run_driver_one).find_all("a",class_="_1Nw60R")
    time.sleep(5)
    if len(shopee_Product_list) < 1: ## 顯性等待至可以抓到商品分類 , < 1 代表沒抓到任何東西
        while len(shopee_Product_list) == 0:
            time.sleep(ts)
            shopee_Product_list = Get_html_sourse(Run_driver_one).find_all("a",class_="_1Nw60R")
    Run_driver_one.quit()

    ### Step2
    #### 設置多開瀏覽器異步爬取賣家ID
    step = int(len(shopee_Product_list) / Chrome_count) ## 設置需要Chrome_count個數量的瀏覽器 每個瀏覽器去抓step數量的分類
    RunChrome = [shopee_Product_list[i:i+step] for i in range(0,len(shopee_Product_list),step)]
    for i in RunChrome:
        threads.append(threading.Thread(target = Crawler_Product , args=(i,)))
        time.sleep(ts)
    for i in range(0,len(threads)):
        threads[i].start()