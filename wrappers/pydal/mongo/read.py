from bson import SON
import pymongo

from ...serialization.json.deserializer import Deserializer
from .helper.document_normalizer import DocumentNormalizer

__author__ = 'Amir H. Nejati'


class ReadCommand:
    def __init__(self, mongo_collection):
        self._mongo_collection = mongo_collection

    def count(self, query=None):
        if query is None:
            document_count = self._mongo_collection.find().count()
        else:
            document_count = self._mongo_collection.find(query).count()
        return document_count

    def find_one(self, query, fields=[]):
        projection = None
        if fields and type(fields) is list:
            fields.append("py/object")
            projection = dict.fromkeys(fields, 1)
        elif fields and type(fields) is dict:
            fields = fields.copy()
            fields.update({"py/object": 1})
            projection = fields
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

    def aggregate(self, fields=[], skip=0, take=50, sort={'_id': pymongo.DESCENDING}, query=[]):
        aggregate_query = []
        aggregate_query.extend(query)
        if fields:
            fields.append("py/object")
            aggregate_query.append({"$project": dict.fromkeys(fields, 1)})
        aggregate_query.append({"$sort": sort})
        aggregate_query.append({"$skip": skip})
        aggregate_query.append({"$limit": take})
        documents = self._mongo_collection.aggregate(aggregate_query, useCursor=False)
        return self._get_list_of_object_from_list_of_mongo_document(documents)

    def aggregate_count(self, query=[], fields=[]):
        aggregate_query = []
        aggregate_query.extend(query)
        if fields:
            fields.append("py/object")
            aggregate_query.append({"$project": dict.fromkeys(fields, 1)})
        else:
            aggregate_query.append({"$project": {"_id": 1}})
        documents = self._mongo_collection.aggregate(aggregate_query, useCursor=False)
        result = self._get_list_of_object_from_list_of_mongo_document(documents)
        return len(result)

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

    def db_command(self, cmd):
        return self._mongo_collection.database.command(cmd)

    def find_cmd(self, select=None, project=None, sort=None, take=None, skip=None, tailable=False, reduce_by=None):
        cmd = SON([('find', self._mongo_collection.name)])
        cmd.update({'filter': select}) if select else None
        cmd.update({'projection': project}) if project else None
        cmd.update({'sort': sort}) if sort else None
        cmd.update({'skip': skip}) if skip else None
        cmd.update({'limit': take}) if take else None
        cmd.update({'tailable': tailable}) if tailable else None
        cmd.update({'singleBatch': True})
        cmd.update({'batchSize': 1000})
        docs = self.db_command(cmd)['cursor']['firstBatch']
        if hasattr(docs, '__iter__'):
            return [d if not reduce_by else reduce_by(**d) for d in docs]
            # for d in docs:
            #     yield d if not reduce_by else reduce_by().objectify(d)
        else:
            return docs if not reduce_by else reduce_by(**docs)

    def aggregate_cmd(self, pipeline, reduce_by=None):
        # cmd = SON([('aggregate', self._mongo_collection.name)])
        # [cmd.update(i) for i in pipeline if any(i.values())]
        # if deserialize and any([True for i in pipeline if '$project' in i]):
        #     pipeline[[i for i in range(len(pipeline))
        #               if '$project' in pipeline[i]][0]]['$project'].update({'py/object': 1})
        # docs = self.db_command(cmd)['result']
        [pipeline.remove(i) for i in pipeline if not any(i.values())]
        docs = self._mongo_collection.aggregate(pipeline=pipeline, useCursor=False)
        if hasattr(docs, '__iter__'):
            for d in docs:
                yield d if not reduce_by else reduce_by(**d)
        else:
            return docs if not reduce_by else reduce_by(**docs)

    def count_cmd(self, select=None, take=None, skip=None):
        cmd = SON([('aggregate', self._mongo_collection.name)])
        cmd.update({'query': select}) if select else None
        cmd.update({'limit': take}) if take else None
        cmd.update({'skip': skip}) if skip else None
        return self.db_command(cmd)['n']

    def distinct_cmd(self, key, query=None):
        cmd = SON([('distinct', self._mongo_collection.name)])
        cmd.update({'key': key})
        cmd.update({'query': key}) if query else None
        return self.db_command(cmd)['values']
