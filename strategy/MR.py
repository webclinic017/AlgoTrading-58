import backtrader as bt
from strategy.AnalyzerSuite import AnalyzerSuite


class strategyMR(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

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

    def highest(self, num):
        highestPrice = self.dataclose[-1]
        for i in range(num):
            if(self.dataclose[-i-1] > highestPrice):
                highestPrice = self.dataclose[-i-1]
        return highestPrice

    def lowest(self, num):
        lowestPrice = self.dataclose[-1]
        for i in range(num):
            if(self.dataclose[-i-1] < lowestPrice):
                lowestPrice = self.dataclose[-i-1]
        return lowestPrice

    def movingAverage(self, amount):
        total = 0
        for i in range(amount):
            total += self.dataclose[-i]
        average = total/amount
        return average

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if(self.dataclose[0] < self.movingAverage(20) and self.dataclose[0] <= self.lowest(7)):
                temp = int(self.broker.get_cash()*0.98/self.dataclose[0])
                #self.order = self.buy(size=temp)
                print("buying at..."+str(self.dataclose[0]))
        # else:
        if(self.dataclose[0] > self.position.price*1 and self.dataclose[0] >= self.highest(7) and self.dataclose[0] > self.movingAverage(20)):
            self.order = self.sell(size=self.position.size)
            #print("selling at..."+str(self.dataclose[0]))
            print("selling at..."+str(self.dataclose[0]))
        # elif(len(self) >= (self.bar_executed + 1)):
        # self.order = self.sell(size=self.position.size)
        #print("force selling at..."+str(self.dataclose[0]))
