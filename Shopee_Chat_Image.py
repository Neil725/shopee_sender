from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import os , bs4 , time , threading , redis , requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

load_dotenv(encoding="utf-8")
redis_r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_POST'), db=os.getenv('REDIS_DB'),
                            decode_responses=True)
cookie = [{'domain': 'shopee.tw', 'expiry': 2245238861.233618, 'httpOnly': False, 'name': 'SPC_T_IV', 'path': '/', 'secure': False, 'value': '"zpvxsqpJgCUgYOSoagj6LA=="'}, {'domain': '.shopee.tw', 'expiry': 2245238861.233588, 'httpOnly': False, 'name': 'SPC_R_T_ID', 'path': '/', 'secure': False, 'value': '"3kTkEkR0TnOdt+TXIGNzLF+AVHUlwsMLHRvY27juzs/vaTMecBJZaTeMQggIkHdunBwiEu1yoIUboDx9nZ+MGwm8ACHKfW9OEPHOkfICKgQ="'}, {'domain': '.shopee.tw', 'expiry': 1614522461.217505, 'httpOnly': False, 'name': 'SPC_CT_a457a9d6', 'path': '/', 'secure': False, 'value': '"1614518861.N+cxaZQbK6FQFp178LOORo2M0FIzQb72V3Wv/tmBiU0="'}, {'domain': '.shopee.tw', 'expiry': 1614522461.187605, 'httpOnly': False, 'name': 'SPC_CT_5bb7495d', 'path': '/', 'secure': False, 'value': '"1614518861.YLq0AeEPxnk4j4fnA8ENM0hABVw3RayufQVshH2yM7Q="'}, {'domain': '.shopee.tw', 'expiry': 1614522461.162299, 'httpOnly': False, 'name': 'SPC_CT_aeb48c55', 'path': '/', 'secure': False, 'value': '"1614518861.hNkqdYB1H1HBrA+n/8Wl7gEiqmCtnQdphyQoDZQd2z0="'}, {'domain': '.shopee.tw', 'expiry': 1677590860, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.1515365180.1613826800'}, {'domain': '.shopee.tw', 'expiry': 2245238861.233632, 'httpOnly': False, 'name': 'SPC_R_T_IV', 'path': '/', 'secure': False, 'value': '"zpvxsqpJgCUgYOSoagj6LA=="'}, {'domain': '.shopee.tw', 'expiry': 1614522363.512287, 'httpOnly': False, 'name': 'SPC_CT_8c469008', 'path': '/', 'secure': False, 'value': '"1614518763.srtLjeT7GASh4W7BR47FHFRiAJzJRStAN2zXNjd8cro="'}, {'domain': '.shopee.tw', 'expiry': 1614522361.9416, 'httpOnly': False, 'name': 'SPC_CT_3bcd1652', 'path': '/', 'secure': False, 'value': '"1614518762.L4s2+omlzlUDyvnYJDBWryUeuu+qoJ7j6YcDShEVPIE="'}, {'domain': '.shopee.tw', 'expiry': 1614605261.233657, 'httpOnly': True, 'name': 'SPC_SI', 'path': '/', 'secure': True, 'value': 'mall.8L9PzPm0M5ggazOVnKaVP7HzxxUTwIC3'}, {'domain': '.shopee.tw', 'expiry': 253402257600, 'httpOnly': False, 'name': 'G_ENABLED_IDPS', 'path': '/', 'secure': False, 'value': 'google'}, {'domain': '.shopee.tw', 'expiry': 1614518900, 'httpOnly': False, 'name': '_dc_gtm_UA-61915057-6', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.shopee.tw', 'expiry': 1621602797, 'httpOnly': False, 'name': '_gcl_au', 'path': '/', 'secure': True, 'value': '1.1.675446401.1613826798'}, {'domain': '.shopee.tw', 'expiry': 2244546797.210374, 'httpOnly': False, 'name': 'SPC_F', 'path': '/', 'secure': True, 'value': '4EHIv0KDZQFYc3BSpldWgSVs2LL5soSu'}, {'domain': '.shopee.tw', 'expiry': 2245238861.138463, 'httpOnly': False, 'name': 'SPC_U', 'path': '/', 'secure': True, 'value': '390667155'}, {'domain': 'shopee.tw', 'expiry': 2244546797.210385, 'httpOnly': True, 'name': 'REC_T_ID', 'path': '/', 'secure': True, 'value': '64fd6a3c-737d-11eb-8c55-b4969146215a'}, {'domain': '.shopee.tw', 'expiry': 2245238861.138429, 'httpOnly': True, 'name': 'SPC_EC', 'path': '/', 'secure': True, 'value': '4JOiBZ6Pn1eWyegaQ69H8nxRPs/6/kLtlp/ELdZSC+2uOTz8LeAyW1+QJHUz99pcpXk10DuZJgzO/zPMj33m26FtFS8+/ovmzoxyK2iUjnZaqFaRa+gByqGlZAO/gG9uaetYS7Xitg+yn2krUObljqBvFRb/+tMSSPwtn4c+NL0='}, {'domain': '.shopee.tw', 'expiry': 1614605260, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.397751969.1614518762'}, {'domain': '.shopee.tw', 'expiry': 1614522361.985901, 'httpOnly': False, 'name': 'SPC_CT_0583dc58', 'path': '/', 'secure': False, 'value': '"1614518762.EEiDwPuPHIPQ/uX36r0/8aJkAoCoIVnU+LhhO20Ep5c="'}, {'domain': '.shopee.tw', 'expiry': 1622294860, 'httpOnly': False, 'name': '_fbp', 'path': '/', 'secure': False, 'value': 'fb.1.1613826798658.436713562'}, {'domain': '.shopee.tw', 'expiry': 2244546883.559088, 'httpOnly': False, 'name': 'SPC_CLIENTID', 'path': '/', 'secure': True, 'value': 'NEVISXYwS0RaUUZZgsdghtpiummhfouo'}, {'domain': 'shopee.tw', 'expiry': 2245238859.997991, 'httpOnly': False, 'name': 'SPC_IA', 'path': '/', 'secure': False, 'value': '-1'}, {'domain': '.shopee.tw', 'expiry': 1614522363.7021, 'httpOnly': False, 'name': 'SPC_CT_05c675f4', 'path': '/', 'secure': False, 'value': '"1614518763.D2/a+Bn/oz+4JBX8w1l3jBZxWGErRcxsrjvUut7IHkI="'}, {'domain': '.shopee.tw', 'expiry': 1614522363.559745, 'httpOnly': False, 'name': 'SPC_CT_6fd5216d', 'path': '/', 'secure': False, 'value': '"1614518763.HiYmny7ZYXTH7ljdatjHCwceDMcgYGUZzQ5epkttnfQ="'}, {'domain': '.shopee.tw', 'expiry': 1677590860, 'httpOnly': False, 'name': '_ga_RPSBE3TQZZ', 'path': '/', 'secure': False, 'value': 'GS1.1.1614518761.2.1.1614518860.40'}, {'domain': 'shopee.tw', 'expiry': 2245238861.233645, 'httpOnly': False, 'name': 'SPC_T_ID', 'path': '/', 'secure': False, 'value': '"3kTkEkR0TnOdt+TXIGNzLF+AVHUlwsMLHRvY27juzs/vaTMecBJZaTeMQggIkHdunBwiEu1yoIUboDx9nZ+MGwm8ACHKfW9OEPHOkfICKgQ="'}, {'domain': '.shopee.tw', 'expiry': 1614522362, 'httpOnly': False, 'name': 'AMP_TOKEN', 'path': '/', 'secure': False, 'value': '%24NOT_FOUND'}, {'domain': 'shopee.tw', 'expiry': 2245238761, 'httpOnly': False, 'name': 'csrftoken', 'path': '/', 'secure': True, 'value': 'bCti5dnhRBQ76jmZ126TrU5hoNwges0h'}]

def loginShopee(cookie):
    url = 'https://shopee.tw/ryan941'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2,
             'permissions.default.stylesheet': 2,
             "profile.default_content_setting_values.notifications" : 2}  ## 設置Chrome不加載圖片 & CSS
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe", chrome_options=chrome_options)
    driver.get(url)
    for i in cookie:
        driver.add_cookie(cookie_dict=i)
    driver.get(url)
    return driver

def CrawlerSendChat(cookie):
    driver = loginShopee(cookie)
    time.sleep(5)
    firstclick = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@class='shopee-button-outline shopee-button-outline--complement shopee-button-outline--fill shopee-button-outline-- ']")))
    firstclick.click()
    time.sleep(2)
    while True :
        list = [] # 儲存聊聊被鎖後還未送出訊息的賣家
        for i in range(0,5,1):
            homeurl = redis_r.lpop('shopee_seller_homeurl')
            driver.execute_script("window.open(\'{}\')".format(homeurl))
            list.append(homeurl)
        time.sleep(1)
        handles = driver.window_handles[1:]
        handles.reverse()
        for i in handles:
            time.sleep(1)
            image = os.getenv('message')
            driver.switch_to.window(i)
            message(driver,image)
            time.sleep(1)
            try:
                no_send_sign = driver.find_element_by_class_name('src-components-MessageSectionLayout-ConversationMessages-BaseMessage-index__resend-wrap--1ufYm')
                for i in list:
                    driver.switch_to.window(i)
                    redis_r.rpush('shopee_seller_homeurl', driver.current_url)
                print("聊聊功能已被封鎖")
                driver.quit()
            except:
                driver.close()
                continue
        driver.switch_to.window(driver.window_handles[0])
        if len(redis_r.lrange('shopee_seller_homeurl',0,-1)) == 0 :
            print("所有賣家已發送完畢")
            break
