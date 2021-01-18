import requests
from bs4 import BeautifulSoup
from telegram.ext import *

from reservation_bot.stock import stockBot


def get_price(company_code):
    url = 'https://finance.naver.com/item/main.nhn?code=' + str(company_code)
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})
    now_price = blind.text
    chart = get_candle_chart(bs_obj)
    if chart:
        chart['현재가'] = now_price

    return chart


def get_candle_chart(bs_obj):
    td_first = bs_obj.find("td", {"class": "first"})  # 태그 td, 속성값 first 찾기
    blind = td_first.find("span", {"class": "blind"})  # 태그 span, 속성값 blind 찾기
    close = blind.text

    # high 고가
    table = bs_obj.find("table", {"class": "no_info"})  # 태그 table, 속성값 no_info 찾기
    trs = table.find_all("tr")  # tr을 list로 []
    first_tr = trs[0]  # 첫 번째 tr 지정
    tds = first_tr.find_all("td")  # 첫 번째 tr 안에서 td를 list로
    second_tds = tds[1]  # 두 번째 td 지정
    high = second_tds.find("span", {"class": "blind"}).text

    # open 시가
    second_tr = trs[1]  # 두 번째 tr 지정
    tds_second_tr = second_tr.find_all("td")  # 두 번째 tr 안에서 td를 list로
    first_td_in_second_tr = tds_second_tr[0]  # 첫 번째 td 지정

    open = first_td_in_second_tr.find("span", {"class": "blind"}).text

    # low 저가
    second_td_in_second_tr = tds_second_tr[1]  # 두 번째 td 지정
    low = second_td_in_second_tr.find("span", {"class": "blind"}).text

    return {"종가(전일)": close, "고가": high, "시가": open, "저가": low}


if __name__ == "__main__":
    stock_bot = stockBot.StockBot()
    stock_bot.add_comm_handler('start', stock_bot.start)
    stock_bot.add_comm_handler('stop', stock_bot.stop)
    stock_bot.add_comm_handler('time', stock_bot.keyword_handler)

    stock_bot.add_comm_handler('task', stock_bot.keyword_handler)

    stock_bot.add_message_handler(Filters.text, stock_bot.crawlering)
    button_callback_handler = CallbackQueryHandler(stock_bot.callback_button)
    stock_bot.add_handler(button_callback_handler)
    stock_bot.start()


# def crawler(company_code, maxpage):
#     page = 1
#     while page <= int(maxpage):

# url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page)
# source_code = requests.get(url).text
# html = BeautifulSoup(source_code, "lxml")
# bs_obj = BeautifulSoup(source_code, "html.parser")

# 뉴스 제목
# titles = html.select('.title')
# title_result = []
# for title in titles:
#     title = title.get_text()
#     title = re.sub('\n', '', title)
#     title_result.append(title)

# 뉴스 링크
# links = html.select('.title')
#
# link_result = []
# for link in links:
#     add = 'https://finance.naver.com' + link.find('a')['href']
#     link_result.append(add)

# 뉴스 날짜
# dates = html.select('.date')
# date_result = [date.get_text() for date in dates]

# 뉴스 매체
# sources = html.select('.info')
# source_result = [source.get_text() for source in sources]

# 변수들 합쳐서 해당 디렉토리에 csv파일로 저장하기
# price = get_price(company_code)
# result = {"가격": price, "시간 ": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# {"날짜": date_result, "언론사": source_result, "기사제목": title_result, "링크": link_result}
# df_result = pd.DataFrame(result)
#
# print("다운 받고 있습니다------")
# df_result.to_csv('page' + str(page) + '.csv', mode='w', encoding='utf-8-sig')

# page += 1
# # updates = chatbot.getUpdates()
# chat_id = chatbot.getUpdates()[-1].message.chat.id
# chatbot.sendMessage(chat_id=chat_id, text=f"삼성전자({company_code}) 주식 : {result}")


# def start(bot, update):
#     bot.sendMessage(chat_id=update.message.chat_id, text="아녕하떼요")


# def exception_crawler():
#     bot.sendMessage(chat_id=1, text=f"한국 거래소에 없는 주식입니다.")
