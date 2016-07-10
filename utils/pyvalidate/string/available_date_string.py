import dateutil.parser
from ..resources import ErrorCodes

__author__ = 'H.Rouhani'


class AvailableDateString:
    def validate(self, item_to_validate):
        try:
            dateutil.parser.parse(item_to_validate)
            return None
        except:
            result = ErrorCodes.DATE_TIME_STRING_IS_NOT_VALID
            result["data"] = item_to_validate
            return result
