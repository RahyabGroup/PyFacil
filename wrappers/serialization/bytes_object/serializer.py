import pickle

__author__ = 'Amir H. Nejati'


class Serializer:
    def serialize_to_bytes(self, data):
        bytes_string = pickle.dumps(data)
        return bytes_string
