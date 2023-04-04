import backtrader as bt
import datetime
import strategyBob
import matplotlib
import AnalyzerSuite as AnalyzerSuite

cash = 100000
comission = 0.01


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(comission)

    data = bt.feeds.YahooFinanceCSVData(dataname='BN.TO.csv',
                                        fromdate=datetime.datetime(
                                            2009, 12, 2),
                                        todate=datetime.datetime(2019, 12, 31),
                                        reverse=False)

    cerebro.adddata(data)
    cerebro.addstrategy(strategyBob.strategyBob1)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()

    AnalyzerSuite.AnalyzerSuite.defineAnalyzers(AnalyzerSuite, cerebro)
    thestrats = cerebro.run(stdstats=True)
    print(AnalyzerSuite.AnalyzerSuite.returnAnalyzers(AnalyzerSuite, thestrats))
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
