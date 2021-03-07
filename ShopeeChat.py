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
cookie = [{'domain': '.shopee.tw', 'expiry': 2245826039.822831, 'httpOnly': False, 'name': 'SPC_R_T_IV', 'path': '/', 'secure': False, 'value': '"Hmq5LVwiJWhbVtR2lJJ9pA=="'}, {'domain': '.shopee.tw', 'expiry': 1615109595.282499, 'httpOnly': False, 'name': 'SPC_CT_0d36e8e4', 'path': '/', 'secure': False, 'value': '"1615105992.Or6Qf3rn6jdUu3kxoCFQ15ksx3HHfyP8Vi5ys0Osv8A="'}, {'domain': 'shopee.tw', 'expiry': 2245826039.822818, 'httpOnly': False, 'name': 'SPC_T_IV', 'path': '/', 'secure': False, 'value': '"Hmq5LVwiJWhbVtR2lJJ9pA=="'}, {'domain': 'shopee.tw', 'httpOnly': False, 'name': 'csrftoken', 'path': '/', 'secure': False, 'value': 'YoTVLD9I99Nh4X2Gy4wugCbOfp1xMw2P'}, {'domain': '.shopee.tw', 'expiry': 2245826039.822784, 'httpOnly': False, 'name': 'SPC_R_T_ID', 'path': '/', 'secure': False, 'value': '"rCQ14OVfIuRLgnaGNguVEO4OG2CiyPvh4wwzeDC3OIyIofdj1TZGonjXpFiAiqnaYQM8n9L1RrFj+WSOIMDJXwja+OFwkQhJZ2G1Snxkx+4="'}, {'domain': '.shopee.tw', 'expiry': 1622882039, 'httpOnly': False, 'name': '_fbp', 'path': '/', 'secure': False, 'value': 'fb.1.1615105994013.541535529'}, {'domain': '.shopee.tw', 'expiry': 1615109639.787191, 'httpOnly': False, 'name': 'SPC_CT_369d5b9a', 'path': '/', 'secure': False, 'value': '"1615106036.+G97nTq1V6+jBVa9R3cfMTFO7YYhzov7H3yCC9DE4dA="'}, {'domain': '.shopee.tw', 'expiry': 1678178039, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.1.544308976.1615105995'}, {'domain': '.shopee.tw', 'expiry': 2245826021.229245, 'httpOnly': False, 'name': 'SPC_CLIENTID', 'path': '/', 'secure': False, 'value': 'TFI1ZUt1TzdqaDcxmgaemjoqrbpsgjtj'}, {'domain': '.shopee.tw', 'expiry': 1678178039, 'httpOnly': False, 'name': '_ga_RPSBE3TQZZ', 'path': '/', 'secure': False, 'value': 'GS1.1.1615105994.1.1.1615106039.15'}, {'domain': '.shopee.tw', 'expiry': 253402257600, 'httpOnly': False, 'name': 'G_ENABLED_IDPS', 'path': '/', 'secure': False, 'value': 'google'}, {'domain': '.shopee.tw', 'expiry': 1615109595.396044, 'httpOnly': False, 'name': 'SPC_CT_365a7def', 'path': '/', 'secure': False, 'value': '"1615105992.tlZmcLuQWDMHUlLC9rxVk7awj5cWAByQd9Nnc7CqhBQ="'}, {'domain': 'shopee.tw', 'expiry': 2245826039.822845, 'httpOnly': False, 'name': 'SPC_T_ID', 'path': '/', 'secure': False, 'value': '"rCQ14OVfIuRLgnaGNguVEO4OG2CiyPvh4wwzeDC3OIyIofdj1TZGonjXpFiAiqnaYQM8n9L1RrFj+WSOIMDJXwja+OFwkQhJZ2G1Snxkx+4="'}, {'domain': '.shopee.tw', 'expiry': 1615109595, 'httpOnly': False, 'name': 'AMP_TOKEN', 'path': '/', 'secure': False, 'value': '%24NOT_FOUND'}, {'domain': '.shopee.tw', 'expiry': 1615109595.263059, 'httpOnly': False, 'name': 'SPC_CT_0f1c6dc4', 'path': '/', 'secure': False, 'value': '"1615105992.pvPmdcn38KL58tu1yollSdHvS8JwRX1vzDGUvczX3Cs="'}, {'domain': '.shopee.tw', 'expiry': 1615192439.822856, 'httpOnly': True, 'name': 'SPC_SI', 'path': '/', 'secure': True, 'value': 'mall.bYdPq83KlgFNg81CItUmBFV1L3ldh9cK'}, {'domain': '.shopee.tw', 'expiry': 1615109639.694549, 'httpOnly': False, 'name': 'SPC_CT_7bea31a6', 'path': '/', 'secure': False, 'value': '"1615106036.qMgJ+/p+uIoTQbLbUg+1ibRtMy/tXu1xJz18XCVPtlg="'}, {'domain': '.shopee.tw', 'expiry': 2245825992.930627, 'httpOnly': False, 'name': 'SPC_F', 'path': '/', 'secure': True, 'value': 'LR5eKuO7jh71zd5iLWYiHqqO3R9zexjM'}, {'domain': '.shopee.tw', 'expiry': 1615109639.684481, 'httpOnly': False, 'name': 'SPC_CT_9ec38512', 'path': '/', 'secure': False, 'value': '"1615106036.5abgkfwLbAiElvtZlsG4P4Yvpq6obeNyI6c8Z+WvLIM="'}, {'domain': '.shopee.tw', 'expiry': 1622881993, 'httpOnly': False, 'name': '_gcl_au', 'path': '/', 'secure': False, 'value': '1.1.491808875.1615105993'}, {'domain': '.shopee.tw', 'expiry': 2245826039.711328, 'httpOnly': False, 'name': 'SPC_U', 'path': '/', 'secure': True, 'value': '390667155'}, {'domain': 'shopee.tw', 'expiry': 2245825992.930637, 'httpOnly': True, 'name': 'REC_T_ID', 'path': '/', 'secure': True, 'value': 'bf9f66d6-7f1f-11eb-8f32-b4969146213a'}, {'domain': '.shopee.tw', 'expiry': 2245826039.711293, 'httpOnly': True, 'name': 'SPC_EC', 'path': '/', 'secure': True, 'value': 'maaE96QfhUsho8p7QvmdOQO6jTdA/l2TiM1Ms5XBsRwMwrDfyDernlIuqKV45gGxxuGmxtIGtloxgTyXbR4PwxPxYUiQpLa/gWgDE7S+BC9RDXbFCNNB1AYhrc0jabkzLnttGOy0kEfAhvujunhWW94/jSqeBdQlW3U75a2k8dw='}, {'domain': '.shopee.tw', 'expiry': 1615192439, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.847838830.1615105995'}, {'domain': 'shopee.tw', 'expiry': 2245826038.66546, 'httpOnly': False, 'name': 'SPC_IA', 'path': '/', 'secure': False, 'value': '-1'}]

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
        list = []
        for i in range(0,5,1):
            home = redis_r.lpop('shopee_seller_homeurl')
            driver.execute_script("window.open(\'{}\')".format(home))
            list.append(home)
        time.sleep(1)
        handles = driver.window_handles[1:]
        handles.reverse()
        for i in handles:
            time.sleep(1)
            msg = os.getenv('message')
            driver.switch_to.window(i)
            message(driver,msg)
            time.sleep(1)
            try:
                no_send_sign = driver.find_element_by_class_name('src-components-MessageSectionLayout-ConversationMessages-BaseMessage-index__resend-wrap--1ufYm')
                for i in list:
                    redis_r.lpush('shopee_seller_homeurl',driver.current_url)
                print("聊聊功能已被封鎖")
                driver.quit()
            except:
                driver.close()
                continue
        driver.switch_to.window(driver.window_handles[0])
        if len(redis_r.lrange('shopee_seller_homeurl',0,-1)) == 0 :
            break
