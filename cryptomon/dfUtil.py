from sqlalchemy import create_engine

# def write2mysql(df):
#   engine = create_engine("mysql+pymysql://{user}:{pw}@127.0.0.1:{port}/{db}"
#                          .format(user="root",
#                                  pw="rootpwd123",
#                                  port="4306",
#                                  db="cmc"))
#   df.to_sql(con=engine, name='cm_daily', if_exists='append', index=False)


# column filter
dictfilt = lambda x, y: dict([(i,x[i]) for i in x if i in set(y)])
columns1 = ['id','name','symbol','date_added']
columns2 = ['price','percent_change_24h','volume_24h','volume_change_24h','percent_change_7d','percent_change_30d','percent_change_90d','market_cap','last_updated']


# create dataframe
# df = pd.DataFrame(columns=columns1 + columns2)
# data = json.loads(response.text)['data']
# for row in data:
#   sub1 = dictfilt(row, columns1)
#   tmp = row['quote']['USD']
#   sub2 = dictfilt(tmp, columns2)
#   sub1.update(sub2)
#   rows.append(sub1)
# df = pd.DataFrame.from_dict(rows, orient='columns')
# write2mysql(df)