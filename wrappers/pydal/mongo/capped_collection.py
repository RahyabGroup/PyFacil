from .capped_read import CappedReadCommand
from .capped_write import CappedWriteCommand

__author__ = 'Hooman'


class CappedCollection:
    def __init__(self, collection_name, mongo_collection):
        self.collection_name = collection_name
        self._mongo_collection = mongo_collection

    def _get_reader(self):
        pydal_reader = CappedReadCommand(self._mongo_collection)
        return pydal_reader

    def _get_writer(self):
        pydal_writer = CappedWriteCommand(self._mongo_collection)
        return pydal_writer

    reader = property(_get_reader)
    writer = property(_get_writer)
