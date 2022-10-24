import time

import redis
from pykrx import stock
from datetime import datetime, timedelta

from pymongo import MongoClient

redis = redis.StrictRedis(host="redis-12441.c294.ap-northeast-1-2.ec2.cloud.redislabs.com", port=12441,
                          password="uvLuMUsT4ChA2OJCDlDu5SkDtBzVEnQj")

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock


def renew_stock_data():
    today = datetime.now().strftime("%Y%m%d")
    df = stock.get_market_ohlcv(today, market="ALL")
    index = df.index.to_list()
    for i in range(df.shape[0]):
        stock_code = index[i]
        # stock_name = stock.get_market_ticker_name(stock_code)
        first_price = str(int(df.iloc[i]["시가"]))
        high_price = str(int((df.iloc[i]["고가"])))
        low_price = str(int(df.iloc[i]["저가"]))
        last_price = str(int(df.iloc[i]["종가"]))
        volume = str(int(df.iloc[i]["거래량"]))
        trading_value = str(int(df.iloc[i]["거래대금"]))
        fluctuation_rate = str(df.iloc[i]["등락률"])
        result = {
            "first_price": first_price,
            "high_price": high_price,
            "low_price": low_price,
            "last_price": last_price,
            "volume": volume,
            "trading_value": trading_value,
            "fluctuation_rate": fluctuation_rate
        }
        db.chart.update_one({"code": stock_code}, {"$set": {"current": result}})
        redis.rpush(stock_code, last_price)


def set_expire_at():
    today = datetime.now()
    if today.weekday() == 4: # 금요일
        until = today + timedelta(days=3)
    else:
        until = today + timedelta(days=1)
    exp_date = until.date()
    exp_time = until.time().replace(8, 57, 0, 0)
    expire_at = datetime.combine(exp_date, exp_time)

    for key in redis.keys():
        redis.expireat(key.decode(), expire_at)