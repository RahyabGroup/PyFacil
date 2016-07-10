from .bucket import Bucket

__author__ = 'Amir H.'


class BucketType:
    def __init__(self, name, riak_client):
        self._bucket_type_name = name
        self._bucket_type = riak_client.bucket_type(name)

    def bucket(self, name):
        pyfas_bucket = Bucket(name, self._bucket_type)
        return pyfas_bucket
