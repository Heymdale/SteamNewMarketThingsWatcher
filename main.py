import asyncio
import os

from aiogram import Bot
import aiohttp
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from loguru import logger

from request_headers import headers

TRIES = 6
URL = 'https://steamcommunity.com/market/search?q=&category_3231090_inventory_type%5B%5D=tag_crate&appid=3231090'

load_dotenv()
logger.add('log.txt', rotation='10 MB')

async def send_message(message):
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=message)

async def main():
    async with aiohttp.ClientSession() as session:
        for i in range(TRIES):
            try:
                async with session.get(URL, headers=headers) as response:
                    html = await response.text()
                    soup = bs(html, 'lxml')
                    search_results_div = soup.find(id='searchResultsRows')
                    print(f'{search_results_div=}')
                    count_elements = len(search_results_div.find_all('a', class_='market_listing_row_link'))
                    print(f'{count_elements=}')
                    if count_elements == 0:
                        raise Exception('No elements was found')
                    elif count_elements > 4:
                        await send_message(f'!!!AHTUNG!!!\n ButtSlapper added new crate!!!')
                    break
            except Exception as e:
                if i == TRIES - 1:
                    await send_message(
                        f'!!!WARNING!!!\n Can\'t get list of buttslapper crates.'
                    )
                    break
                logger.error(e)
                await asyncio.sleep((i+1)^2 * 10)


if __name__ == '__main__':
    asyncio.run(main())
