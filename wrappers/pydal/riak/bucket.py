from .read import ReadCommand
from .write import WriteCommand

__author__ = 'Amir H.'


class Bucket:
    def __init__(self, name, bucket_type):
        self._bucket_name = name
        self._bucket = bucket_type.bucket(name)

    @property
    def reader(self):
        pyfas_reader = ReadCommand(self._bucket)
        return pyfas_reader

    @property
    def writer(self):
        pyfas_writer = WriteCommand(self._bucket)
        return pyfas_writer
