import time
import yfinance as yf
import backtrader as bt
import pandas as pd
import datetime
import strategy.strategyBob as strategyBob
import strategy.strategyAverage as strategyAverage
import matplotlib
import strategy.AnalyzerSuite as AnalyzerSuite


def runStrategy(symbol, printEnable=False, plotMode=False, cash=100000, comission=0.01):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(comission)

    data = bt.feeds.PandasData(dataname=yf.download(
        symbol, '2010-01-01', '2020-01-01', auto_adjust=True))

    cerebro.adddata(data)
    # cerebro.addstrategy(strategyBob.strategyBob1)
    cerebro.addstrategy(strategyAverage.strategyBob2)

    if(printEnable):
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()

    AnalyzerSuite.AnalyzerSuite.defineAnalyzers(AnalyzerSuite, cerebro)
    thestrats = cerebro.run(stdstats=True)
    if(printEnable):
        print(AnalyzerSuite.AnalyzerSuite.returnAnalyzers(
            AnalyzerSuite, thestrats))
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    if(plotMode):
        cerebro.plot()

    outputs = AnalyzerSuite.AnalyzerSuite.returnAnalyzers(
        AnalyzerSuite, thestrats)
    outputs['Final Value'] = cerebro.broker.getvalue()
    #outputs['Symbol'] = symbol
    return(outputs)


if __name__ == '__main__':
    start = time.time()
    list = ['BN.TO', 'TD.TO', 'ENB.TO', 'BNS.TO']
    list = ['DELL']
    readFile = open("./testing/sample/sampleList.txt", "r")
    #list = readFile.read().split('\n')
    readFile.close()

    writeFile = open("./testing/sample/resultSample.txt", "a")

    count = 1
    for stock in list:
        print(str(count)+"/"+str(len(list)))
        try:
            result = runStrategy(stock, True, True)
            if(result['DrawDown'] < 30 and result['Sharpe Ratio:'] > 1):
                writeFile.write("Positive: "+str(stock)+" : "+str(result)+"\n")
            else:
                writeFile.write("Netural: "+str(stock)+" : "+str(result)+"\n")
        except:
            writeFile.write("Negative: "+str(stock)+" : " +
                            "Blame Jimmy for not fixing these errors"+"\n")
            print("Jimmy is too lazy to fix this")
        count += 1
    writeFile.close()
    end = time.time()
    print(end - start)
