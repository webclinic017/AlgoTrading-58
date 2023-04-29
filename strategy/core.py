import backtrader as bt


class strategyBob3(bt.Strategy):

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
        highestPrice = self.dataclose[0]
        for i in range(num):
            if(self.dataclose[-i] > highestPrice):
                highestPrice = self.dataclose[-i]
        return highestPrice

    def lowest(self, num):
        lowestPrice = self.dataclose[0]
        for i in range(num):
            if(self.dataclose[-i] < lowestPrice):
                lowestPrice = self.dataclose[-i]
        return lowestPrice

    def delta(self, amount):
        total = 0
        for i in range(amount):
            total += self.dataclose[-i]
        average = total/amount
        change = ((self.dataclose[0]-average)/average)*100
        return change

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        days = 5
        weekChange = self.delta(5)
        monthChange = self.delta(20)

        if not self.position:
            if(self.dataclose[0] <= self.lowest(days) and weekChange < -0.5):
                temp = int(self.broker.get_cash()*0.98/self.dataclose[0])
                #self.order = self.buy(size=temp)
                print("buying at..."+str(self.dataclose[0]))
        # else:
        if(self.dataclose[0] > self.position.price and self.dataclose[0] >= self.highest(days)):
            self.order = self.sell(size=self.position.size)
            print("selling at..."+str(self.dataclose[0]))
        elif(len(self) >= (self.bar_executed + 1)):
            self.order = self.sell(size=self.position.size)
