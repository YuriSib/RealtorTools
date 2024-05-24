import requests
import random
import asyncio
import json

from fake_useragent import UserAgent
from playwright.async_api import async_playwright, BrowserContext

from parser.common_scripts import get_proxy_list, hidden_start


async def get_avito_url(primary_url):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        proxy_list = get_proxy_list()

        idx = random.randint(a=0, b=len(proxy_list))
        context = await browser.new_context(proxy=proxy_list[idx])
        page = await hidden_start(context)


# tasks = []
# task = asyncio.create_task(get_url())
# tasks.append(task)
# result = asyncio.gather(*tasks)
