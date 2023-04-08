import backtrader as bt


class strategyBob1(bt.Strategy):

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

    def delta(self, amount):
        total = 0
        for i in range(amount):
            total += self.dataclose[-i]
        average = total/amount
        change = ((self.dataclose[0]-average)/average)*100
        return change

    def lowest(self, num):
        lowestPrice = self.dataclose[0]
        for i in range(num):
            if(self.dataclose[-i] < lowestPrice):
                lowestPrice = self.dataclose[-i]
        return lowestPrice

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        yearChange = self.delta(252)
        monthChange = self.delta(20)
        weekChange = self.delta(5)

        total = 0
        for i in range(5):
            total += self.data.volume[-i]
        weekAveV = total/5
        weekChangeV = ((self.data.volume[0]-weekAveV)/weekAveV)*100

        if not self.position:
            if(weekChange < -2 and monthChange < 10):
                self.order = self.buy(size=2000)
        else:
            if(self.dataclose[0] > self.position.price*1.1):
                self.order = self.sell(size=self.position.size)
            # elif(len(self) >= (self.bar_executed + 200)):
            elif(self.dataclose[0] > self.position.price*1 and self.dataclose[0] < self.position.price*0.8):
                self.order = self.sell(size=self.position.size)
