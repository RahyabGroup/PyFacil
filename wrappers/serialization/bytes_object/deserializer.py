import pickle

__author__ = 'Amir H. Nejati'


class Deserializer:
    def deserialize_from_bytes(self, bytes_string):
        data = pickle.loads(bytes_string)
        return data
