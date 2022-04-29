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
# limit_condition = ''' limit 10'''
limit_condition = '''  '''
today = datetime.datetime.today()-datetime.timedelta(days=2)
yestoday = today - datetime.timedelta(days=1)
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


def df_yestoday():
    time_condition = str("where rank_date =" + "'" + dt_yestoday + "'")
    sql = '{}{}{}'.format(sql_base, time_condition, limit_condition)
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
        df_yesday = pd.DataFrame(query.fetchall(), columns=['tid', 'cmcid', 'cmcrank', 'symbol', 'rank_date'])
    return df_yesday


df_today = df_today()
#
# for idx,data in df_today.iterrows():
#     print(data.get("tid"))



df_yestoday = df_yestoday()
df_all = merged_df = pd.merge(df_today, df_yestoday, how='outer', on=['cmcid'], suffixes=('_today', '_yestoday'))
#
df_change = pd.DataFrame(columns=['cmcid', 'symbol', 'cmc_date', 'rank_change', 'rank_today', 'rank_yestoday'])

# print(df_all.columns)
# print(len(df_all))
# ### test
# for idx,row in df_all.iterrows():
#     if row.get('cmcid') == 8611:
#         print(row.get('cmcid'),row.get('cmcrank_today'),row.get('cmcrank_yestoday'))
#         print(np.isnan(row.get('cmcrank_yestoday')))


##  insert data to dataframe method
## df = df.append({'A': 1, 'B': 12.3, 'C': 'xyz'}, ignore_index=True)
####  df.loc[len(df)] = [a, b, c]

### df_all columns ['tid_today', 'cmcid', 'cmcrank_today', 'symbol_today','rank_date_today', 'tid_yestoday', 'cmcrank_yestoday','symbol_yestoday', 'rank_date_yestoday']
####df_change olumns=['cmcid', 'symbol', 'cmc_date', 'rank_change', 'rank_today', 'rank_yestoday']
for idx,row in df_all.iterrows():
    if ~np.isnan(row.get('cmcrank_today')) and ~np.isnan(row.get('cmcrank_yestoday')):
        r_cmcid = row.get('cmcid')
        r_sybol = row.get('symbol_today')
        r_cmc_date = row.get('rank_date_today')
        r_rank_today = int(row.get('cmcrank_today'))
        r_rank_yestoday = int(row.get('cmcrank_yestoday'))
        r_ranchange = r_rank_yestoday - r_rank_today
        df_change = df_change.append(
            {'cmcid': r_cmcid, 'symbol': r_sybol, 'cmc_date': r_cmc_date, 'rank_today': r_rank_today,
             'rank_yestoday': r_rank_yestoday, 'rank_change': r_ranchange}, ignore_index=True)
    if np.isnan(row.get('cmcrank_today')) and ~np.isnan(row.get('cmcrank_yestoday')):   ### 退出排行榜
        r_cmcid = row.get('cmcid')
        r_sybol = row.get('symbol_yestoday')
        r_cmc_date = row.get('rank_date_today')
        r_rank_today = row.get('cmcrank_today')
        r_rank_yestoday = int(row.get('cmcrank_yestoday'))
        r_ranchange = r_rank_yestoday - 5000
        df_change = df_change.append(
            {'cmcid': r_cmcid, 'symbol': r_sybol, 'cmc_date': r_cmc_date, 'rank_today': r_rank_today,
             'rank_yestoday': r_rank_yestoday, 'rank_change': r_ranchange}, ignore_index=True)
    if ~np.isnan(row.get('cmcrank_today'))  and np.isnan(row.get('cmcrank_yestoday')):   ###新晋排行榜
        r_cmcid = row.get('cmcid')
        r_sybol = row.get('symbol_today')
        r_cmc_date = row.get('rank_date_today')
        r_rank_today = int(row.get('cmcrank_today'))
        r_rank_yestoday = row.get('cmcrank_yestoday')
        r_ranchange = 5000 - r_rank_yestoday
        df_change = df_change.append(
            {'cmcid': r_cmcid, 'symbol': r_sybol, 'cmc_date': r_cmc_date, 'rank_today': r_rank_today,
             'rank_yestoday': r_rank_yestoday, 'rank_change': r_ranchange}, ignore_index=True)


with engine.connect().execution_options(autocommit=True) as conn:
    df_change.to_sql('cmcchange', con=conn, if_exists='append', index= False)