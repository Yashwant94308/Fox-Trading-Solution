from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import requests
import datetime
import time

yf.pdr_override()

stocklist = si.tickers_sp500()
index_name = '^GSPC'  # S&P 500

final = []
index = []
n = -1

exportList = pd.DataFrame(
    # columns=['Ticker', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
    columns=['Ticker', "Date", "Time", "open", "High", "Low", "Close", "Volume"])

for stock in stocklist[0:5]:
    n += 1
    time.sleep(1)

    print("\npulling {} with index {}".format(stock, n))

    # RS_Rating
    now = datetime.datetime.now()
    start = now.strftime("%H:%M:%S")
    start_date = datetime.datetime.now()
    end_date = datetime.date.today()

    df = pdr.get_data_yahoo(stock, start=start_date, end=end_date)
    df['Percent Change'] = df['Adj Close'].pct_change()
    stock_return = df['Percent Change'].sum() * 100

    index_df = pdr.get_data_yahoo(index_name, start=start_date, end=end_date)
    index_df['Percent Change'] = index_df['Adj Close'].pct_change()
    index_return = index_df['Percent Change'].sum() * 100

    RS_Rating = round((stock_return / index_return) * 10, 2)

    try:
        currentClose = df["Adj Close"][-1]
        lows = min(df["Adj Close"][:])
        highs = max(df["Adj Close"][:])
        volume = df["volume"]

        final.append(stock)
        index.append(n)

        dataframe = pd.DataFrame(list(zip(final, index)), columns=['Company', 'Index'])

        dataframe.to_csv('stocks.csv')

        exportList = exportList.append({'Ticker': stock, "Start": start, "End": end_date,
                                        "Low": lows, "High": highs, "close": currentClose, "volume": volume},
                                       ignore_index=True)
        print(stock + " made the requirements")
    except Exception as e:
        print(e)
        print("No data on " + stock)

print(exportList)

writer = ExcelWriter("ScreenOutput.xlsx")
exportList.to_excel(writer, "Sheet1")
writer.save()