def message(driver,image):
    while True :
        try:
            # 點聊聊
            click_chat = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='shopee-button-outline shopee-button-outline--complement shopee-button-outline--fill shopee-button-outline-- ']"))).click()
            time.sleep(1)
            # 確認聊天室是否連到賣家
            seller_id = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='src-components-ConversationDetailLayout-BuyerProfile-index__name--1UP54']")))
            if len(seller_id.get_attribute('textContent')) != 0: # 表示有連到
                uploadfile = driver.find_element_by_xpath("//*[@class='src-components-Common-ImageSelector-index__root--2t-rJ']")
                uploadfile.send_keys(image)
                # Enter = driver.find_element_by_xpath("//*[@class='src-components-Common-ChatEditor-index__send-button--t-OKC']")
                # Enter.click()
                break
            else: # 未連線
                redis_r.rpush('shopee_seller_homeurl', driver.current_url)
                break
        except Exception as e:
            try:
                # 聊聊賣家未開啟 聊聊功能
                click_chat = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@class='shopee-button-outline shopee-button-outline--complement shopee-button-outline--fill shopee-button-outline--disabled ']")))
                break
            except Exception as e:
                try:
                    click_chat = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='shopee-button-outline shopee-button-outline-- ']"))).click()
                    uploadfile = driver.find_element_by_xpath("//*[@class='src-components-Common-ImageSelector-index__root--2t-rJ']")
                    uploadfile.send_keys(image)
                    break
                except:
                    redis_r.rpush('shopee_seller_homeurl', driver.current_url)
                    break
    return 'OK'

if __name__ == '__main__':
    threads = []
    for i in range(0,6,1):
        threads.append(threading.Thread(target=CrawlerSendChat, args=(cookie,)))
        time.sleep(1)
    for i in range(0,len(threads)):
        threads[i].start()


