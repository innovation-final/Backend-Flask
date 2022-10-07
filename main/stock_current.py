from pykrx import stock

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock


def renew_stock_data(today):
    print("start renewing current stock")
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
    print("done renewing current stock")