import news, stock_list, stock_detail, ranking, stock_current, index, fin_table
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask


sched = BackgroundScheduler(timezone='Asia/Seoul', job_defaults={'max_instances': 5})

# 뉴스
sched.add_job(news.get_news, 'cron', hour='*/3', id='get_news') # 매일 3시간마다

# 종목 리스트
sched.add_job(stock_list.renew_stock_list, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour=8, minute=30, id='renew_stock_list') # 월-금 8:30

# 코스피, 코스닥
sched.add_job(index.renew_current_index, 'cron', day_of_week='mon-fri', hour='9-15', minute='*/2', id='renew_current_index') # 월-금 9-15시 2분마다
sched.add_job(index.add_kosdaq, 'cron', day_of_week='mon-fri', hour=23, minute=59, id='add_kosdaq') # 월-금 23:59
sched.add_job(index.add_kospi, 'cron', day_of_week='mon-fri', hour=23, minute=59, id='add_kospi') # 월-금 23:59

# 주식차트, 시총
sched.add_job(stock_detail.add_data, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour=15, minute=30, id='add_data') # 월-금 15:30
sched.add_job(stock_detail.renew_marcap, 'cron', day_of_week='fri', hour='23', id='renew_marcap') # 매주 금요일 자정마다

# 주식 랭킹
sched.add_job(ranking.renew_ranking_top10, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour='9-15', minute='*/2', id='renew_ranking_top10')
sched.add_job(ranking.renew_ranking_top100, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour='9-15', minute='*/2', id='renew_ranking_top100')

# 주식 실시간
sched.add_job(stock_current.renew_stock_data, 'cron', args=[datetime.now().strftime("%Y%m%d")], day_of_week='mon-fri', hour='9-15', minute='*/2', id='renew_stock_data')

# 재무제표
sched.add_job(fin_table.renew_fin_table, 'cron', args=[fin_table.kosdaq_stocks, ".KQ"], month=12, id='renew_fin_table_kosdaq')
sched.add_job(fin_table.renew_fin_table, 'cron', args=[fin_table.kospi_stocks, ".KS"], month=12, id='renew_fin_table_kospi')


sched.start()

app = Flask(__name__)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)




