# AlgoTrading
As using the BackTrader library we can implement and test out algo trading strategy

In the Sample data folder we have some sample data that can download from Yahoo Finance, but as of saving time for doing testing to multiple stocks we had implemented the yfinance library to take any symbol and run tests

As in the testing folder we have sampleList.txt where it stores the list of symbols that can be runned to test and of course for some more testing
There is always the SP500 folder where it inlcude a list of sp500 symbols and a results file that stores the results from the algo

In terms of strategies we have:
1) Average/Bob1: 
  So this strategy takes in weekly, monthly averages and the volume in count to determine when to buy the order 
  As for selling or exiting the market, it will exit once the price hits the buy factor times the price or it had waited too long and auto exits
2) Period/Bob2:
  This strategy bascially buys once it hits the lowest price of the week and sells when it gets to the highest of the week and the price its profitable
3) Core/Bob3:
  This one takes in consideration of both the average and period in factor of entering and exiting the market. 
 4) MR:
  Improved version of core which gives less average but more mean revision comparisons.
 5) Momentum:
  Takes in whole lis of symbols and buy the stock in their momentum (buy high and sell even higher). This only buys the highest momentum stock in the list provided.

In the traderMain it has a runstrategy that can take in symbol, printEnable(to enable the printing of the results), plotMode(enable to plot the results for every symbol), starting cash amount, and comission (in percentage)

********************************************************************************************************************************************************************************

Actually using the algo in real-life!

- In main function it runs the list of stocks against MR strategy
- Outputs buy signal into the daily txt file
- In the txt file it also contains the last 3 day's data 

Decide: Check if the last buy price is close enough to the last market close price then BUY IT! with your own trader account

Note: Do some research before actually buying cause sometimes terrible news can used to flag the buying signal
