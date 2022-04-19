# 1) datetime to timestamp  1645228800
# 2)  startday + stepNum  schedule
# 3)  rest api  for startday
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=1&convertId=2781&timeStart=1637280000&timeEnd=1639785600
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={id}&convertId=2781&timeStart={starttime}&timeEnd={endtime}
# 4)  dataparlser

from datetime import datetime,timedelta

import requests
from bs4 import BeautifulSoup

from cryptomon.html_extractor import HtmlExtractor


def get_timestap():
    dt = datetime(2022, 2, 19, 8, 0, 0).timestamp()
    print(int(dt))

def get_deltaday(dayCap = 60):
    next_dt = (datetime(2022, 2, 19, 8, 0, 0)+ timedelta(days=dayCap)).timestamp()
    print(int(next_dt))

def get_data(self, symbol):
        """
        Get data from the symbol and parse it.
        :param symbol: Symbol
        :returns Array of market volume
        """
        ret = []
        response = requests.get(HtmlExtractor.URL % symbol)
        if response.status_code == 200:
            # Successful
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            market_table = None
            for table in tables:
                if table.has_attr('id'):
                    market_table = table
            assert market_table is not None, "Cannot find table markets-table"
            table_body = market_table.find_all('tbody')
            assert len(table_body) == 1, \
                "Number of table body (%d) should be equal to 1." % len(table_body)
            records = table_body[0].find_all('tr')

            # Parse each record
            for record in records:
                entries = record.find_all('td')
                exchange = entries[HtmlExtractor.EXCHANGE_INDEX].text
                pair = entries[HtmlExtractor.PAIR_INDEX].text
                price = re.search("(\d+\.*\d*)",
                                  entries[HtmlExtractor.PRICE_INDEX].text).group(0)
                price = float(price)
                market_share = re.search("(\d+\.*\d*)",
                                         entries[HtmlExtractor.MARKET_SHARE_INDEX].text).group(0)
                market_share = float(market_share)
                update = entries[HtmlExtractor.LATEST_UPDATE_INDEX].text
                if update == "Recently":
                    ret.append(CurrencyPair(exchange, pair, price, market_share))
        else:
            # Failed
            raise requests.exceptions.HTTPError("Http request error: %d" % response.status_code)

        return ret

