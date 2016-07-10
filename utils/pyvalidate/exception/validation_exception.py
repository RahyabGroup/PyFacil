__author__ = 'Hooman'


class ValidationException(Exception):
    def __init__(self, errors):
        super(ValidationException, self)
        self.errors = errors

    def _getErrors(self):
        return self.errors

    Errors = property(_getErrors)
