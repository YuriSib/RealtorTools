import requests
import random
import asyncio
import json

from fake_useragent import UserAgent
from playwright.async_api import async_playwright, BrowserContext

from common_scripts import get_proxy_list, hidden_start


class SomeName:
    def __init__(self, headless=False):
        self.ProxyList = get_proxy_list()
        self.headless = headless
        self.RandomUrls = self.GetRandomUrls()

    @staticmethod
    def GetRandomUrls():
        with open('random_url.txt', 'r', encoding='utf-8') as file:
            return file.read().split('\n')

    async def SaveState(self):
        async def GetState(context: BrowserContext, proxy: dict):
            page = await hidden_start(context)
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
            browser = await p.firefox.launch(headless=self.headless)

            tasks = []
            for proxy in self.ProxyList:
                context = await browser.new_context(proxy=proxy)
                task = asyncio.create_task(GetState(context, proxy))
                tasks.append(task)

            result = await asyncio.gather(*tasks)
            for idx, cookie in enumerate(result):
                with open(f"cookies/cookies_{idx}.json", 'w', encoding='utf-8') as file:
                    json.dump(cookie, file, indent=4, ensure_ascii=False)


# obj = SomeName(False)
# asyncio.run(obj.SaveState())

# idx = 0#random.randint(0, 2)
for idx in range(6):
    print(idx)
    with open(f'cookies/cookies_{idx}.json', 'r', encoding='utf-8') as file:
        d = json.load(file)

    proxy = "http://{}:{}@{}".format(d['username'], d['password'], d['server'])
    print(proxy)
    proxies = {
        'http': proxy,
        'https': proxy
    }
    ua = UserAgent().random
    print(d['cookies'])
    cookies = {
        i['name']: i['value'] for i in d['cookies']
    }
    print(cookies)

    response = requests.get(
        url='https://www.avito.ru',
        headers={'user-agent': ua},
        cookies=cookies,
        proxies=proxies
    )
    print(response.status_code)
