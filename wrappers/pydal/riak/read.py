__author__ = 'Amir H. Nejati'


class ReadCommand:
    def __init__(self, riak_bucket):
        self._riak_bucket = riak_bucket

        # import riak
        # self._riak_bucket = riak.RiakClient().bucket_type().bucket()

    def get(self, key):
        data = self._riak_bucket.get(key).data
        return data

    def mget(self, keys_list):
        yield [v.data for v in self._riak_bucket.multiget(keys_list)]

    def get_all_keys(self):
        return self._riak_bucket.get_keys()

    def map_reduce(self, map_func, reduce_func=None):
        query = self._riak_bucket._client.add(self._riak_bucket.name,
                                              bucket_type=self._riak_bucket.bucket_type.name)
        query.map(map_func)
        if reduce_func:
            query.reduce(reduce_func)
        return query.run()

