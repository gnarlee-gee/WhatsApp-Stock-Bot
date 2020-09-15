import os
from iexfinance.stocks import Stock



stockObj = Stock('AAPL', token=os.getenv('IEX_TOKEN'))
print(stockObj.get_quote()['latestPrice'])