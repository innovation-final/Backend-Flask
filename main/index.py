from pandas_datareader import data as pdr
from datetime import datetime
import yfinance as yf

import pymongo
import redis

redis = redis.StrictRedis(host="redis-12441.c294.ap-northeast-1-2.ec2.cloud.redislabs.com", port=12441,
                          password="uvLuMUsT4ChA2OJCDlDu5SkDtBzVEnQj")

client = pymongo.MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock

yf.pdr_override()


def add_kosdaq():
    result = []
    df_kosdaq = pdr.get_data_yahoo("^KQ11", start="2012-01-01", end=datetime.now().strftime('%Y-%m-%d'))
    for j in range(0, df_kosdaq.shape[0], 30):
        day = df_kosdaq.index[j]
        date = day.strftime('%Y-%m-%d')
        close_price = round(df_kosdaq.iloc[j]["Adj Close"], 2)
        result.append([date, close_price])
    db.index.update_one({"name": 'kosdaq'}, {"$set": {"index": result}})


def add_kospi():
    result = []
    df_kospi = pdr.get_data_yahoo("^KS11", start="2012-01-01", end=datetime.now().strftime('%Y-%m-%d'))
    for j in range(0, df_kospi.shape[0], 30):
        day = df_kospi.index[j]
        date = day.strftime('%Y-%m-%d')
        close_price = round(df_kospi.iloc[j]["Adj Close"], 2)
        result.append([date, close_price])
    db.index.update_one({"name": 'kospi'}, {"$set": {"index": result}})


def renew_current_index():
    today = datetime.now().strftime('%Y-%m-%d')

    df_kosdaq_now = pdr.get_data_yahoo("^KQ11", today)
    kq_close_price = round(df_kosdaq_now.iloc[0]['Adj Close'], 2)
    db.index.update_one({'name': 'kosdaq'}, {'$set': {"current": kq_close_price}})
    redis.rpush('kosdaq', kq_close_price)

    df_kospi_now = pdr.get_data_yahoo("^KS11", today)
    ks_close_price = round(df_kospi_now.iloc[0]['Adj Close'], 2)
    db.index.update_one({"name": 'kospi'}, {"$set": {"current": ks_close_price}})
    redis.rpush('kospi', ks_close_price)