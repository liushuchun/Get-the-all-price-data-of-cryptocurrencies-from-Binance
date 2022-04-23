import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pandas as pd
import winsound


def dateStr_To_TimeStamp(date_string):
    dt_obj = datetime.strptime(date_string,
                               '%Y-%m-%d %H:%M:%S')
    timestamp = dt_obj.timestamp() * 1000
    return int(timestamp)


def get_bars(symbol, interval, start, end):
    root_url = 'https://api.binance.com/api/v1/klines'
    url = (root_url + '?symbol=' + symbol + '&interval=' + interval +
           "&startTime=" + str(dateStr_To_TimeStamp(start)) +
           "&endTime="+str(dateStr_To_TimeStamp(end)))
    data = json.loads(requests.get(url).text)
    df = pd.DataFrame(data)
    df.columns = ['open_time',
                  'o', 'h', 'l', 'c', 'v',
                  'close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore']

    df.insert(1, "Open_Time", [datetime.fromtimestamp(x/1000.0)
              for x in df.open_time], True)
    df.insert(2, "Close_Time", [datetime.fromtimestamp(x/1000.0)
              for x in df.close_time], True)
    df.insert(0, "Symbol", [symbol for x in range(len(df))], True)
    df.insert(8, "Price_Direction", [(float(x["c"]) - float(x["o"])) *
              100 / float(x["o"]) for index, x in df.iterrows()], True)

    del df["h"]
    del df["l"]
    del df["v"]
    del df["qav"]
    del df["close_time"]
    del df["open_time"]
    del df["num_trades"]
    del df["taker_base_vol"]
    del df["taker_quote_vol"]
    del df["ignore"]
    return df

if __name__ == "__main__":
    past = True
    with open("CoinList.txt", "r", encoding="utf-8") as file:
        coinList = file.readlines()
        lastCoin = coinList[-1]
    for coinName in coinList:
        continueLoop = True
        newCoinTime = False
        coinName = coinName[:-1]
        while past and continueLoop:
            if newCoinTime:
                continueLoop = False
            else:
                coinData = []

                with open("DateData/"+coinName+"_last_time.txt", "r",
                          encoding="utf-8") as file:
                    coinData.append(file.read().split(" ", 1))

                for coin, coinTime in coinData:

                    hours = 4
                    hours_added = timedelta(hours=hours)
                    date_time_obj = datetime.strptime(coinTime[:-1],
                                                      '%Y-%m-%d %H:%M:%S')
                    mainDf = pd.DataFrame({'Symbol': [],
                                           'Open_Time': [],
                                           'Close_Time': [],
                                           'o': [],
                                           'c': [],
                                           'Price_Direction': []
                                           })

                    while True:
                        try:
                            future_date_and_time = date_time_obj + hours_added
                            df2 = get_bars(coin, "4h", str(date_time_obj),
                                           str(future_date_and_time))
                            date_time_obj = future_date_and_time
                            mainDf = pd.concat([mainDf, df2], ignore_index=True)
                            print(df2)
                        except:
                            if date_time_obj > datetime.now():
                                winsound.Beep(600, 500)
                                oldDf = pd.read_csv("Price_Data/" + coin +
                                                    "_Data.csv", index_col=0)
                                mainDf = pd.concat([oldDf, mainDf[:-1]],
                                                   ignore_index=True)
                                mainDf.to_csv("Price_Data/"+coin+"_Data.csv")
                                with open("DateData/"+coinName+"_last_time.txt",
                                          "w", encoding="utf-8") as file:
                                    for data in [[coin, date_time_obj -
                                                 hours_added]]:
                                        file.write(data[0]+" "+str(data[1]))
                                if coin == lastCoin:
                                    past = False
                                newCoinTime = True
                                print("We came now.")
                                break
                            else:
                                winsound.Beep(600, 500)
                                oldDf = pd.read_csv("Price_Data/" + coin +
                                                    "_Data.csv", index_col=0)
                                mainDf = pd.concat([oldDf, mainDf],
                                                   ignore_index=True)
                                mainDf.to_csv("Price_Data/"+coin+"_Data.csv")
                                print("!!! Error !!!")
                                with open("mistakes.txt", "a",
                                          encoding="utf-8") as file:
                                    file.write(coinName + " " +
                                               str(future_date_and_time -
                                                   hours_added - hours_added) +
                                               "\n")
                                with open("DateData/"+coinName+"_last_time.txt",
                                          "w", encoding="utf-8") as file:
                                    for data in [[coin, future_date_and_time]]:
                                        file.write(data[0]+" "+str(data[1]))
                                break
