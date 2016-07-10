from redis import Redis

from .read import ReadCommand
from .write import WriteCommand

__author__ = 'Amir H.'


class Connection:
    def __init__(self, host='localhost', port=6379, db=0, password=None, **kwargs):
        """redis 'sentinel' / 'strict' parameters can be passed by kwargs"""
        self._redis_connection = Redis(host=host, port=port, db=db, password=password)

    @property
    def host(self):
        return self._redis_connection.connection_pool.connection_kwargs['host']
        # return self._host

    @property
    def port(self):
        return self._redis_connection.connection_pool.connection_kwargs['port']
        # return self._port

    @property
    def db_name(self):
        return self._redis_connection.connection_pool.connection_kwargs['db']
        # return self._db

    @property
    def password(self):
        return self._redis_connection.connection_pool.connection_kwargs['password']
        # return self._password

    @property
    def reader(self):
        pyfas_reader = ReadCommand(self._redis_connection)
        return pyfas_reader

    @property
    def writer(self):
        pyfas_writer = WriteCommand(self._redis_connection)
        return pyfas_writer
