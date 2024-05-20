import requests
import random
import time
import asyncio
import json
import logging
import re

from fake_useragent import UserAgent
from playwright.async_api import async_playwright, BrowserContext

logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG, encoding='utf-8')

API_KEY = 'c89f64ef82-bd47afbe30-93e0257d03'


class AvitoParser():
    def __init__(
        self,
        InputURLs: list[str] = [],
        headless: bool = False,
        sleepSeconds: int = 600,
    ):
        self.urls = InputURLs
        self.ProxyListForContext = self.GetProxy()
        self.ProxyListForRequest = [
            {
                'http': f"http://{proxy['username']}:{proxy['password']}@{proxy['server']}",
                'https': f"http://{proxy['username']}:{proxy['password']}@{proxy['server']}"
            } for proxy in self.ProxyListForContext]
        self.headless = headless
        self.RandomUrls = self.GetRandomUrls()
        self.logger = logging.getLogger('AvitoParser')
        self.sleepSeconds = sleepSeconds

    @staticmethod
    def ReadCookies():
        with open('cookies.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def WriteCookies(CookiesList : list[dict]):
        with open('cookies.json', 'w', encoding='utf-8') as file:
            json.dump(
                obj=CookiesList,
                fp=file,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def GetRandomUrls():
        with open('random_url.txt', 'r', encoding='utf-8') as file:
            return file.read().split('\n')

    @staticmethod
    def GetProxy():
        response = requests.get(f"https://proxy6.net/api/{API_KEY}/getproxy")   
        data = response.json()
        result = []
        for item in data['list'].values():
            result.append({
                'server': f'{item["ip"]}:{item["port"]}',
                'username': item['user'],
                'password': item['pass']
            })
        return result

    async def WorkWithCookies(self):
        async def GetCookies(context:BrowserContext, init: bool = True):
            page = await context.new_page()
            if init:
                await page.goto('https://www.google.com', wait_until='load')
                await page.wait_for_timeout(2 * 1000)
                await page.get_by_title('Поиск').fill('avito')
                await page.keyboard.press('Enter')
                await page.wait_for_timeout(3 * 1000)
                await page.get_by_role("link", name="Авито: недвижимость, транспорт, работа, услуги, вещи Авито https://www.avito.ru").click()
                await page.wait_for_timeout(5 * 1000)
                # try:
                #     await page.goto('https://www.avito.ru', wait_until='domcontentloaded')
                # except Exception as _ex:
                #     self.logger.error('Получили ошибку {}'.format(_ex), exc_info=1)
                # for _ in range(5):
                #     await page.goto(random.choice(self.RandomUrls), wait_until='commit')
                #     await page.wait_for_timeout(random.randint(5, 12) * 1000)
            else:
                try:
                    await page.goto(random.choice(self.RandomUrls), wait_until='load')
                except Exception as __ex:
                    self.logger.error('Получили ошибку {}'.format(__ex), exc_info=1)
                
                await page.wait_for_timeout(random.randint(3, 4) * 1000)
            cookies = {
                item['name'] : item['value'] for item in (await context.cookies())
            }
            await page.close()
            return cookies

        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=self.headless)
            contexts = [
                await browser.new_context(proxy=proxy) for proxy in self.ProxyListForContext[:1]
            ]
            tasks = []
            for context in contexts:
                task = asyncio.create_task(GetCookies(context))
                tasks.append(task)

            await asyncio.gather(*tasks)

            while True:
                tasks = []
                for context in contexts:
                    task = asyncio.create_task(GetCookies(context, init=False))
                    tasks.append(task)
                
                self.WriteCookies(await asyncio.gather(*tasks))
                self.logger.info('Мы обновили cookies, спим {} секунд'.format(self.sleepSeconds))
                await asyncio.sleep(self.sleepSeconds)
                self.WriteCookies([])

    async def GetHtml(self):
        idx = 0
        while self.urls:
            CookiesList = self.ReadCookies()
            if CookiesList == []:
                await asyncio.sleep(40)
            else:
                for cookies, proxies in zip(CookiesList, self.ProxyListForRequest):
                    if self.urls:
                        url = self.urls.pop()
                        response = requests.get(
                            url=url,
                            cookies=cookies,
                            proxies=proxies,
                            headers={'user-agent' : UserAgent().random}
                        )
                        print(response.status_code)
                        if response.ok:
                            self.logger.debug('Статус код: {} | URL: {}'.format(response.status_code, response.url))
                            with open(f'html/{idx}.html', 'w', encoding='utf-8') as file:
                                file.write(response.text)
                            self.logger.debug('Мы записали HTML с {} в html/{}.html'.format(response.url, idx))
                            idx += 1
                        else:
                            self.logger.debug('Статус код: {} | URL: {}'.format(response.status_code, response.url))
                            self.urls.append(url)
                        await asyncio.sleep(random.randint(1, 2))
                    else:
                        break

    async def run(self):
        self.WriteCookies([])
        await asyncio.gather(
            self.GetHtml(),
            self.WorkWithCookies()
        )


with open('input_urls.txt', 'r', encoding='utf-8') as file:
    urls = [url for url in file.read().split('\n') if url != ''] * 4


parser = AvitoParser(InputURLs=urls, sleepSeconds=3600, headless=False)
asyncio.run(parser.run())
