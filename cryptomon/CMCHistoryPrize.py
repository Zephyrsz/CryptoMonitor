import requests
import json
from config import db
from models import CMCRank
from datetime import datetime

class HistoryPrizeExtractor(object):
    """
    Extract the cryptocurrency price information from the website coinmarketcap.
    By default, only the first 10 records (more than 10% of market cap) is recorded.
    """
    URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=5000&sortBy=market_cap&sortType=desc&convert=USD"
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
        response = requests.get(HistoryPrizeExtractor.URL)
        if response.status_code == 200:
            return response

    def data_parser(self,response):
        data = json.loads(response.text)
        crypoList= data['data']['cryptoCurrencyList']
        return crypoList

    # columns id ,rank ,symbol,rank_date


import pprint

try:
    extractor =HistoryPrizeExtractor()
    response = extractor.get_data()
    clist = extractor.data_parser(response)
    db.create_all()
    for c in clist:
        randdate = c.get("lastUpdated")[0:10]
        rkdt = datetime.fromisoformat(randdate)
        crank = CMCRank(id=c.get("id"),rank = c.get("cmcRank"),symbol = c.get("symbol"), rank_date = rkdt )
        if db.session.query(CMCRank).filter_by(id=crank.id).filter_by(rank_date=crank.rank_date ).first() is None:
            db.session.add(crank)
    db.session.commit()
except Exception as e:
    print(e)

