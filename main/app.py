import logging
import redis
from pykrx import stock

import news, stock_list, stock_detail, ranking, stock_current, index, fin_table
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore

from flask import Flask, jsonify

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from flask_cors import CORS
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')

redis = redis.StrictRedis(host="redis-12441.c294.ap-northeast-1-2.ec2.cloud.redislabs.com", port=12441,
                          password="uvLuMUsT4ChA2OJCDlDu5SkDtBzVEnQj")

app = Flask(__name__)


CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})


logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


sched = BackgroundScheduler(timezone='Asia/Seoul', job_defaults={'max_instances': 5}, jobstores={'default': MongoDBJobStore(client=client)})


@app.route('/jobs')
def get_schedule():
    return jsonify({"data": list(map(str, sched.get_jobs()))})


@app.route('/api/stock/today/<stock_code>')
def get_today_stock(stock_code):
    result = redis.lrange(stock_code, 0, -1)
    result = list(map(int, result))
    return jsonify({"price": result})


@app.route('/api/index/today/<index_name>')
def get_today_index(index_name):
    result = redis.lrange(index_name, 0, -1)
    result = list(map(int, result))
    return jsonify({"price": result})


# 뉴스
sched.add_job(news.get_news, 'interval', hours=3, id='get_news', replace_existing=True) # 매일 3시간마다

# 종목 리스트
sched.add_job(stock_list.renew_stock_list, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour=8, minute=30, id='renew_stock_list', replace_existing=True) # 월-금 8:30

# 코스피, 코스닥
sched.add_job(index.renew_current_index, 'cron', day_of_week='mon-fri', hour='9-15', minute='*/2', id='renew_current_index', replace_existing=True) # 월-금 9-15시 2분마다
sched.add_job(index.add_kosdaq, 'cron', day_of_week='mon-fri', hour=23, minute=59, id='add_kosdaq', replace_existing=True) # 월-금 23:59
sched.add_job(index.add_kospi, 'cron', day_of_week='mon-fri', hour=23, minute=59, id='add_kospi', replace_existing=True) # 월-금 23:59

# 주식차트, 시총
sched.add_job(stock_detail.add_data, 'cron', misfire_grace_time=None, args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour=15, minute=30, id='add_data', replace_existing=True) # 월-금 15:30
sched.add_job(stock_detail.renew_marcap, 'cron', day_of_week='fri', hour='23', id='renew_marcap', replace_existing=True)

# 주식 랭킹
sched.add_job(ranking.renew_ranking_top10, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour='9-15', minute='*/2', jitter=60, id='renew_ranking_top10', replace_existing=True)
sched.add_job(ranking.renew_ranking_top100, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour='9-15', minute='*/2', jitter=60, id='renew_ranking_top100', replace_existing=True)

# 주식 실시간
sched.add_job(stock_current.renew_stock_data, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour='9-15', minute='*/2', id='renew_stock_data', replace_existing=True)
sched.add_job(stock_current.set_expire_at, 'cron', args=[datetime.now()], day_of_week='mon-fri', hour='16', id='set_expire_at', replace_existing=True)

# 재무제표
sched.add_job(fin_table.renew_fin_table, 'cron', args=[fin_table.kosdaq_stocks, ".KQ"], month=12, id='renew_fin_table_kosdaq', replace_existing=True)
sched.add_job(fin_table.renew_fin_table, 'cron', args=[fin_table.kospi_stocks, ".KS"], month=12, id='renew_fin_table_kospi', replace_existing=True)


sched.start()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
