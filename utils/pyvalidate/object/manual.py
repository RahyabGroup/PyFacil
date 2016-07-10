__author__ = 'Hooman'


class Manual:
    data = None

    def __init__(self, data=""):
        self.data = data

    def validate(self, validation_error_code):
        validation_error_code["data"] = self.data
        return validation_error_code
