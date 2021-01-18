

import asyncio

from reservation_bot.telegrambot import TelegramBot


zz = "te"
async def stock_task(id):
    # telegram = TelegramBot
    print("hi"+ str(id))

loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
# loop.run_until_complete(stock_task(id))  # hello가 끝날 때까지 기다림
# loop.close()