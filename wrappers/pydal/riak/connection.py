import riak

from .bucket_type import BucketType

__author__ = 'Amir H.'


class Connection:
    def __init__(self, host='127.0.0.1', port=8087, username=None, password=None, nodes=None, **kwargs):
        credentials = kwargs.get('credentials', {})
        if username and password:
            credentials.setdefault('username', username)
            credentials.setdefault('password', password)
        self._riak_client = riak.RiakClient(host=host, pb_port=port, protocol='pbc', credentials=credentials,
                                            nodes=nodes)

    def bucket_type(self, name):
        pyfas_bucket_type = BucketType(name, self._riak_client)
        return pyfas_bucket_type
