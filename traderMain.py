import time
import yfinance as yf
import backtrader as bt
import pandas as pd
import datetime
import strategy.strategyAverage as strategyAverage
import strategy.strategyPeriod as strategyPeriod
import strategy.core as core
import strategy.MR as MR
import strategy.momentum as momentum
import matplotlib
import strategy.AnalyzerSuite as AnalyzerSuite
import os
import sys


def runStrategy(symbol, printEnable=False, plotMode=False, startDate='2010-01-01', endDate='2020-01-01', cash=100000, comission=0.01):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(comission)

    data = bt.feeds.PandasData(dataname=yf.download(
        symbol, startDate, endDate, auto_adjust=True))

    cerebro.adddata(data)
    # cerebro.addstrategy(strategyAverage.strategyBob1)
    # cerebro.addstrategy(strategyPeriod.strategyBob2)
    # cerebro.addstrategy(core.strategyBob3)
    cerebro.addstrategy(MR.strategyMR)

    if(printEnable):
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.run()

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
    # outputs['Symbol'] = symbol
    return(outputs)


def runMomentum(list, printEnable=False, plotMode=False, cash=100000, comission=0.01):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(comission)

    count = 1
    for stock in list:
        print(str(count)+"/"+str(len(list)))
        data0 = bt.feeds.PandasData(dataname=yf.download(
            stock, '2010-01-01', '2020-01-01', auto_adjust=True))
        cerebro.adddata(data0)
        count += 1

    cerebro.addstrategy(momentum.strategyMomentum)

    if(printEnable):
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

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
    # outputs['Symbol'] = symbol
    return(outputs)


def runTesting():
    start = time.time()
    list = ['ENB.TO', 'TD.TO', 'BN.TO', 'BNS.TO', 'SU.TO']
    # list = ['TD.TO']
    readFile = open("./testing/sp500/sp500.txt", "r")
    #readFile = open("./testing/sample/sampleList2.txt", "r")
    list = readFile.read().split('\n')
    readFile.close()

    writeFile = open("./testing/sp500/results5.txt", "a")
    #writeFile = open("./testing/sample/resultSample.txt", "a")

    count = 1

    lowest = 100000
    highest = 100000
    lowSym = "None"
    highSym = "None"

    results = {"positive": 0, "neutral": 0, "negative": 0, "error": 0}

    newList = []
    firstPart = False
    if(firstPart == True):
        for stock in list:
            print(str(count)+"/"+str(len(list)))
            try:
                result = runStrategy(stock)  # , True, True)
                if(result['DrawDown'] < 30 and result['Sharpe Ratio:'] > 1):
                    writeFile.write("Positive: "+str(stock) +
                                    " : "+str(result)+"\n")
                    results["positive"] += 1
                    newList.append(stock)
                elif(result['Returns:'] < 0):
                    writeFile.write("Negative: "+str(stock) +
                                    " : "+str(result)+"\n")
                    results["negative"] += 1
                else:
                    writeFile.write("Netural: "+str(stock) +
                                    " : "+str(result)+"\n")
                    results["neutral"] += 1
                if(result['Final Value'] < lowest):
                    lowest = result['Final Value']
                    lowSym = stock
                if(result['Final Value'] > highest):
                    highest = result['Final Value']
                    highSym = stock
            except:
                writeFile.write("Error: "+str(stock)+" : " +
                                "Blame Jimmy for not fixing these errors"+"\n")
                results["error"] += 1
                print("Jimmy is too lazy to fix this")
            count += 1
        writeFile.close()
        print("Highest: "+str(highSym)+" with: "+str(highest))
        print("Lowest: "+str(lowSym)+" with: "+str(lowest))
        end = time.time()
        print("*********************Finish run*********************")
        print("Finish running Part 1 in: "+str(end - start))
        print(results)
    else:
        newList = ['ACN', 'AET', 'AEE', 'AEP', 'AMT', 'AMGN', 'AON', 'ADP', 'BDX', 'BA', 'CB', 'CINF', 'CTAS', 'CLX', 'CMS', 'KO', 'COST', 'DHR', 'DRI', 'ECL', 'FISV', 'HD', 'HON', 'HRL',
                   'INTU', 'JNJ', 'LLY', 'MMC', 'MA', 'MKC', 'MSFT', 'MSI', 'NDAQ', 'NEE', 'NKE', 'NI', 'PEP', 'PGR', 'RSG', 'ROP', 'ROST', 'SYY', 'TRV', 'TJX', 'UNH', 'VZ', 'WEC', 'XEL', 'XYL']

    # newList = ['ENB.TO', 'BN.TO', 'TD.TO', 'BNS.TO', 'SU.TO']
    # newList = list
    # newList = ['UNH', 'VZ', 'AEE', 'XEL', 'MSFT']
    print(newList)
    start = time.time()
    result = runMomentum(newList, True, True)
    end = time.time()
    print("*********************Finish run*********************")
    print("Finish running Part 2 in: "+str(end - start))
    print(result)


if __name__ == '__main__':
    # runTesting()
    # list = ['RY.TO', 'BN.TO', 'TD.TO', 'BNS.TO']
    # newList = ['ACN', 'AET', 'AEE', 'AEP', 'AMT', 'AMGN', 'AON', 'ADP', 'BDX', 'BA', 'CB', 'CINF', 'CTAS', 'CLX', 'CMS', 'KO', 'COST', 'DHR', 'DRI', 'ECL', 'FISV', 'HD', 'HON', 'HRL',
    #            'INTU', 'JNJ', 'LLY', 'MMC', 'MA', 'MKC', 'MSFT', 'MSI', 'NDAQ', 'NEE', 'NKE', 'NI', 'PEP', 'PGR', 'RSG', 'ROP', 'ROST', 'SYY', 'TRV', 'TJX', 'UNH', 'VZ', 'WEC', 'XEL', 'XYL']
    # for stock in newList:
    #     print(stock)
    list = ['GFL.TO', 'SU.TO', 'ENB.TO', 'RY.TO', 'BN.TO', 'TD.TO', 'BNS.TO']
    # list = ['BN.TO']
    print("starting...")
    endDate = datetime.datetime.today().strftime('%Y-%m-%d')
    # print(endDate)
    startDate = datetime.datetime.today() - datetime.timedelta(days=6*30)
    # print(startDate)
    file = open("./results/results_"+str(endDate)+".txt", "a")
    sys.stdout = file
    for stock in list:
        print("for ..... "+stock)
        startDatetemp = datetime.datetime.today() - datetime.timedelta(days=3)
        data = yf.download(stock, startDatetemp, endDate)
        print(data)
        result = runStrategy(
            stock, False, False, startDate=startDate, endDate=endDate)
        print("****************************************************************************************")
