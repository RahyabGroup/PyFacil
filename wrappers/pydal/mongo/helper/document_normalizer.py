from builtins import staticmethod
from bson import ObjectId

__author__ = 'h.rouhani'


class DocumentNormalizer:
    @staticmethod
    def normalize_mongo_document_to_making_object(document):
        document["_id"] = str(document["_id"])
        return document

    @staticmethod
    def normalize_serialized_dictionary_to_making_mongo_document(dictionary):
        if dictionary.__contains__("_id"):
            dictionary["_id"] = ObjectId(dictionary["_id"])
        else:
            dictionary["_id"] = ObjectId()
        return dictionary

    @staticmethod
    def normalize_id_string_for_mongodb(id_string):
        return ObjectId(id_string)
