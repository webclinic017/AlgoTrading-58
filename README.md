# AlgoTrading
As using the BackTrader library we can implement and test out algo trading strategy

In the Sample data folder we have some sample data that can download from Yahoo Finance, but as of saving time for doing testing to multiple stocks we had implemented the yfinance library to take any symbol and run tests

As in the testing folder we have sampleList.txt where it stores the list of symbols that can be runned to test and of course for some more testing
There is always the SP500 folder where it inlcude a list of sp500 symbols and a results file that stores the results from the algo

In terms of strategies we have:
1) Bob/Bob1: 
  So this strategy takes in weekly, monthly averages and the volume in count to determine when to buy the order 
  As for selling or exiting the market, it will exit once the price hits the buy factor times the price or it had waited too long and auto exits
2) Average/Bob2:
  This strategy bascially buys once it hits the lowest price of the week and sells when it gets to the highest of the week and the price its profitable

In the traderMain it has a runstrategy that can take in symbol, printEnable(to enable the printing of the results), plotMode(enable to plot the results for every symbol), starting cash amount, and comission (in percentage)
