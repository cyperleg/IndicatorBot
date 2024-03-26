import numpy as np


class Divergenses:
    def __init__(self, data, fig):
        self.data = data
        self.fig = fig
        self.row_main = 1
        self.col_main = 1
        self.row_macd = 2
        self.col_macd = 1
        self.num_candles = 100
        self.__last = [0, 0]

    def create_vis(self, time_1, time_2, y_1_1, y_1_2, y_2_1, y_2_2):
        self.fig.add_shape(type="line",
                                x0=time_1, y0=y_1_1,
                                x1=time_2, y1=y_1_2,
                                line=dict(color="purple", width=3),
                                row=self.row_main, col=self.col_main
                                )
        self.fig.add_shape(type="line",
                                x0=time_1, y0=y_2_1,
                                x1=time_2, y1=y_2_2,
                                line=dict(color="purple", width=3),
                                row=self.row_macd, col=self.col_macd
                                )

    @staticmethod
    def MACD_signalpivotid(data, l, n1, n2):  # n1 n2 before and after candle l
        if l - n1 < 0 or l + 2 >= len(data['MACD_signal']):
            return 0

        pividlow = 1
        pividhigh = 1
        if l + n2 + 1 > len(data['MACD_signal']):
            for i in range(l - n1, l + (len(data['MACD_signal'])) - l):
                if (data['MACD_signal'][l] > data['MACD_signal'][i]):
                    pividlow = 0
                if (data['MACD_signal'][l] < data['MACD_signal'][i]):
                    pividhigh = 0
        else:
            for i in range(l - n1, l + n2 + 1):
                if (data['MACD_signal'][l] > data['MACD_signal'][i]):
                    pividlow = 0
                if (data['MACD_signal'][l] < data['MACD_signal'][i]):
                    pividhigh = 0
        if pividlow and pividhigh:
            return 3
        elif pividlow and data['MACD_signal'][l] <= 0:
            if l + 2 + 1 > len(data['MACD_signal']):
                for i in range(l - 2, l + (len(data['MACD_signal'])) - l):
                    if not (data['MACD_signal'][l] < 0 and data['MACD_signal'][i] < 0):
                        return 4
            else:
                for i in range(l - 2, l + 2 + 1):
                    if not (data['MACD_signal'][l] < 0 and data['MACD_signal'][i] < 0):
                        return 4
            return 1
        elif pividhigh and data['MACD_signal'][l] > 0:
            if l + 2 + 1 > len(data['MACD_signal']):
                for i in range(l - 2, l + (len(data['MACD_signal'])) - l):
                    if not (data['MACD_signal'][l] > 0 and data['MACD_signal'][i] > 0):
                        return 5
            else:
                for i in range(l - 2, l + 2 + 1):
                    if not (data['MACD_signal'][l] > 0 and data['MACD_signal'][i] > 0):
                        return 5
            return 2
        else:
            return 0

    @staticmethod
    def MACD_signalpointpos(x):
        if x['MACD_signalpivot'] == 1:
            return x['MACD_signal']
        elif x['MACD_signalpivot'] == 2:
            return x['MACD_signal']
        elif x['MACD_signalpivot'] == 4:
            return x['MACD_signal']
        elif x['MACD_signalpivot'] == 5:
            return x['MACD_signal']
        else:
            return np.nan


    def calculate_cross(self):
        temp = False
        for j in range(5,21):
            for i in range(len(self.data['open_time'])-self.num_candles, len(self.data['open_time']), j):
                if (self.data['MACD_fast'][i] <= self.data['MACD_slow'][i] and self.data['MACD_fast'][i-1] >= self.data['MACD_slow'][i-1]) or \
                    (self.data['MACD_fast'][i] >= self.data['MACD_slow'][i] and self.data['MACD_fast'][i-1] <= self.data['MACD_slow'][i-1]):
                    if not temp:
                        temp = i
                    else:

                        # calculating avr position between slow and fast
                        avr_1 = min(self.data['MACD_fast'][i], self.data['MACD_slow'][i]) + abs(
                            self.data['MACD_fast'][i] - self.data['MACD_slow'][i])
                        avr_2 = min(self.data['MACD_fast'][temp], self.data['MACD_slow'][temp]) + abs(
                            self.data['MACD_fast'][temp] - self.data['MACD_slow'][temp])

                        # maxmin2 candle
                        avr_candle_1 = (self.data['high'][i] + self.data['low'][i])/2
                        avr_candle_2 = (self.data['high'][temp] + self.data['low'][temp])/2



                        # bullish trand
                        if avr_2 < avr_1 and avr_candle_2 > avr_candle_1:
                            self.create_vis(self.data['open_time'][i], self.data['open_time'][temp],
                                            avr_candle_1, avr_candle_2, avr_1, avr_2)

                        # bearish trand
                        elif avr_2 > avr_1 and avr_candle_2 < avr_candle_1:
                            self.create_vis(self.data['open_time'][i], self.data['open_time'][temp],
                                            avr_candle_1, avr_candle_2, avr_1, avr_2)

                        temp = i


    def create_pivot(self):
        self.data['MACD_signalpivot'] = self.data.apply(
            lambda x: Divergenses.MACD_signalpivotid(self.data, x.name, 5, 5), axis=1)
        print(*self.data['MACD_signalpivot'])
        self.data['MACD_signalpointpos'] = self.data.apply(lambda row: Divergenses.MACD_signalpointpos(row), axis=1)
        self.fig.add_scatter(x=self.data.open_time, y=self.data.MACD_signalpointpos, mode="markers",
                                  marker=dict(size=5, color="Black"), name="MACD_signalpivot", row=2, col=1)

    def find_diver_lower(self, limit=False, candlestick_limit=7):
        temp = False
        if not limit:
            limit = len(self.data['MACD_signalpivot'])
        for i in range(len(self.data['MACD_signalpivot']) - limit, len(self.data['MACD_signalpivot']) - 1):
            if self.data['MACD_signalpivot'][i] == 1:
                if not temp:
                    temp = i
                else:
                    for j in range(temp, i + 1):
                        if self.data['MACD_signalpivot'][j] == 2 or self.data['MACD_signalpivot'][j] == 5:
                            # maxmin2 candle
                            avr_candle_1 = (self.data['high'][i] + self.data['low'][i]) / 2
                            avr_candle_2 = (self.data['high'][temp] + self.data['low'][temp]) / 2

                            print("--------------------")
                            print(avr_candle_2, avr_candle_1, self.data['MACD_signal'][temp],
                                  self.data['MACD_signal'][i], temp, i)
                            print(self.data['MACD_signal'][temp] < self.data['MACD_signal'][i],
                                  avr_candle_2 > avr_candle_1)
                            print(self.data['MACD_signal'][temp] > self.data['MACD_signal'][i],
                                  avr_candle_2 < avr_candle_1)

                            if (self.data['MACD_signal'][temp] < self.data['MACD_signal'][i]
                                and avr_candle_2 > avr_candle_1) or \
                                (self.data['MACD_signal'][temp] > self.data['MACD_signal'][i] and
                                avr_candle_2 < avr_candle_1):
                                #print(f'i={i}, temp={temp}, {limit - i <= candlestick_limit}')
                                if limit - i <= candlestick_limit:

                                    res = f"{self.data['open_time'][temp]}  {self.data['open_time'][i]}"

                                    if res != self.__last[0]:
                                        self.create_vis(self.data['open_time'][i], self.data['open_time'][temp],
                                                        avr_candle_1, avr_candle_2,
                                                        self.data['MACD_signalpointpos'][i],
                                                        self.data['MACD_signalpointpos'][temp])

                                        self.__last[0] = res

                                        return res
                    temp = i

        return False

    def find_diver_upper(self, limit=False, candlestick_limit=7):
        temp = False
        if not limit:
            limit = len(self.data['MACD_signalpivot'])
        for i in range(len(self.data['MACD_signalpivot']) - limit, len(self.data['MACD_signalpivot']) - 1):
            if self.data['MACD_signalpivot'][i] == 2:
                if not temp:
                    temp = i
                else:
                    for j in range(temp, i + 1):
                        if self.data['MACD_signalpivot'][j] == 1 or self.data['MACD_signalpivot'][j] == 4:
                            # maxmin2 candle
                            avr_candle_1 = (self.data['high'][i] + self.data['low'][i]) / 2
                            avr_candle_2 = (self.data['high'][temp] + self.data['low'][temp]) / 2

                            print("--------------------")
                            print(avr_candle_2, avr_candle_1, self.data['MACD_signalpivot'][temp], self.data['MACD_signalpivot'][i], temp, i)
                            print(self.data['MACD_signalpivot'][temp] < self.data['MACD_signalpivot'][i], avr_candle_2 > avr_candle_1)
                            print(self.data['MACD_signalpivot'][temp] > self.data['MACD_signalpivot'][i],
                                avr_candle_2 < avr_candle_1)

                            if (self.data['MACD_signal'][temp] < self.data['MACD_signal'][i]
                                and avr_candle_2 > avr_candle_1) or \
                                (self.data['MACD_signal'][temp] > self.data['MACD_signal'][i] and
                                avr_candle_2 < avr_candle_1) and limit - temp <= candlestick_limit:
                                if limit - i <= candlestick_limit:
                                    res = f"{self.data['open_time'][temp]}  {self.data['open_time'][i]}"

                                    if res != self.__last[1]:

                                        self.create_vis(self.data['open_time'][i], self.data['open_time'][temp],
                                                        avr_candle_1, avr_candle_2,
                                                        self.data['MACD_signalpointpos'][i],
                                                        self.data['MACD_signalpointpos'][temp])

                                        self.__last[1] = res

                                        return res
                    temp = i

        return False

