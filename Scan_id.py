from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import os, requests, asyncio, aiohttp , redis , time , logging
from datetime import datetime

load_dotenv(encoding="utf-8")
redis_r = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_POST'), db=os.getenv('REDIS_DB'),
                            decode_responses=True)

async def seller_home():
    timeout = aiohttp.ClientTimeout()
    async with aiohttp.ClientSession(timeout=timeout) as session:
        while True:
            seller_id = redis_r.lpop("Shopee_seller_id")
            if seller_id == None: ## id掃完為None時跳出迴圈
                print('全部的id已掃描完成')
                break
            try:
                url = 'https://shopee.tw/shop/{}/search'.format(seller_id)
                headers = {
                    'User-Agent': 'Googlebot'
                }
                while True:
                    async with session.get(url, headers = headers) as r:
                        text = await r.text()
                        soup = BeautifulSoup(text ,'html.parser')
                        soup = soup.find_all('a',class_='shopee-seller-portrait__avatar')
                        if len(soup) > 0:
                            href = soup[0].get('href')
                            url = urljoin(url, href)
                            print("完成了"+str(url))
                            redis_r.rpush('shopee_seller_homeurl', url)
                            break
                        if len(soup) == 0:
                            await asyncio.sleep(3)
            except Exception as e:
                print(e)
                redis_r.rpush('shopee_error_seller_id', seller_id)
    return "ok"
start = datetime.now()
loop = asyncio.get_event_loop()
tasks = []
for i in range(0,50,1):
    tasks.append(loop.create_task(seller_home()))
loop.run_until_complete(asyncio.wait(tasks))
end = datetime.now()
print("花費幾秒:"+str((end-start).seconds))