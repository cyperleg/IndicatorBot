import plotly.graph_objects as go


class CandlestickPattern:
    def __init__(self, plot):
        self.plot = plot

    def avg_value(self):
        list_avg_symbols = []
        for k in range(400):
            list_avg_symbols.append(float(self.plot.klines[-k][2]))
        avg_val = (max(list_avg_symbols) - min(list_avg_symbols)) / 400
        return avg_val

    def bull_trand_hammer(self):

        #      optionable params

        """
        BIAS = 2
        BIAS_BODY = 3
        BIAS_HEAD = 0.8
        BIAS_FOOT = 1
        BIAS_VOLUME = 0.001

        !!!    1    !!!
        BIAS = 1.65
        BIAS_BODY = 2.85
        BIAS_HEAD = 0.95
        BIAS_FOOT = 0.78
        BIAS_VOLUME = 0.0019
        """

        #       for bigger timeframe(2h, 4h)

        BIAS = 1.7
        BIAS_BODY = 2.6
        BIAS_HEAD = 0.75
        BIAS_FOOT = 0.7
        BIAS_VOLUME = 0.007

        i = 0

        #####
        avg = self.avg_value()
        print(f'    1_avarage = {avg}')
        while i < len(self.plot.klines):

            body = abs(self.plot.klines[i][1] - self.plot.klines[i][4])
            if float(self.plot.klines[i][1]) > float(self.plot.klines[i][4]):  # open > close  (k_red)
                low_shadow = abs(self.plot.klines[i][3] - self.plot.klines[i][4])
                high_shadow = abs(self.plot.klines[i][2] - self.plot.klines[i][1])
                BIAS += 0.2
            else:  # close > open (k_green)
                low_shadow = abs(self.plot.klines[i][3] - self.plot.klines[i][1])
                high_shadow = abs(self.plot.klines[i][2] - self.plot.klines[i][4])
            if (body / avg) >= BIAS_BODY:
                weight = BIAS_FOOT * (low_shadow / body) - BIAS_HEAD * (high_shadow / body) + BIAS_VOLUME * (
                            abs(self.plot.klines[i][2] - self.plot.klines[i][3]) / avg)
                if weight - BIAS >= 0:
                    self.plot.fig.add_trace(
                        go.Scatter(x=[self.plot.klines[i][0]], y=[float(self.plot.klines[i][3]) - avg * 2], mode='markers', name='markers',
                                   marker=go.Marker(size=10, symbol='triangle-up', color='blue'),
                                   row=self.row, col=self.col))
                    print(i, self.plot.klines[i][0], weight)
            i += 1
            BIAS = 1.7
            #     BIAS = 1.65

    def bear_trand_hammer(self):

        #      optionable params

        BIAS = 1.65
        BIAS_BODY = 2
        BIAS_HEAD = 0.78
        BIAS_FOOT = 0.7
        BIAS_VOLUME = 0.0073

        #####

        body, low_shadow, high_shadow, weight = 0, 0, 0, 0
        avg = self.avg_value()
        i = 0
        print('    2_avarage=', avg)
        while i < len(self.plot.klines):

            body = abs(self.plot.klines[i][1] - self.plot.klines[i][4])
            if float(self.plot.klines[i][1]) > float(self.plot.klines[i][4]):  # open > close  (k_red)
                low_shadow = abs(self.plot.klines[i][2] - self.plot.klines[i][1])
                high_shadow = abs(self.plot.klines[i][4] - self.plot.klines[i][3])
            else:  # close > open (k_green)
                low_shadow = abs(self.plot.klines[i][2] - self.plot.klines[i][4])
                high_shadow = abs(self.plot.klines[i][4] - self.plot.klines[i][3])
            if (body / avg) >= BIAS_BODY:
                weight = BIAS_FOOT * (low_shadow / body) - BIAS_HEAD * (high_shadow / body) + BIAS_VOLUME * (
                            abs(self.plot.klines[i][2] - self.plot.klines[i][3]) / avg)
                if weight - BIAS >= 0:
                    self.plot.fig.add_trace(go.Scatter(x=[self.plot.klines[i][0]], y=[(float(self.plot.klines[i][2])) + avg * 2], mode='markers',
                                             name='markers',
                                             marker=go.Marker(size=10, symbol='triangle-down', color='#ff85fa'),
                                             row=self.row, col=self.col))
                    print(i, self.plot.klines[i][0], weight)
            i += 1