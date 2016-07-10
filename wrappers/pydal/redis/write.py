from ...serialization.bytes_object.serializer import Serializer

__author__ = 'Amir H. Nejati'


class WriteCommand:
    def __init__(self, redis_con):
        self._redis_con = redis_con

    def set(self, key, value, ex=None, px=None, nx=None, xx=None, serialize=True):
        value = self._serialize_to_bytes(value) if serialize else value
        self._redis_con.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def hset(self, key, index, value, serialize=True):
        value = self._serialize_to_bytes(value) if serialize else value
        self._redis_con.hset(key, index, value)

    def getset(self, key, value, serialize=True):
        value = self._serialize_to_bytes(value) if serialize else value
        return self._redis_con.getset(key, value)

    def enqueue(self, qname, *values, serialize=True):
        values = map(self._serialize_to_bytes, values) if serialize else values
        self._redis_con.lpush(qname, *values)

    def incr(self, key, amount=1):
        self._redis_con.incr(key, amount)

    def decr(self, key, amount=1):
        self._redis_con.decr(key, amount)

    def delete(self, *keys):
        self._redis_con.delete(*keys)

    def _serialize_to_bytes(self, data):
        if data is None:
            return None
        bytes_object_serializer = Serializer()
        bytes_str = bytes_object_serializer.serialize_to_bytes(data)
        return bytes_str
