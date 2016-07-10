from ...serialization.bytes_object.deserializer import Deserializer

__author__ = 'Amir H. Nejati'


class ReadCommand:
    def __init__(self, redis_con):
        self._redis_con = redis_con

    def get(self, key, deserialize=True):
        data = self._redis_con.get(key)
        data = self._deserialize_from_bytes(data) if deserialize else data
        return data

    def hget(self, key, index, deserialize=True):
        data = self._redis_con.hget(key, index)
        data = self._deserialize_from_bytes(data) if deserialize else data
        return data

    def dequeue(self, qname, blocking=False, deserialize=True):
        if blocking:
            data = self._redis_con.brpop(qname)
            data = data[1] if data else data
        else:
            data = self._redis_con.rpop(qname)
            data = data[1] if data else data
        data = self._deserialize_from_bytes(data) if deserialize else data
        return data

    def _deserialize_from_bytes(self, bytes_str):
        if bytes_str is None:
            return None
        bytes_str_deserializer = Deserializer()
        data = bytes_str_deserializer.deserialize_from_bytes(bytes_str)
        return data
