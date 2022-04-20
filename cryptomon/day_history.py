import pandas as pd
from datetime import datetime

def history_data_reduce(result, all_columns):
    df = pd.DataFrame()
    for i in range(len(all_columns)-1, -1, -1):

        # 最大的日期
        x_date = all_columns[i]
        x_datetime = pd.to_datetime(x_date)
        x_temp = datetime.date(x_datetime)

        # 前一天的日期
        y_date = all_columns[i - 1]
        y_datetime = pd.to_datetime(y_date)
        y_temp = datetime.date(y_datetime)

        # 今天-前一天的
        result[str(x_temp)] = result[str(x_temp)] - result[str(y_temp)]
        df = result
    return df



if __name__ == '__main__':
    data = pd.read_csv("data.txt")

    result = pd.pivot_table(data, index='id', columns=['data'], values='value')

    # today = datetime.date.today()
    # yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    # result[str(today)] = result[str(today)]-result[str(yesterday)]
    # result[str(today)] = result.apply(lambda x: new_equals(x[str(today)]), axis=1)
    # print(result)

    all_columns = list(result.columns)

    df = history_data_reduce(result, all_columns)
    # df_2 = new_equals(df, all_columns)
    df[df > 0] = 1
    df[df < 0] = 0
    print(df)
    # print(df)