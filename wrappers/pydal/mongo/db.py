from .capped_collection import CappedCollection
from .collection import Collection

__author__ = 'Hooman'


class Db:
    def __init__(self, db_name, mongodb):
        self.db_name = db_name
        self.mongodb = mongodb

    def collection(self, name):
        mongo_collection = self.mongodb[name]
        pydal_collection = Collection(name, mongo_collection)
        return pydal_collection

    def capped_collection(self, name, size=10000000000):
        if name in self.mongodb.collection_names():
            mongo_collection = self.mongodb[name]
        else:
            mongo_collection = self.mongodb.create_collection(name, capped=True, size=size)
        pydal_collection = CappedCollection(name, mongo_collection)
        return pydal_collection
