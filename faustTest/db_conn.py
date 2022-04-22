from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


class DatabaseConnect(object):
    def __init__(self, db_config_dict):
        self.__config = db_config_dict
        self.POOL_RECYCLE = 7200
        self.POOL_SIZE = 10
        self.MAX_OVERFLOW = 20
        self.POOL_TIMEOUT = 30
        url = URL(**self.__config)
        print(url)
        self.Engine = create_engine(url,
                                    pool_size=self.POOL_SIZE,
                                    max_overflow=self.MAX_OVERFLOW,
                                    pool_timeout=self.POOL_TIMEOUT,
                                    pool_recycle=self.POOL_RECYCLE)

    def get_conn(self):
        return self.Engine.connect()


if __name__ == '__main__':
    pass
