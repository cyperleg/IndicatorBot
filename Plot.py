from binance.client import Client
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.subplots
from CandlestickPattern import CandlestickPattern
from Figures import Figures
from Indicators import Indicators
from Divergenses import Divergenses


class Plot:
    api_secret = 'FlPtJVYWZZQae6Qec0hle3HenWAIfSvst5ZM16OES4wdnqoFeJq22OAie8JFUMgA'
    api_key = 'hWUHsM5blTOmQQZTaurkB6t1GqEifJpx8cxUDmQl58qDFmN8a6Fcfoc3By2D33Og'
    client = Client(api_key, api_secret)

    def __init__(self, name, interval, limit=1000):
        self.name = name
        self.interval = interval
        self.klines = Plot.client.get_historical_klines(name, eval("Plot.client."+interval), limit=limit)
        self.convert_klines()
        self.data: pd.DataFrame = None
        self.fig: plotly.subplots = None
        self.pat: CandlestickPattern = None
        self.figures: Figures = None
        self.ind: Indicators = None
        self.diver: Divergenses = None

    def init_pat(self):
        self.pat = CandlestickPattern(self.data, self.fig)

    def init_figures(self):
        self.figures = Figures(self.data)

    def init_ind(self):
        self.ind = Indicators(self.data, self.fig)

    def init_diver(self):
        self.diver = Divergenses(self.data, self.fig)

    def convert_klines(self):
        for i in range(len(self.klines)):
            self.klines[i][0], self.klines[i][6] = datetime.fromtimestamp(self.klines[i][0]/1000),\
                                                   datetime.fromtimestamp(self.klines[i][6]/1000)
            self.klines[i][1] = float(self.klines[i][1])
            self.klines[i][2] = float(self.klines[i][2])
            self.klines[i][3] = float(self.klines[i][3])
            self.klines[i][4] = float(self.klines[i][4])

    def create_base_plot(self):
        self.data = pd.DataFrame(self.klines)
        self.data.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades',
                        'taker_base_vol', 'taker_quote_vol', 'ignore'] # create colums name

        # Candlestick
        self.fig = make_subplots(rows=3, cols=1, row_heights=[0.5, 0.4, 0.1])

        self.fig.add_trace(
            go.Candlestick(
                x=self.data.open_time,
                open=self.data.open,
                high=self.data.high,
                low=self.data.low,
                close=self.data.close,
            ),
            row=1, col=1
        )
        self.fig.update_layout(
            title=self.name,
            xaxis_rangeslider_visible=False
        )

    def start_plot(self):
        if not isinstance(self.fig, list):
            self.fig.show()