import time
import telebot
from Plot import Plot

limit = 100

cnf = [
    ('BTCUSDT', 'KLINE_INTERVAL_15MINUTE'),
    ('BTCUSDT', 'KLINE_INTERVAL_30MINUTE'),
    ('BTCUSDT', 'KLINE_INTERVAL_1HOUR'),
    ('BTCUSDT', 'KLINE_INTERVAL_2HOUR'),
    ('BTCUSDT', 'KLINE_INTERVAL_4HOUR'),
    ('BTCUSDT', 'KLINE_INTERVAL_6HOUR'),
    ('BTCUSDT', 'KLINE_INTERVAL_1DAY'),
    ('ETHUSDT', 'KLINE_INTERVAL_15MINUTE'),
    ('ETHUSDT', 'KLINE_INTERVAL_30MINUTE'),
    ('ETHUSDT', 'KLINE_INTERVAL_1HOUR'),
    ('ETHUSDT', 'KLINE_INTERVAL_2HOUR'),
    ('ETHUSDT', 'KLINE_INTERVAL_4HOUR'),
    ('ETHUSDT', 'KLINE_INTERVAL_6HOUR'),
    ('ETHUSDT', 'KLINE_INTERVAL_1DAY'),
    ('ADAUSDT', 'KLINE_INTERVAL_15MINUTE'),
    ('ADAUSDT', 'KLINE_INTERVAL_30MINUTE'),
    ('ADAUSDT', 'KLINE_INTERVAL_1HOUR'),
    ('ADAUSDT', 'KLINE_INTERVAL_2HOUR'),
    ('ADAUSDT', 'KLINE_INTERVAL_4HOUR'),
    ('ADAUSDT', 'KLINE_INTERVAL_6HOUR'),
    ('ADAUSDT', 'KLINE_INTERVAL_1DAY'),
    ('GALAUSDT', 'KLINE_INTERVAL_1DAY'),
    ('KAVAUSDT', 'KLINE_INTERVAL_1DAY'),
    ('ETCUSDT', 'KLINE_INTERVAL_1DAY'),
    ('LINKUSDT', 'KLINE_INTERVAL_1DAY'),
    ('SOLUSDT', 'KLINE_INTERVAL_1DAY'),
    ('XMRUSDT', 'KLINE_INTERVAL_1DAY'),
    ('TRXUSDT', 'KLINE_INTERVAL_1DAY'),

]

temp = [0 for x in cnf]


bot = telebot.TeleBot('5564033711:AAEqKjUX0lbnAU8g562EqA3Bs-eWHEpPktc')


chat_id = -637481791


while True:
    plot = [Plot(x[0], x[1], limit) for x in cnf]
    for j, i in enumerate(plot):
        time.sleep(1)
        i.create_base_plot()
        i.init_ind()
        i.init_diver()
        i.ind.create_MACD()
        i.diver.create_pivot()
        k = i.diver.find_diver_lower(candlestick_limit=7)
        if k and k != temp[j]:
            bot.send_message(chat_id, f'{i.name} {i.interval.split("_")[-1]}\n{k}\nlower diver')
            temp[j] = k
        k = i.diver.find_diver_upper(candlestick_limit=7)
        if k and k != temp[j]:
            bot.send_message(chat_id, f'{i.name} {i.interval.split("_")[-1]}\n{k}\nupper diver')
            temp[j] = k

    time.sleep(900)
