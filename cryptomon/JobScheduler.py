# 1) datetime to timestamp  1645228800
# 2)  startday + stepNum  schedule
# 3)  rest api  for startday
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=1&convertId=2781&timeStart=1637280000&timeEnd=1639785600
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={id}&convertId=2781&timeStart={starttime}&timeEnd={endtime}
# 4)  dataparlser
# 5 main page request
#  https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=101&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap
import json
from datetime import datetime, timedelta, date

import requests


def initday():
    today = datetime.now()
    return get_start_timestap(today.year, today.month, today.day)


def get_start_timestap(year, month, day):
    dt = datetime(year, month, day, 8, 0, 0)
    return dt


def get_deltaday(startday, dayCap):
    next_dt = (startday - timedelta(days=dayCap))
    return next_dt


init_start_day = initday()
gap = 60
remain_day = 1000
iter_count = 1000 // gap
inter = 0

for i in range(1, iter_count):
    startday = get_deltaday(init_start_day, inter)
    endday = get_deltaday(startday, gap)
    inter = inter + gap + 1
    print(inter)
    # print("###############")
    print("start_day is %s, end_day is %s" % (int(startday.timestamp()), int(endday.timestamp())))


def getJobCidlist() -> list:
    pass


def getJobRange(cid):
    pass


baseUrl = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={}&convertId=2781&timeStart={}&timeEnd={}"

class HistoryPrizeExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={}&convertId=2781&timeStart={}&timeEnd={}"  ###.format(cid,start,end)
    # URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=3&limit=1&sortBy=market_cap&sortType=descconvert=USD&cryptoType=all"
    # URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=3&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap"
    def __init__(self, cid, start, end):
        """
        Constructor
        """
        self.cid = cid
        self.start = start
        self.end = end

    # def get_data(self):
    #     """
    #     Get data from the symbol and parse it.
    #     :param symbol: Symbol
    #     :returns Array of market volume
    #     """
    #     extactor = HistoryPrizeExtractor()
    #
    #     response = requests.get(HistoryPrizeExtractor.URL)
    #     if response.status_code == 200:
    #         return response

    def data_parser(self, response):
        data = json.loads(response.text)
        crypoList = data['data']['cryptoCurrencyList']
        return crypoList


### 一天时间 86400
###

def crwal_history(cid, start, end):
    gap = 10000000
    remain = start - end
    while (remain > 0):
        extactor = HistoryPrizeExtractor(cid, start, start - gap)
        url = baseUrl.format(cid, start, start - gap)
        remain = remain - gap
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            pass
