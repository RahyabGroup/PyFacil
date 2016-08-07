from pymongo.mongo_client import MongoClient

from .db import Db

__author__ = 'Hooman'


class Connection:
    def __init__(self, host, port, user_name=None, password=None, **kwargs):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        if self.user_name:
            cs = 'mongodb://{username}:{password}@{host}:{port}/admin'
        else:
            cs = 'mongodb://{host}:{port}'
        self._mongo_connection = MongoClient(cs)

    def db(self, name):
        mongodb = self._mongo_connection[name]

        # if self.user_name and self.password:
        #     mongodb.authenticate(self.user_name, self.password, mechanism='SCRAM-SHA-1')

        pydaldb = Db(name, mongodb)
        return pydaldb
