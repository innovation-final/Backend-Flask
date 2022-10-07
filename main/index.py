from pandas_datareader import data as pdr
from datetime import datetime
import yfinance as yf

import pymongo

client = pymongo.MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock

yf.pdr_override()


def add_kosdaq():
    result = []
    df_kosdaq = pdr.get_data_yahoo("^KQ11", start="2012-01-01", end=datetime.now().strftime('%Y-%m-%d'))
    for j in range(df_kosdaq.shape[0]):
        day = df_kosdaq.index[j]
        date = day.strftime('%Y-%m-%d')
        close_price = round(df_kosdaq.iloc[j]["Adj Close"], 2)
        result.append([date, close_price])
    db.index.update_one({"name": 'kosdaq'}, {"$set": {"index": result}})


def add_kospi():
    result = []
    df_kospi = pdr.get_data_yahoo("^KS11", start="2012-01-01", end=datetime.now().strftime('%Y-%m-%d'))
    for j in range(df_kospi.shape[0]):
        day = df_kospi.index[j]
        date = day.strftime('%Y-%m-%d')
        close_price = round(df_kospi.iloc[j]["Adj Close"], 2)
        result.append([date, close_price])
    db.index.update_one({"name": 'kospi'}, {"$set": {"index": result}})


def renew_current_index():
    today = datetime.now().strftime('%Y-%m-%d')

    df_kosdaq_now = pdr.get_data_yahoo("^KQ11", today)
    close_price = round(df_kosdaq_now.iloc[0]['Adj Close'], 2)
    db.index.update_one({'name': 'kosdaq'}, {'$set': {"current": close_price}})

    df_kospi_now = pdr.get_data_yahoo("^KS11", today)
    close_price = round(df_kospi_now.iloc[0]['Adj Close'], 2)
    db.index.update_one({"name": 'kospi'}, {"$set": {"current": close_price}})