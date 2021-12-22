import urllib.parse
import re
import asyncio
import aiohttp
from random import randint
import aiofiles

async def main(url):
    url = await resolve_link(url)
    cookie,token = await get_data()
    video_url = await get_video_url(url,cookie,token)
    item_name = randint(1,1000000)
    await download_item(video_url,item_name)

async def resolve_link(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return str(resp.url)

async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ttdownloader.com/") as resp:
            if resp.status == 200:
                cookie = resp.headers['set-cookie']
                html = await resp.text()
                match = re.search(r"<input type=\"hidden\" id=\"token\" name=\"token\"[^>]*value=\"([^ ]+)\"", html, re.MULTILINE)
                token = match.group(1)
            return cookie,token

async def get_video_url(url,cookie,token):
    datapost = urllib.parse.urlencode({"url" : url,"format": '',"token": token})
    headers = {
        'Cookie': cookie,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ttdownloader.com',
        'referer': 'https://ttdownloader.com',
              }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://ttdownloader.com/req/", data = datapost, headers = headers) as resp:
            html = await resp.text()
            url = re.search(r"href=\"([^ ]+)\"", html)
            return url.group(1)


async def download_item(video_url,item_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as resp:
            f = await aiofiles.open(f'./files/{item_name}.mp4', mode='wb')
            await f.write(await resp.read())
            await f.close()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #URL HERE!!!!
    url = ''
    asyncio.run(main(url))