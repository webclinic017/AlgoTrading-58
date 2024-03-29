import backtrader as bt
from strategy.AnalyzerSuite import AnalyzerSuite


class strategyMomentum(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.dataIndex = -1
        self.placed = False
        self.shares = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            # if order.isbuy():
            #     self.log('BUY EXECUTED {}'.format(order.executed.price))
            # elif order.issell():
            #     self.log('SELL EXECUTED {}'.format(order.executed.price))
            self.bar_executed = len(self)
        self.order = None

    def calMom(self, i, period):
        mom = ((self.datas[i].close[0]-self.datas[i].close[-period]
                )/self.datas[i].close[-period])*100
        return mom

    def buyAll(self, period):
        highest = self.calMom(0, period)
        dataIn = 0
        for i in range(len(self.datas)):
            val = self.calMom(i, period)
            if(val >= highest):
                highest = val
                dataIn = i
        temp = int(self.broker.get_cash()
                   * 0.98/self.datas[dataIn].close[0])
        self.order = self.buy(
            data=self.datas[dataIn], size=temp)
        #print(str(dataIn)+" buying "+str(temp))
        self.shares = temp
        self.dataIndex = dataIn
        self.placed = True

    def sellAll(self):
        # print(self.dataIndex)
        # print(self.shares)
        self.order = self.sell(
            data=self.datas[self.dataIndex], size=self.shares)
        # print(str(self.dataIndex)+" selling " +
        #       str(self.shares))
        self.placed = False

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        period = 2

        if (self.placed == False):
            if(len(self) % period == 0):
                self.buyAll(period)
        else:
            if(len(self) % period == (period-1) and self.datas[self.dataIndex].close[0] > self.position.price*1.2):
                self.sellAll()
            # elif(len(self) >= (self.bar_executed + 252)):
            #     self.sellAll()
