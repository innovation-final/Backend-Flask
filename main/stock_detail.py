import FinanceDataReader as fdr
from datetime import datetime
from pykrx import stock

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock

# 문자열로 오늘 날짜 얻기
now = datetime.now()
today = now.strftime("%Y%m%d")


# tickers = stock.get_market_ticker_list(today, market='ALL')
# for c, ticker in enumerate(tickers):
#     result = []
#     df = fdr.DataReader(ticker, start='2021-01-01')
#     index = df.index.to_list()
#     for i in range(df.shape[0]):
#         result.append([
#             str(index[i])[:10],  # date
#             str(int(df.iloc[i]["Open"])),
#             str(int(df.iloc[i]["High"])),
#             str(int(df.iloc[i]["Low"])),
#             str(int(df.iloc[i]["Close"])),
#             str(int(df.iloc[i]["Volume"])),
#             str(df.iloc[i]["Change"]),
#         ])
#     db.chart.update_one({"code": ticker}, {"$set": {"data": result}})
#     print(f"{c + 1}/{2650} {ticker}")

# def set_data():
#     cnt = 0
#
#     kospi_tickers = stock.get_market_ticker_list(today, market='KOSPI')
#     for ticker in kospi_tickers:
#         result = []
#         try:
#             df = fdr.DataReader(ticker, start='2021-01-01')
#             index = df.index.to_list()
#             for i in range(df.shape[0]):
#                 result.append([
#                     str(index[i])[:10],  # date
#                     str(int(df.iloc[i]["Close"]))
#                     # str(int(df.iloc[i]["Volume"]))
#                 ])
#         except:
#             cnt += 1
#             continue
#
#         db.chart_year.insert_one({
#             "name": stock.get_market_ticker_name(ticker),
#             "code": ticker,
#             "market": "KOSPI",
#             "data": result
#         })
#         cnt += 1
#         print(f"{cnt}/{2650} {ticker}")
#
#     kosdaq_tickers = stock.get_market_ticker_list(today, market='KOSDAQ')
#     for ticker in kosdaq_tickers:
#         result = []
#         try:
#             df = fdr.DataReader(ticker, start='2021-01-01')
#             index = df.index.to_list()
#             for i in range(df.shape[0]):
#                 result.append([
#                     str(index[i])[:10],  # date
#                     str(int(df.iloc[i]["Close"]))
#                     # str(int(df.iloc[i]["Volume"]))
#                 ])
#         except:
#             cnt += 1
#             continue
#
#         db.chart_year.insert_one({
#             "name": stock.get_market_ticker_name(ticker),
#             "code": ticker,
#             "market": "KOSDAQ",
#             "data": result
#         })
#         cnt += 1
#         print(f"{cnt}/{2650} {ticker}")


def add_data():
    today = datetime.now().strftime("%Y%m%d")
    stocks = list(db.chart.find({}))
    for i, stock in enumerate(stocks):
        ticker = stock["code"]
        try:
            df = fdr.DataReader(ticker, today, today)
            index = df.index.to_list()[0]

            result = db.chart.find_one({"code": ticker})["data"]
            result_year = db.chart_year.find_one({"code": ticker})["data"]

            result.append([
                str(index)[:10],  # date
                str(int(df["Open"])),
                str(int(df["High"])),
                str(int(df["Low"])),
                str(int(df["Close"])),
                str(int(df["Volume"])),
                str(float(df["Change"])),
            ])
            result_year.append([str(index)[:10], str(int(df["Close"]))])

            db.chart.update_one({"code": ticker}, {"$set": {"data": result}})
            db.chart_year.update_one({"code": ticker}, {"$set": {"data": result_year}})

        except:
            continue


def renew_marcap():
    data = fdr.StockListing('KRX-MARCAP')
    marcap_list = data['Marcap'].to_list()
    code_list = data['Code'].to_list()
    for i, code in enumerate(code_list):
        try:
            db.chart.update_one({"code": code}, {"$set": {"marcap": marcap_list[i]}})
        except:
            continue