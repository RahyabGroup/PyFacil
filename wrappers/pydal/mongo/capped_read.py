import pymongo

from ...serialization.json.deserializer import Deserializer
from .helper.document_normalizer import DocumentNormalizer

__author__ = 'Hooman'


class CappedReadCommand:
    def __init__(self, mongo_collection):
        self._mongo_collection = mongo_collection

    def open_tailable_cursor(self, query, skip=0, take=10, natural_hint=-1):
        options = {'cursor_type': pymongo.CursorType.TAILABLE, 'skip': skip, 'limit': take}
        cursor = self._mongo_collection.find(query, **options).hint([('$natural', natural_hint)])
        return cursor

    def count(self, query=None):
        if query is None:
            document_count = self._mongo_collection.find().count()
        else:
            document_count = self._mongo_collection.find(query).count()
        return document_count

    def find_one(self, query, fields=[]):
        projection = None
        if fields:
            fields.append("py/object")
            projection = dict.fromkeys(fields, 1)
        document = self._mongo_collection.find_one(query, projection)
        if document is None:
            return None
        data = self._get_object_from_mongo_document(document)
        return data

    def find_many(self, query, fields=[], skip=0, take=50, sort={'_id': pymongo.DESCENDING}):
        sort = [(k, v) for k, v in sort.items()]
        projection = None
        if fields:
            fields.append("py/object")
            projection = dict.fromkeys(fields, 1)
        documents = self._mongo_collection.find(query, projection, skip=skip, limit=take, sort=sort)
        list_of_data = self._get_list_of_object_from_list_of_mongo_document(documents)
        return list_of_data

    def is_available(self, query):
        return self._mongo_collection.find_one(query, {"_id": 1}) is not None

    def _get_list_of_object_from_list_of_mongo_document(self, documents):
        results = []
        for document in documents:
            data = self._get_object_from_mongo_document(document)
            results.append(data)
        return results

    def _get_object_from_mongo_document(self, document):
        DocumentNormalizer.normalize_mongo_document_to_making_object(document)
        json_deserializer = Deserializer()
        data = json_deserializer.deserialize_from_dictionary(document)
        return data
