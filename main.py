from Plot import Plot


if __name__ == "__main__":
    plot_btc = Plot("BTCUSDT", "KLINE_INTERVAL_15MINUTE", 100)
    plot_btc.create_base_plot()
    plot_btc.init_ind()
    plot_btc.init_figures()
    plot_btc.init_pat()
    #ind_plot_btc.create_short_EMA()
    plot_btc.ind.create_MACD(diagram=True)
    plot_btc.ind.create_RSI(16)
    #fg_plot_btc.create_line(28894.91, "blue", 1)
    #fg_plot_btc.create_fib_sup(29352.96, 31795.1)
    #fg_plot_btc.create_fib_fan("4.5.2022.3.0", "12.6.2022.3.0", 39877.2, 25921.18)
    #dv_plot_dtc = Divergenses(plot_btc)
    #dv_plot_dtc.create_pivot()
    #dv_plot_dtc.create_point()
    #dv_plot_dtc.create_signal()
    plot_btc.init_diver()
    plot_btc.diver.create_pivot()
    #plot_btc.diver.find_diver_lower(50)
    #plot_btc.diver.find_diver_upper(50)
    plot_btc.start_plot()
