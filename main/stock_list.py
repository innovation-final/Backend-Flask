from pykrx import stock

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock


def renew_stock_list(today):
    print("start renewing stock list")
    tickers = stock.get_market_ticker_list(today, market='ALL')
    db.stocklist.delete_many({})
    for ticker in tickers:
        stock_name = stock.get_market_ticker_name(ticker)
        db.stocklist.insert_one({"name": stock_name, "code": ticker})

    print("done renewing stock list")
