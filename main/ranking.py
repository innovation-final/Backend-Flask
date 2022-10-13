import redis
from datetime import datetime

from pykrx import stock


from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock

redis = redis.StrictRedis(host="redis-12441.c294.ap-northeast-1-2.ec2.cloud.redislabs.com", port=12441,
                          password="uvLuMUsT4ChA2OJCDlDu5SkDtBzVEnQj")


def update_rank_data(df, criteria, cnt=10):
    result = []
    index = df.index.to_list()
    for i in range(cnt):
        stock_code = index[i]
        stock_name = stock.get_market_ticker_name(stock_code)
        first_price = str(int(df.iloc[i]["시가"]))
        high_price = str(int((df.iloc[i]["고가"])))
        low_price = str(int(df.iloc[i]["저가"]))
        last_price = str(int(df.iloc[i]["종가"]))
        volume = str(int(df.iloc[i]["거래량"]))
        trading_value = str(int(df.iloc[i]["거래대금"]))
        fluctuation_rate = str(df.iloc[i]["등락률"])
        temp = {
            "rank": str(i + 1),
            "stock_code": stock_code,
            "stock_name": stock_name,
            "first_price": first_price,
            "high_price": high_price,
            "low_price": low_price,
            "last_price": last_price,
            "volume": volume,
            "trading_value": trading_value,
            "fluctuation_rate": fluctuation_rate
        }
        result.append(temp)
    db.ranking.update_one({"criteria": criteria}, {"$set": {"data": result}})


def renew_ranking_top10():
    today = datetime.now().strftime("%Y%m%d")

    kospi = stock.get_market_ohlcv(today, market="KOSPI")  # 오늘 코스피 종목들의 OHLCV
    kosdaq = stock.get_market_ohlcv(today, market="KOSDAQ")  # 오늘 코스닥 종목들의 OHLCV

    update_rank_data(kospi.sort_values("등락률", ascending=False).head(10), "kospi_rate")
    update_rank_data(kospi.sort_values("거래량", ascending=False).head(10), "kospi_vol")

    update_rank_data(kosdaq.sort_values("등락률", ascending=False).head(10), "kosdaq_rate")
    update_rank_data(kosdaq.sort_values("거래량", ascending=False).head(10), "kosdaq_vol")


def renew_ranking_top100():
    today = datetime.now().strftime("%Y%m%d")

    kospi = stock.get_market_ohlcv(today, market="KOSPI")  # 오늘 코스피 종목들의 OHLCV
    kosdaq = stock.get_market_ohlcv(today, market="KOSDAQ")  # 오늘 코스닥 종목들의 OHLCV

    update_rank_data(kospi.sort_values("등락률", ascending=False).head(100), "kospi_rate_extend", 100)
    update_rank_data(kospi.sort_values("거래량", ascending=False).head(100), "kospi_vol_extend", 100)

    update_rank_data(kosdaq.sort_values("등락률", ascending=False).head(100), "kosdaq_rate_extend", 100)
    update_rank_data(kosdaq.sort_values("거래량", ascending=False).head(100), "kosdaq_vol_extend", 100)
