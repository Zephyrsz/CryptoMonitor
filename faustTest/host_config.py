from sqlalchemy import engine
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

DATA_MASTER_DB = {
    "drivername": "mysql+pymysql",
    "host": 'data_analysis_m.db.xiaoying.io',
    "port": 3306,
    "username": 'data',
    "password": 'xL8sG4NtiJZKRU',
    "database": 'cluster_monitor',
    "query": {"charset": 'utf8'}
}

OPS_MASTER_DB = {
    "drivername": "mysql+pymysql",
    "host": '10.0.20.99',
    "port": 3306,
    "username": 'p2p_dev',
    "password": 'p2p_dev',
    "database": 'xy_ops',
    "query": {"charset": 'utf8'}
}

url = engine.url.URL(**DATA_MASTER_DB)
ops_url = engine.url.URL(**OPS_MASTER_DB)
db_conn = create_engine(url, poolclass=NullPool, connect_args={'connect_timeout': 10})
ops_db_conn = create_engine(ops_url, poolclass=NullPool, connect_args={'connect_timeout': 10})
ipList = ['10.2.0.5', '10.0.194.131', '10.0.10.198', '10.0.193.116']
ipList = [
    '10.2.0.5',
    '10.0.193.116',
    '10.0.194.131',
    '10.0.10.198',
    '10.0.4.35',
    '10.3.0.29',

    'xydw32',
    'xydw33',
    'xydw34',
    'xydw35',
    'xydw36',
    'xydw37',
    'xydw38',
    'xydw39',
    'xydw41',
    'xydw42',
    'xydw43',
    'xydw44',
    'xydw45',
    'xydw46',
    'xydw47',
    'xydw48',
    'xydw49',
    'xydw50',
    'xydw51',
    'xydw52',
    'xydw53',
    'xydw54',
    'xydw55',
    'xydw56',
    'xydw57',

    'xybase01',
    'xybase02',
    'xybase07',
    'xybase08',

    'xybase09',
    'xybase10',
    'xybase11',
    'xybase12',

    'xykfk01',
    'xykfk02',
    'xykfk03',
    'xykfk04',
    'xykfk05'
]

ipList = [
    # '10.2.0.5',
    # '10.0.193.116',
    # '10.0.194.131',
    # '10.0.10.198',
    # '10.0.4.35',
    # '10.3.0.29',

    '10.3.0.9',
    '10.3.0.2',
    '10.3.0.3',
    '10.3.0.4',
    '10.3.0.5',
    '10.3.0.6',
    '10.3.0.7',
    '10.3.0.8',
    '10.3.0.11',
    '10.3.0.12',
    '10.3.0.13',
    '10.3.0.14',
    '10.3.0.15',
    '10.3.0.16',
    '10.3.0.17',
    '10.3.0.18',
    '10.3.0.19',
    '10.3.0.20',
    '10.3.0.21',
    '10.3.0.22',
    '10.3.0.23',
    '10.3.0.24',
    '10.3.0.25',
    '10.3.0.26',
    '10.3.0.27',

    '10.2.0.44',
    '10.2.0.45',
    '10.3.0.40',
    '10.3.0.41',

    '10.3.0.47',
    '10.3.0.48',
    '10.3.0.49',
    '10.3.0.46',

    '10.0.122.8',
    '10.0.122.10',
    '10.0.122.15',
    '10.0.122.3',
    '10.0.122.16'
]

ipList = [
    '10.0.192.132',
    '10.0.192.197'
]
