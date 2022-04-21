#!/bin/python
from bs4 import BeautifulSoup
import requests
import re

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class Currency(object):
    """
    meta information of a currency.
    """
    def __init__(self, ID, startTime, price, market_share):
        """
        Constructor
        """
        self.id = ID
        self.startTime = startTime
        self.price = price
        self.market_share = market_share
    
    def __str__(self):
        return ("Exchange: %s, Pair: %s, Price: %.8f, Market share: %.2f%%" %
                (self.ID, self.startTime, self.price, self.market_share))

class Currency_daily_prize(object):
    """
     History daily prize .Date	Open High Low Close	Volume	Market_Cap
    """
    def __init__(self, name, prize, Date, Open,high,low,close,volume,market_cap):
        """
        Constructor
        """
        self.name = name,
        self.prize = prize,
        self.Date = Date,
        self.Open = Open,
        self.high = high,
        self.low = low,
        self.close = close,
        self.volume = volume,
        self.market_cap = market_cap

    def __str__(self):
        return ("Name: %s, prize: %s, Date: %s, open: %.2f%%, high: %.2f%%,open: %.2f%%,high: %.2f%%,low: %.2f%%,close: %.2f%%,volume: %.2f%%,market_cap: %.2f%%" %
                (self.name,self.prize,self.Date,self.Open,self.high,self.low,self.close,self.volume,self.market_cap))

class HtmlExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    # URL = "https://coinmarketcap.com/currencies/%s/#markets"
    URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=%s&convertId=2781&timeStart=%s&timeEnd=%s"
    def __init__(self):
        """
        Constructor
        """
        pass
    
    def get_data(self, id, startDt,endDt):
        """
        Get data from the symbol and parse it.
        :param symbol: Symbol
        :returns Array of market volume
        """
        ret = []
        response = requests.get(HtmlExtractor.URL % (id,startDt,endDt))
        if response.status_code == 200:
            return response

    def history_parser(self,response):
        data = json.loads(response.text)
        dataIner= data['data']
        id = dataIner['id']
        name = dataIner['name']
        quotes = dataIner['quotes']
        return quotes
        # for quote in data:
        #     quote_data=quote['quote']

    def timeStamp_generator(self, date_start, day_gap =60):
        pass

class MainExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=3&sortBy=market_cap&sortType=desc&convert=USD"
    # URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=3&limit=1&sortBy=market_cap&sortType=descconvert=USD&cryptoType=all"
    # URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=3&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap"

    def __init__(self):
        """
        Constructor
        """
        pass

    def get_data(self):
        """
        Get data from the symbol and parse it.
        :param symbol: Symbol
        :returns Array of market volume
        """
        response = requests.get(MainExtractor.URL)
        if response.status_code == 200:
            return response

    def data_parser(self,response):
        data = json.loads(response.text)
        crypoList= data['data']['cryptoCurrencyList']
        return crypoList
        # for quote in data:
        #     quote_data=quote['quote']

    def schema_map(self,crypoList):
        pass


import pprint
extractor =MainExtractor()
response = extractor.get_data()
clist = extractor.data_parser(response)

for c in clist:
    pprint.pprint(c)
    print("#################")

# data = json.loads(response.text)
# pprint.pprint(data)

###grace print json data
import pprint
        
# if __name__ == '__main__':
#     extractor = HtmlExtractor()
#     id = 1
#     start = 1645228800
#     end = 1650326400
#     response = extractor.get_data(id,start,end)
#     data = extractor.history_parser(response)
#     # print(type(data))
#     for quote in data:
#         quote_data=quote['quote']
#         print(quote_data)
#     # pprint.pprint(data)

