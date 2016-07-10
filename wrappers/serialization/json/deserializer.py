from bson import json_util
import jsonpickle

__author__ = 'h.rouhani'


class Deserializer:
    def add_backend(self, backend_string):
        jsonpickle.load_backend(backend_string)
        jsonpickle.set_preferred_backend(backend_string)

    def deserialize_from_string(self, json_string):
        data = jsonpickle.decode(json_string)
        return data

    def deserialize_from_dictionary(self, json_dictionary, dumper=json_util):
        data_json_string = dumper.dumps(json_dictionary)
        return self.deserialize_from_string(data_json_string)
