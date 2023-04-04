import yfinance as yf
import backtrader as bt
import pandas as pd
import datetime
import strategyBob
import matplotlib
import AnalyzerSuite as AnalyzerSuite


def runStrategy(symbol, cash=100000, comission=0.01):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(comission)

    data = bt.feeds.PandasData(dataname=yf.download(
        symbol, '2010-01-01', '2020-01-01', auto_adjust=True))

    cerebro.adddata(data)
    cerebro.addstrategy(strategyBob.strategyBob1)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()

    AnalyzerSuite.AnalyzerSuite.defineAnalyzers(AnalyzerSuite, cerebro)
    thestrats = cerebro.run(stdstats=True)
    print(AnalyzerSuite.AnalyzerSuite.returnAnalyzers(
        AnalyzerSuite, thestrats))
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.plot()


if __name__ == '__main__':
    list = ['BN.TO', 'TD.TO', 'ENB.TO']
    list = ['BN.TO', 'BNS.TO']
    # tickers = pd.read_html(
    #     'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    # print(tickers.head())
    # print(tickers.Symbol.to_list())
    for stock in list:
        runStrategy(stock)
