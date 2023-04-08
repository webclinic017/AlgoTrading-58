import time
import yfinance as yf
import backtrader as bt
import pandas as pd
import datetime
import strategy.strategyAverage as strategyAverage
import strategy.strategyPeriod as strategyPeriod
import strategy.core as core
import matplotlib
import strategy.AnalyzerSuite as AnalyzerSuite


def runStrategy(symbol, printEnable=False, plotMode=False, cash=100000, comission=0.01):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(comission)

    data = bt.feeds.PandasData(dataname=yf.download(
        symbol, '2010-01-01', '2020-01-01', auto_adjust=True))

    cerebro.adddata(data)
    # cerebro.addstrategy(strategyAverage.strategyBob1)
    # cerebro.addstrategy(strategyPeriod.strategyBob2)
    cerebro.addstrategy(core.strategyBob3)

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
    #list = ['RY']
    readFile = open("./testing/sp500/sp500.txt", "r")
    #readFile = open("./testing/sample/sampleList.txt", "r")
    list = readFile.read().split('\n')
    readFile.close()

    writeFile = open("./testing/sp500/results3.txt", "a")
    #writeFile = open("./testing/sample/resultSample.txt", "a")

    count = 1

    lowest = 100000
    highest = 100000
    lowSym = "None"
    highSym = "None"

    for stock in list:
        print(str(count)+"/"+str(len(list)))
        try:
            result = runStrategy(stock)  # , True, True)
            if(result['DrawDown'] < 30 and result['Sharpe Ratio:'] > 1):
                writeFile.write("Positive: "+str(stock)+" : "+str(result)+"\n")
            elif(result['Returns:'] < 0):
                writeFile.write("Negative: "+str(stock)+" : "+str(result)+"\n")
            else:
                writeFile.write("Netural: "+str(stock)+" : "+str(result)+"\n")
            if(result['Final Value'] < lowest):
                lowest = result['Final Value']
                lowSym = stock
            if(result['Final Value'] > highest):
                highest = result['Final Value']
                highSym = stock
        except:
            writeFile.write("Error: "+str(stock)+" : " +
                            "Blame Jimmy for not fixing these errors"+"\n")
            print("Jimmy is too lazy to fix this")
        count += 1
    writeFile.close()
    print("Highest: "+str(highSym)+" with: "+str(highest))
    print("Lowest: "+str(lowSym)+" with: "+str(lowest))
    end = time.time()
    print("*********************Finish run*********************")
    print(end - start)
