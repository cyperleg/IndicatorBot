import talib
import plotly.graph_objects as go


class Indicators:
    def __init__(self, data, fig):
        self.data = data
        self.fig = fig

    def create_MACD(self, fastperiod=12, slowperiod=26, signalperiod=9, diagram=False):
        self.data['MACD_fast'], self.data['MACD_slow'], self.data['MACD_signal'] = talib.MACD(
            self.data.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod
        )

        macd_trace_fast = go.Scatter(x=self.data.open_time, y=self.data.MACD_fast, mode="lines", name="macd_fast")
        macd_trace_slow = go.Scatter(x=self.data.open_time, y=self.data.MACD_slow, mode="lines", name="macd_slow")
        if diagram:
            for i, d in enumerate(self.data['open_time']):
                if self.data['MACD_signal'][i] > 0:
                    self.fig.add_shape(type="line",
                                            x0=d, y0=0, x1=d, y1=self.data['MACD_signal'][i],
                                            line=dict(color='green', width=3),
                                            row=2, col=1
                                            )
                else:
                    self.fig.add_shape(type="line",
                                            x0=d, y0=0, x1=d, y1=self.data['MACD_signal'][i],
                                            line=dict(color='red', width=3),
                                            row=2, col=1
                                            )
        else:
            self.fig.add_trace(macd_trace_fast, row=2, col=1)
            self.fig.add_trace(macd_trace_slow, row=2, col=1)
        macd_trace_signal = go.Scatter(x=self.data.open_time, y=self.data.MACD_signal, name="macd_signal", mode='lines')
        self.fig.add_trace(macd_trace_signal, row=2, col=1)

    def create_EMA(self, time_1 = 50, time_2 = 100, time_3 = 200):
        self.data['EMA_50'] = talib.EMA(self.data.close, timeperiod=time_1)
        self.data['EMA_100'] = talib.EMA(self.data.close, timeperiod=time_2)
        self.data['EMA_200'] = talib.EMA(self.data.close, timeperiod=time_3)

        EMA_trace_50 = go.Scatter(x=self.data.open_time, y=self.data.EMA_50, mode="lines", name="EMA50")
        EMA_trace_100 = go.Scatter(x=self.data.open_time, y=self.data.EMA_100, mode="lines", name="EMA100")
        EMA_trace_200 = go.Scatter(x=self.data.open_time, y=self.data.EMA_200, mode="lines", name="EMA200")
        self.fig.add_trace(EMA_trace_50, row=1, col=1)
        self.fig.add_trace(EMA_trace_100, row=1, col=1)
        self.fig.add_trace(EMA_trace_200, row=1, col=1)

    def create_RSI(self, time=14):
        self.data['RSI'] = talib.RSI(self.data.close, timeperiod=time)

        RSI = go.Scatter(x=self.data.open_time, y=self.data.RSI, mode="lines", name="RSI")
        self.fig.add_trace(RSI, row=3, col=1)

    def create_short_EMA(self):
        self.data['EMA_2'] = talib.EMA(self.data.close, timeperiod=2)
        EMA_trace_2 = go.Scatter(x=self.data.open_time, y=self.data.EMA_2, mode="lines", name="EMA2")
        self.fig.add_trace(EMA_trace_2, row=1, col=1)
