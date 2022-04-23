from datetime import datetime, timedelta
from getPrice import get_bars


def getFirstDate(newCoinName):
    with open("DateData/"+newCoinName+"_last_time.txt", "w",
              encoding="utf-8") as file:
        timestamp = get_bars(newCoinName+"USDT", "4h", "2015-08-17 00:00:00",
                             "2022-11-08 00:00:00").iloc[0]["Open_Time"]
        date = datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S")
        seconds = 1
        second_added = timedelta(seconds=seconds)
        date = date - second_added
        file.write(get_bars(newCoinName+"USDT", "4h", "2015-08-17 00:00:00",
                            "2022-11-08 00:00:00").iloc[0]["Symbol"] + " " +
                            str(date)+"\n")

newCoin = input("Please, enter the name of new coin. (ex: ETH)    :  ")

try:
    getFirstDate(newCoin.upper())
    with open("CoinList.txt", "a", encoding="utf-8") as file:
        file.write(newCoin.upper()+"\n")
    with open("Price_Data/"+newCoin.upper()+"USDT_Data.csv", "w") as file:
        file.write(",Symbol,Open_Time,Close_Time,o,c,Price_Direction")
    print("We got the first date of new coin.\
          You can get prices from getPrice.py")
except:
    print("ERROR!!! Try again.")
