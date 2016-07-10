from ..integer.equality import Equality
from ..integer.negative import Negative
from ..integer.positive import Positive
from ..integer.size import Size
from ..validation_container import ValidationContainer

__author__ = 'h.rouhani'


class Container(ValidationContainer):
    def size(self, int_value, min_value=None, max_value=None, none_exception=True):
        int_size_validation = Size(min_value, max_value)
        return self._execute(int_value, int_size_validation, none_exception)

    def positive(self, int_value, include_zero=True, none_exception=True):
        positive_validation = Positive(include_zero)
        return self._execute(int_value, positive_validation, none_exception)

    def negative(self, int_value, include_zero=True, none_exception=True):
        negative_validation = Negative(include_zero)
        return self._execute(int_value, negative_validation, none_exception)

    def equality(self, int_value, compare_with, none_exception=True):
        integer_equality_validator = Equality(compare_with)
        return self._execute(int_value, integer_equality_validator, none_exception)
