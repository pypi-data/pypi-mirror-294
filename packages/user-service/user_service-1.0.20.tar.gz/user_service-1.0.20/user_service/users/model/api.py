from sqlalchemy import create_engine
from sqlalchemy.orm import (Session)

from abc import ABC, abstractmethod

class IDBDriver(ABC):
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    @abstractmethod
    def generate_driver_url(self):
        pass

class MySQLDriver(IDBDriver):
    def __init__(self, user_name, password, database, host, port):
        self.__driver = "mysql+pymysql://"
        self.__user_name = user_name
        self.__password = password
        self.__port = port
        self.database = database
        self.host = host
        self.session = self.connect()
    def generate_driver_url(self):
        url = (self.__driver + self.__user_name + ":" +
               self.__password + "@" + self.host + ":" +
               self.__port + "/" + self.database)
        return url

    def connect(self):
        sess = None
        try:
            engine = create_engine(self.generate_driver_url())
            sess = Session(engine)
            return sess
        except Exception as ex:
            print(ex)
        finally:
            sess.close()

    def disconnect(self):
        pass

session = MySQLDriver('root',
                      password='strong_password',
                      database='users',
                      host='192.168.1.33',
                      port='3307').connect()


