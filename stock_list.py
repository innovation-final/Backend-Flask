from pykrx import stock
from datetime import datetime

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock


def renew_stock_list():
    today = datetime.now().strftime("%Y%m%d")
    tickers = stock.get_market_ticker_list(today, market='ALL')
    for ticker in tickers:
        stock_name = stock.get_market_ticker_name(ticker)
        db.stocklist.update_one({"name": stock_name}, {"$set": {"code": ticker}}, upsert=True)