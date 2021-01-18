import time

import pandas as pd
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction
from telegram.ext import CommandHandler, MessageHandler

from reservation_bot.reserve import get_price, CallbackQueryHandler
from reservation_bot.stock.service import get_code, get_download_kospi, get_download_kosdaq
from reservation_bot.stock.tasks import stock_task
from reservation_bot.telegrambot import TelegramBot

MY_TOKEN: str = "1584666157:AAFouodJILWqHk-9zS2WZ7msK9xJxJoRTCM"


class StockBot(TelegramBot):
    def __init__(self):
        self.token = MY_TOKEN
        TelegramBot.__init__(self, 'Stock', self.token)
        self.updater.stop()
        self.company_code = self.get_kosdaq_kospi()
        self.stock = list()

    def add_comm_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def add_message_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(MessageHandler(cmd, func))

    def add_handler(self, handler):
        self.updater.dispatcher.add_handler(handler)

    def keyword_handler(self, cmd, func):
        task_buttons = [[
            InlineKeyboardButton('60minutes', callback_data="3600")
            , InlineKeyboardButton('30minutes', callback_data="1800")
        ], [
            InlineKeyboardButton('10minutes', callback_data="10")
        ], [
            InlineKeyboardButton('cancel', callback_data="cancel")
        ]]

        show_markup = InlineKeyboardMarkup(task_buttons)  # make markup
        cmd.message.reply_text("원하는 값을 선택하세요",
                                                   reply_markup=show_markup)

    def tasks_keyword_handler(self, cmd, func):
        # self.stock.append()
        print(f"{cmd}" , func)


    def callback_button(self, cmd, context):
        query = cmd.callback_query
        data = query.data
        context.bot.send_chat_action(
            chat_id=cmd.effective_user.id
            , action=ChatAction.TYPING
        )
        context.bot.edit_message_text(
            text='[{}] 작업을 진행 하겠습니다.'.format(data)
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
        stock_task(query.message.message_id)



    def start(self):
        self.updater.start_polling(timeout=1, clean=True)
        self.updater.idle()

    def crawlering(self, cmd, func):

        print(f"요청한 stock: {cmd.message.text}")
        code = get_code(self.company_code, cmd.message.text)
        print(code)
        self.stock.append(code)
        if code.isdigit():
            self.crawler(code, cmd)
        else:
            self.exception_crawler(cmd)

    def crawler(self, company_code, cmd):
        price = get_price(company_code)

        if price:
            # result = {"가격": price, "시간 ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            price_string = self.convert_to_str(price)
            self.sendMessage(cmd.message.chat_id, f"{cmd.message.text}({company_code}) 주식\n {price_string}")

        else:
            self.exception_crawler(cmd)

    def exception_crawler(self, cmd):
        self.sendMessage(cmd.message.chat_id, f"한국 거래소에 없는 주식입니다.")

    @staticmethod
    def convert_to_str(price):
        print(price)
        price_string = ", \n".join(":".join((k, str(v))) for k, v in sorted(price.items()))
        return price_string

    @staticmethod
    def get_kosdaq_kospi():
        kospi_df = get_download_kospi()
        kosdaq_df = get_download_kosdaq()
        code_df = pd.concat([kospi_df, kosdaq_df])
        code_df = code_df[['회사명', '종목코드']]
        code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
        return code_df
