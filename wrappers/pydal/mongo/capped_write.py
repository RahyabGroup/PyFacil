from ...serialization.json.serializer import Serializer
from .helper.document_normalizer import DocumentNormalizer

__author__ = 'Hooman'


class CappedWriteCommand:
    def __init__(self, mongo_collection):
        self._mongo_collection = mongo_collection

    def save(self, data):
        serialized_data_dictionary = self._get_normalized_dictionary_to_persist_in_mongodb(data)
        data._id = str(serialized_data_dictionary["_id"])
        self._mongo_collection.save(serialized_data_dictionary)

    def add(self, data):
        serialized_data_dictionary = self._get_normalized_dictionary_to_persist_in_mongodb(data)
        data._id = str(serialized_data_dictionary["_id"])
        self._mongo_collection.insert(serialized_data_dictionary)

    def edit(self, data):
        serialized_data_dictionary = self._get_normalized_dictionary_to_persist_in_mongodb(data)
        self._mongo_collection.update({"_id": serialized_data_dictionary["_id"]}, serialized_data_dictionary)

    def edit_by_condition(self, first_query, second_query, multi=True):
        self._mongo_collection.update(first_query, second_query, multi=multi)

    def _get_normalized_dictionary_to_persist_in_mongodb(self, data):
        json_serializer = Serializer()
        data_json_dictionary = json_serializer.serialize_to_dictionary(data)
        DocumentNormalizer.normalize_serialized_dictionary_to_making_mongo_document(data_json_dictionary)
        return data_json_dictionary
