from datetime import datetime


class Figures:
    def __init__(self, plot):
        self.plot = plot
        self.row = 1
        self.col = 1

    @staticmethod
    def totimestamp(dt, epoch=datetime(1970, 1, 1)):
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6

    def create_line(self, y, color, width):
        self.plot.fig.add_hline(y, line_color=color, line_width=width, row=self.row, col=self.col)

    def create_fib_sup(self,y_start, y_stop):
        fibka = [0.236, 0.382, 0.5, 0.618, 0.786, 1.272, 1.618]
        y = min(y_start, y_stop)
        delta = abs(y_start - y_stop)
        self.create_line(y_start, "blue", 3)
        self.create_line(y_stop, "blue", 3)
        for i in fibka:
            self.create_line(y + delta * i, "blue", 1)

    def create_fib_fan(self,x_1, x_2, y_1, y_2):
        fibka = [0.236, 0.382, 0.5, 0.618, 0.786]
        delta = abs(y_1 - y_2)
        x_1 = datetime(int(x_1.split('.')[2]), int(x_1.split('.')[1]), int(x_1.split('.')[0]), int(x_1.split('.')[3]),
                       int(x_1.split('.')[4]))
        x_2 = datetime(int(x_2.split('.')[2]), int(x_2.split('.')[1]), int(x_2.split('.')[0]), int(x_2.split('.')[3]),
                       int(x_2.split('.')[4]))

        delta_x = abs(Figures.totimestamp(x_1) - Figures.totimestamp(x_2))
        k = (y_2 - y_1) / (Figures.totimestamp(x_2) - Figures.totimestamp(x_1))
        b = y_1 - k * Figures.totimestamp(x_1)
        x_2_1 = self.plot.klines[-1][0]
        y_2_1 = k * Figures.totimestamp(x_2_1) + b
        y_2_2 = y_2_1
        self.plot.fig.add_shape(type="line",
                      x0=x_1, y0=y_1, x1=x_2_1, y1=y_2_1,
                      line=dict(color="black", width=3),
                      row=self.row, col=self.col
                      )
        for i in fibka:
            k = (y_2 + delta * i - y_1) / (Figures.totimestamp(x_2) - Figures.totimestamp(x_1))
            b = y_1 - k * Figures.totimestamp(x_1)
            x_2_1 = self.plot.klines[-1][0]
            y_2_1 = k * Figures.totimestamp(x_2_1) + b
            self.plot.fig.add_shape(type="line",
                          x0=x_1, y0=y_1, x1=x_2_1, y1=y_2_1,
                          line=dict(color="black", width=1),
                          row=self.row, col=self.col
                          )
        for i in fibka:
            k = (y_2 - y_1) / (Figures.totimestamp(x_2) - delta_x * i - Figures.totimestamp(x_1))
            b = y_1 - k * Figures.totimestamp(x_1)
            y_2_1 = y_2_2
            x_2_1 = datetime.fromtimestamp((y_2_1 - b)/k)
            self.plot.fig.add_shape(type="line",
                          x0=x_1, y0=y_1, x1=x_2_1, y1=y_2_1,
                          line=dict(color="black", width=1),
                          row=self.row, col=self.col
                          )


