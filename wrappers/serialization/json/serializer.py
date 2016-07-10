import json
from bson import json_util
import jsonpickle

__author__ = 'h.rouhani'


class Serializer:
    def add_handler(self, cls, handler):
        jsonpickle.handlers.registry.register(cls, handler)

    def serialize_to_string(self, data, include_class_path=True):
        if isinstance(data, str):
            return data
        data_json_string = jsonpickle.encode(data, unpicklable=include_class_path)
        return data_json_string

    def serialize_to_dictionary(self, data, include_class_path=True, object_hook=json_util.object_hook):
        data_json_string = self.serialize_to_string(data, include_class_path)
        data_json_dictionary = json.loads(data_json_string, object_hook=object_hook)
        return data_json_dictionary
