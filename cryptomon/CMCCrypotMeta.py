from datetime import datetime
from requests import Request, Session
import json

from config import db
from models import CMCCrypotMeta


# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'c26e10ef-b5cb-4783-877e-14d919f56db1',
}

session = Session()
session.headers.update(headers)

#['id','name','symbol','tag','date_added']
import pprint
try:
  # db.drop_all()
  # db.create_all()
  response = session.get(url, params=parameters)
  data = json.loads(response.text)['data']
  # pprint.pprint(data)
  for row in data:
    # pprint.pprint(row)
    tagList = row.get("tags")
    ## convert list to string
    tags = ' '.join(map(str, tagList))
    ## format orginal time value to iso format
    dtAdded = row.get("date_added")[0:19]
    fmtdt = datetime.fromisoformat(dtAdded)
    cmeta = CMCCrypotMeta(id=row.get("id"),name=row.get("name"),symbol=row.get("symbol"),tag=tags,date_added =fmtdt)
    ##判断是否存在该主键
    if db.session.query(CMCCrypotMeta).filter_by(id=cmeta.id).first() is None:
      db.session.add(cmeta)

  db.session.commit()
# except (ConnectionError, Timeout, TooManyRedirects, IntegrityError) as e:
except Exception as e:
  print(e)


