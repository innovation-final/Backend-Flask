from pykrx import stock
from datetime import datetime
import yfinance as yf
import pymongo

client = pymongo.MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock

kospi_stocks = stock.get_market_ticker_list(datetime.now().strftime("%Y%m%d"), market="KOSPI")
kosdaq_stocks = stock.get_market_ticker_list(datetime.now().strftime("%Y%m%d"), market="KOSDAQ")

def renew_fin_table(stocks, str):
    for stock in stocks:
        code = yf.Ticker(stock + str)
        financials = code.financials
        sheet = code.balance_sheet
        cashflow = code.cashflow
        try:
            arr_final = []
            arr_fin = ['Total Revenue', 'Net Income From Continuing Ops', 'Operating Income']
            for i in range(len(arr_fin)):
                arr_temp = []
                for z in reversed(range(0, 4)):
                    try:
                        arr_temp.append(str(round(financials.loc[arr_fin[i]].iloc[z] / 100000000)))
                    except:
                        arr_temp.append("None")
                        continue
                arr_final.append(arr_temp)

            arr_sh = ['Total Assets', 'Total Liab']
            for i in range(len(arr_sh)):
                arr_temp = []
                for z in reversed(range(0, 4)):
                    try:
                        arr_temp.append(str(round(sheet.loc[arr_sh[i]].iloc[z] / 100000000)))
                    except:
                        arr_temp.append("None")
                        continue
                arr_final.append(arr_temp)

            arr_cf = ['Total Cash From Operating Activities']
            for i in range(len(arr_cf)):
                arr_temp = []
                for z in reversed(range(0, 4)):
                    try:
                        arr_temp.append(str(round(cashflow.loc[arr_cf[i]].iloc[z] / 100000000)))
                    except:
                        arr_temp.append("None")
                        continue
                arr_final.append(arr_temp)
            db.finsInfo.update_one({"code": stock}, {"$set": {"data": arr_final}})
        except:
            continue