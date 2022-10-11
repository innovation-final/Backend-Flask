import html
import json
import urllib.request

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.stock_stock

client_id = "7OMY0HaZANsrK_AIE5Jx"
client_secret = "h0BsFxG13F"


def get_news():
    stocks = list(db.chart.find({}))
    for i, stock in enumerate(stocks):
        stock_name = stock["name"]
        # print(f"{i + 1}/{2650} {stock_name}")

        encText = urllib.parse.quote(stock_name + "주식")
        url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=5"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result_str = response_body.decode('utf-8')
            result = json.loads(result_str)["items"]
            for j in range(len(result)):
                result[j]['title'] = html.unescape(result[j]['title']).replace("<b>", "").replace("</b>", "")
            db.news.update_one({"name": stock_name}, {"$set": {"data": result}})
        else:
            # print("Error Code:" + rescode)
            continue
    print("done getting news")