from ..float.negative import Negative
from ..float.positive import Positive
from ..float.size import Size
from ..validation_container import ValidationContainer

__author__ = 'h.rouhani'


class Container(ValidationContainer):
    def size(self, float_value, min_value=None, max_value=None, none_exception=True):
        float_size_validation = Size(min_value, max_value)
        return self._execute(float(float_value), float_size_validation, none_exception)

    def positive(self, float_value, include_zero=True, none_exception=True):
        positive_validation = Positive(include_zero)
        return self._execute(float_value, positive_validation, none_exception)

    def negative(self, float_value, include_zero=True, none_exception=True):
        negative_validation = Negative(include_zero)
        return self._execute(float_value, negative_validation, none_exception)