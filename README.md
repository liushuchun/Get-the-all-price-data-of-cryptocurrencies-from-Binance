# Get-the-all-price-data-of-cryptocurrencies-from-Binance
This project pulls all the price data of a coin you want on the binance exchange, from start to finish, at any time interval.

# getPrice.py
   The getPrice.py script allows you to pull all data from the binance exchange of any cryptocurrency in any time interval.

# addNewCoin.py
If you want to get a cryptocurrency data, firstly you have to add to cryptocurrency price taker as use addNewCoin.py script.

## Changing Time Intevral
If you want changing time interval you have to change numbers at line 69th and 84th.
For changing time to minute  you have to chance line 70th like this 
 **hours_added = timedelta(minute=hours)**
 and chance "h" charackter to "m" at line 84th.

![The photo of line 69th and 84th](https://user-images.githubusercontent.com/87073563/164894999-b9499f15-d30b-4faa-a02c-106befb53d39.PNG)
