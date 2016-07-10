from .read import ReadCommand
from .write import WriteCommand

__author__ = 'Hooman'


class Collection:
    def __init__(self, collection_name, mongo_collection):
        self.collection_name = collection_name
        self._mongo_collection = mongo_collection

    def _get_reader(self):
        pydal_reader = ReadCommand(self._mongo_collection)
        return pydal_reader

    def _get_writer(self):
        pydal_writer = WriteCommand(self._mongo_collection)
        return pydal_writer

    reader = property(_get_reader)
    writer = property(_get_writer)
