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
        self.dataIndex = 0
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

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        period = 3

        if (self.placed == False):  # not self.position:
            if(len(self) % period == 0):
                highest = 0
                dataIn = 0
                for i in range(len(self.datas)):
                    val = self.calMom(i, period)
                    if(val > highest):
                        highest = val
                        dataIn = i
                if(highest > 0):
                    self.dataIndex = dataIn
                    temp = int(self.broker.get_cash()
                               * 0.98/self.dataclose[0])
                    self.order = self.buy(
                        data=self.datas[self.dataIndex], size=temp)
                    self.placed = True
                    self.shares = temp
        else:
            if(len(self) % period == (period-1) and self.datas[self.dataIndex].close[0] > self.position.price*1.1):
                # print("did sell")
                self.order = self.sell(
                    data=self.datas[self.dataIndex], size=self.shares)
                self.placed = False
