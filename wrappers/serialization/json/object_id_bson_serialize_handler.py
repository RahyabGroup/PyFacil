from jsonpickle.handlers import BaseHandler

__author__ = 'H.Rouhani'


class ObjectIdBsonSerializeHandler(BaseHandler):
    def flatten(self, obj, data):
        return {"$oid": str(obj)}

    def restore(self, data):
        return data
