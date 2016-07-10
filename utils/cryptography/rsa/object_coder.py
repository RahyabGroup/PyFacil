from .string_coder import StringCoder
from pyfacil.wrappers.serialization.json.serializer import Serializer
from pyfacil.wrappers.serialization.json.deserializer import Deserializer

__author__ = 'Hooman'


class ObjectCoder(StringCoder):
    def encode(self, object):
        json_serializer = Serializer()
        object_json_string = json_serializer.serialize_to_string(object)
        encoded_string = super().encode(object_json_string)
        return encoded_string

    def decode(self, encoded_string):
        json_deserializer = Deserializer()
        json_string = super().decode(encoded_string)
        object = json_deserializer.deserialize_from_string(json_string)
        return object
