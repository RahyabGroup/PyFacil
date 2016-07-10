from ..string.available_date_string import AvailableDateString
from ..string.email import Email
from ..string.empty import Empty
from ..string.equality import Equality
from ..string.only_string import OnlyString
from ..string.size import Size
from ..string.text_size import TextSize
from ..validation_container import ValidationContainer

__author__ = 'h.rouhani'


class Container(ValidationContainer):
    def size(self, string, min_size=None, max_size=None, none_exception=True):
        string_size_validation = Size(min_size, max_size)
        return self._execute(string, string_size_validation, none_exception)

    def text_size(self, string, min_size=None, max_size=None, none_exception=True):
        text_size_validation = TextSize(min_size, max_size)
        return self._execute(string, text_size_validation, none_exception)

    def email(self, email, none_exception=True):
        email_validation = Email()
        return self._execute(email, email_validation, none_exception)

    def only_string(self, string, none_exception=True):
        only_string_validation = OnlyString()
        return self._execute(string, only_string_validation, none_exception)

    def equality(self, string, compare_with, none_exception=True):
        string_equality_validator = Equality(compare_with)
        return self._execute(string, string_equality_validator, none_exception)

    def empty(self, string):
        empty_string_validator = Empty()
        return self._execute(string, empty_string_validator, True)

    def available_date_string(self, item_to_validate, none_exception=True):
        available_date_string_validation = AvailableDateString()
        return self._execute(item_to_validate, available_date_string_validation, none_exception)
