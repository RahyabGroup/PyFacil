import re

from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class OnlyString:
    def validate(self, item_to_validate):
        farsi_alef_char = chr(1570)
        farsi_ye_char = chr(1740)
        only_string_pattern = '^[a-zA-Z{}-{} \n]+$'.format(farsi_alef_char, farsi_ye_char)
        if not re.match(only_string_pattern, item_to_validate):
            result = ErrorCodes.ITEM_IS_NOT_ONLY_STRING
            result["data"] = item_to_validate
            return result
        return None
