import requests
import random
import asyncio
import json

from fake_useragent import UserAgent
from playwright.async_api import async_playwright, BrowserContext

API_KEY = 'c89f64ef82-bd47afbe30-93e0257d03'


class SomeName:
    def __init__(self, headless=False):
        response = requests.get(f"https://proxy6.net/api/{API_KEY}/getproxy")
        data = response.json()
        self.ProxyList = []
        for item in data['list'].values():
            if item['user'] == 'QrTVm6':
                self.ProxyList.append({
                    'server': f'{item["ip"]}:{item["port"]}',
                    'username': item['user'],
                    'password': item['pass']
                })
        self.headless = headless
        self.RandomUrls = self.GetRandomUrls()

    @staticmethod
    def GetRandomUrls():
        with open('random_url.txt', 'r', encoding='utf-8') as file:
            return file.read().split('\n')

    async def SaveState(self):
        async def GetState(context: BrowserContext, proxy: dict):
            page = await context.new_page()
            try:
                await page.goto('https://www.avito.ru', wait_until='load')
            except:
                pass
            await page.wait_for_timeout(random.randint(5, 8) * 1000)
            x = random.uniform(-100, random.randint(2, 100))
            y = random.uniform(-93, random.randint(0, 18))
            await page.mouse.move(x, y)
            try:
                await page.goto(random.choice(self.RandomUrls), wait_until='load')
            except:
                pass
            try:
                await page.wait_for_load_state('load')
            except:
                pass
            await page.wait_for_timeout(random.randint(15, 20) * 1000)
            state = await context.storage_state()
            await page.close()
            return {
                **proxy, **state
            }

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless, proxy={'server': 'http://somesite'})

            tasks = []
            for proxy in self.ProxyList:
                context = await browser.new_context(proxy=proxy)
                task = asyncio.create_task(GetState(context, proxy))
                tasks.append(task)

            result = await asyncio.gather(*tasks)
            for idx, cookie in enumerate(result):
                with open(f"cookies_{idx}.json", 'w', encoding='utf-8') as file:
                    json.dump(cookie, file, indent=4, ensure_ascii=False)


obj = SomeName(False)
asyncio.run(obj.SaveState())

idx = 2 #random.randint(0, 2)
with open(f'cookies_{idx}.json', 'r', encoding='utf-8') as file:
    d = json.load(file)

proxy = "http://{}:{}@{}".format(d['username'], d['password'], d['server'])
print(proxy)
proxies = {
    'http': proxy,
    'https': proxy
}
ua = UserAgent().random

cookies = {
    i['name']: i['value'] for i in d['cookies']
}

response = requests.get(
    url='https://www.avito.ru',
    headers={'user-agent': ua},
    cookies=cookies,
    proxies=proxies
)
print(response.status_code)
