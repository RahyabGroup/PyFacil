__author__ = 'Amir H.'


class WriteCommand:
    def __init__(self, riak_bucket):
        self._riak_bucket = riak_bucket

        # import riak
        # self._riak_bucket = riak.RiakClient().bucket_type().bucket()

    def set(self, key, value):
        obj = self._riak_bucket.new(key=key, data=value)
        obj.store()

    def update(self, key, value):
        obj = self._riak_bucket.get(key)
        obj.data = value
        obj.store()

    def delete(self, key):
        self._riak_bucket.delete(key)
