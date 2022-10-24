from datetime import datetime

import requests
import json
from pandas import json_normalize

def is_holiday():
    today = datetime.today().strftime('%Y%m%d')
    today_year = datetime.today().year
    today_month = datetime.today().month

    key = 'DVi48qFrQ23h%2FP88zVgEnYpckjKbUi0OhVHwacJ%2BvtgU%2FB%2BJb%2Bu29m1%2Fmz9rxjogRkp6PKsFWZz5I6lMbCsSJg%3D%3D'
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50&solYear=' + str(today_year) + '&solMonth=' + str(today_month) + '&ServiceKey=' + str(key)
    response = requests.get(url)
    if response.status_code == 200:
        json_ob = json.loads(response.text)
        holidays_data = json_ob['response']['body']['items']['item']
        dataframe = json_normalize(holidays_data)
    dateName = dataframe.loc[dataframe['locdate'] == int(today), 'dateName']

    return dateName.to_list() != []