### dataframe colomns
###  id, rank_chnage ,rank_yesterday, rank_today


##计算方法
####
# 1）id 在昨天存在， rank_chnage = rank_yestory - rank_today  （变小则为正）
# 2) id 在昨天不存在， 则rankchange =  5000 - rank_today ，rank_yesterday = null
# 3） 退出排行榜 ， 则rankchange =  rank_yesday - 5000 ， rank_today = null ,


##### load data from db to df
import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

######
sql_base = '''SELECT * FROM  cmcrank '''
limit_condition = ''' limit 10'''
# limit_condition = '''  '''
today = datetime.datetime.today()
yestoday = datetime.datetime.today() - datetime.timedelta(days=1)
dt_today = str(today.date())
dt_yestoday = str(yestoday.date())

engine = create_engine(
    "mysql+pymysql://root:rootpwd123@localhost:4306/cmc?charset=utf8mb4")


def df_today():
    time_condition = str("where rank_date =" + "'" + dt_today + "'")
    sql = '{}{}{}'.format(sql_base, time_condition, limit_condition)
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
        df_today = pd.DataFrame(query.fetchall(), columns=['tid', 'cmcid', 'cmcrank', 'symbol', 'rank_date'])
    return df_today


def df_yesday():
    time_condition = str("where rank_date =" + "'" + dt_yestoday + "'")
    sql = '{}{}{}'.format(sql_base, time_condition, limit_condition)
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
        df_yesday = pd.DataFrame(query.fetchall(), columns=['tid', 'cmcid', 'cmcrank', 'symbol', 'rank_date'])
    return df_yesday


df_today = df_today()

for idx,data in df_today.iterrows():
    print(data.get("tid"))



# df_yesday = df_yesday()
# df_all = merged_df = pd.merge(df_today, df_yesday, how='outer', on=['cmcid'], suffixes=('_today', '_yestoday'))
#
# df_change = pd.DataFrame(columns=['cmcid', 'symbol', 'cmc_date', 'rank_change', 'rank_today', 'rank_yestoday'])

##  insert data to dataframe method
## df = df.append({'A': 1, 'B': 12.3, 'C': 'xyz'}, ignore_index=True)
####  df.loc[len(df)] = [a, b, c]

# columns=['cmcid', 'symbol', 'cmc_date', 'rank_change', 'rank_today', 'rank_yestoday']
# for row in df_all:
#     if row['cmcrank_today'] is not np.nan and row['cmcrank_today'] is not np.nan:
#         r_cmcid = row['cmcid_today']
#         r_sybol = row['sybol_today']
#         r_cmc_date = row['rank_date_today']
#         r_rank_today = int(row['rank_rank_today'])
#         r_rank_yestoday = int(row['rank_rank_yestoday'])
#         r_ranchange = r_rank_yestoday - r_rank_today
#         df_change = df_change.append(
#             {'cmcid': r_cmcid, 'symbol': r_sybol, 'cmc_date': r_cmc_date, 'rank_today': r_rank_today,
#              'rank_yestoday': r_rank_yestoday, 'rank_change': r_ranchange}, ignore_index=True)
#     if row['cmcrank_today'] is np.nan and row['cmcrank_today'] is not np.nan:
#         r_cmcid = row['cmcid_today']
#         r_sybol = row['sybol_today']
#         r_cmc_date = row['rank_date_today']
#         r_rank_today = row['rank_rank_today']
#         r_rank_yestoday = int(row['rank_rank_yestoday'])
#         r_ranchange = r_rank_yestoday - 5000
#         df_change = df_change.append(
#             {'cmcid': r_cmcid, 'symbol': r_sybol, 'cmc_date': r_cmc_date, 'rank_today': r_rank_today,
#              'rank_yestoday': r_rank_yestoday, 'rank_change': r_ranchange}, ignore_index=True)
#     if row['cmcrank_today'] is not np.nan and row['cmcrank_today'] is np.nan:
#         r_cmcid = row['cmcid_today']
#         r_sybol = row['sybol_today']
#         r_cmc_date = row['rank_date_today']
#         r_rank_today = int(row['rank_rank_today'])
#         r_rank_yestoday = row['rank_rank_yestoday']
#         r_ranchange = 5000 - r_rank_yestoday
#         df_change = df_change.append(
#             {'cmcid': r_cmcid, 'symbol': r_sybol, 'cmc_date': r_cmc_date, 'rank_today': r_rank_today,
#              'rank_yestoday': r_rank_yestoday, 'rank_change': r_ranchange}, ignore_index=True)
#
#
# print(df_change)
