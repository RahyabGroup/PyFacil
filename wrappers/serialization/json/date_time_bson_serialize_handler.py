import calendar
from jsonpickle.handlers import BaseHandler

__author__ = 'H.Rouhani'


class DatetimeBsonSerializeHandler(BaseHandler):
    def flatten(self, obj, data):
        res = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
        return {"$date": res}
