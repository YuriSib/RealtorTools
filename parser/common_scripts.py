import requests
import random

from config import API_KEY


def get_proxy_list():
    response = requests.get(f"https://proxy6.net/api/{API_KEY}/getproxy")
    data = response.json()
    proxy_list = []
    for item in data['list'].values():
        proxy_list.append({
            'server': f'{item["ip"]}:{item["port"]}',
            'username': item['user'],
            'password': item['pass']
        })
    return proxy_list


# hidden_start заходит на главную страницу используя контекст, релает рандомные движения курсром,
            # возвращает page
async def hidden_start(context):
    page = await context.new_page()
    try:
        await page.goto('https://www.avito.ru/all/nedvizhimost', wait_until='load')
    except:
        pass
    await page.wait_for_timeout(random.randint(5, 8) * 1000)
    x = random.uniform(-100, random.randint(2, 100))
    y = random.uniform(-93, random.randint(0, 18))
    await page.mouse.move(x, y)

    return page


print(get_proxy_list())
