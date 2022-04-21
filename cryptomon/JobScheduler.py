# 1) datetime to timestamp  1645228800
# 2)  startday + stepNum  schedule
# 3)  rest api  for startday
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=1&convertId=2781&timeStart=1637280000&timeEnd=1639785600
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={id}&convertId=2781&timeStart={starttime}&timeEnd={endtime}
# 4)  dataparlser
# 5 main page request
#  https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=101&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap

from datetime import datetime,timedelta,date

def init():
    today = datetime.now()
    return get_start_timestap(today.year,today.month,today.day)

def get_start_timestap(year,month,day):
    dt = datetime(year, month, day, 8, 0, 0)
    return dt

def get_deltaday(startday,dayCap):
    next_dt = (startday - timedelta(days=dayCap))
    return next_dt


init_start_day = init()
gap = 60
remain_day = 1000
iter_count = 1000//gap
inter = 0

for i in range(1,iter_count):
    startday = get_deltaday(init_start_day,inter)
    endday = get_deltaday(startday,gap)
    inter = inter + gap + 1
    print(inter)
    # print("###############")
    print("start_day is %s, end_day is %s" % (int(startday.timestamp()),int(endday.timestamp())))

