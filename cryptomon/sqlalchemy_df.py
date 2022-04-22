import sqlalchemy
import pandas as pd


##### load data from db to df
from sqlalchemy import engine
from sqlalchemy.sql import text
sql = '''
    SELECT * FROM table;
'''
with engine.connect().execution_options(autocommit=True) as conn:
    query = conn.execute(text(sql))
df = pd.DataFrame(query.fetchall())

### run multiple sql in df
sql = '''
    DROP TABLE IF EXISTS df;
    CREATE TABLE df(
            id SERIAL PRIMARY KEY,
            salary integer
    );
    INSERT INTO df (salary)
    VALUES 
            (400),
            (200),
            (3001);
    SELECT * FROM df;
'''
with engine.connect().execution_options(autocommit=True) as conn:
    query = conn.execute(text(sql))
df = pd.DataFrame(query.fetchall())


#### operate
# Update rows in a SQL table
sql = '''
    UPDATE table 
    SET col='abc'
    WHERE condition;
'''
with engine.connect().execution_options(autocommit=True) as conn:
    conn.execute(text(sql))
# Insert new rows in a SQL table
sql = '''
    INSERT INTO df
    VALUES 
       (1, 'abc'),
       (2, 'xyz'),
       (1, 'abc');
'''
with engine.connect().execution_options(autocommit=True) as conn:
    conn.execute(text(sql))
# Delete rows in a SQL table
sql = '''
    DELETE FROM df
    WHERE condition;
'''
with engine.connect().execution_options(autocommit=True) as conn:
    conn.execute(text(sql))

#### write df data to db with sqlalchemy
df = pd.read_excel('sample.xlsx')
with engine.connect().execution_options(autocommit=True) as conn:
    df.to_sql('table_name', con=conn, if_exists='append', index= False)



### creat new database
from sqlalchemy.types import Integer, Text, String, DateTime
df = pd.read_excel('sample.xlsx')
df.to_sql(
    "table_name",
    con = engine,
    if_exists = "replace",
    schema='shcema_name',
    index=False,
    chunksize=1000,
    dtype={
        "col_1_name": Integer,
        "col_2_name": Text,
        "col_3_name": String(50),
        "col_4_name": DateTime
    }
)
