import re
from ..resources import ErrorCodes

__author__ = 'h.rouhani'


class Email:
    def validate(self, item_to_validate):
        email_pattern = "[^@]+@[^@]+\.[^@]+"
        if not re.match(email_pattern, item_to_validate):
            result = ErrorCodes.EMAIL_NOT_VALID
            result["data"] = item_to_validate
            return result
        return None