def message(driver,msg):
    while True :
        try:
            # 點聊聊
            element = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='shopee-button-outline shopee-button-outline--complement shopee-button-outline--fill shopee-button-outline-- ']"))).click()
            time.sleep(1)
            # 確認聊天室是否連到賣家
            seller_id = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='src-components-ConversationDetailLayout-BuyerProfile-index__name--1UP54']")))
            if len(seller_id.get_attribute('textContent')) != 0: # 表示有連到
                print("送訊息")
                m = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@class='src-components-ConversationDetailLayout-InputFieldLayout-ChatEditor-index__editor--3D_Zq']")))
                m.send_keys(msg)
                # Enter = driver.find_element_by_xpath("//*[@class='src-components-Common-ChatEditor-index__send-button--t-OKC']")
                # Enter.click()
                break
            else: # 未連線
                redis_r.lpush('shopee_seller_homeurl', driver.current_url)
                break
        except Exception as e:
            try:
                # 聊聊賣家未開啟 聊聊功能
                element = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@class='shopee-button-outline shopee-button-outline--complement shopee-button-outline--fill shopee-button-outline--disabled ']")))
                break
            except Exception as e:
                try:
                    element = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//*[@class='shopee-button-outline shopee-button-outline-- ']"))).click()
                    m = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@class='src-components-Common-ChatEditor-index__editor--2r1w5']")))
                    m.send_keys(msg)
                    break
                except:
                    redis_r.lpush('shopee_seller_homeurl', driver.current_url)
                    break
    return 'OK'

if __name__ == '__main__':
    threads = []
    for i in range(0,4,1):
        threads.append(threading.Thread(target=CrawlerSendChat, args=(cookie,)))
        time.sleep(1)
    for i in range(0,len(threads)):
        threads[i].start()

