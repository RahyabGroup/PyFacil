__author__ = 'H.Rouhani'


class InoperableUserError(Exception):
    def __init__(self):
        super(InoperableUserError, self).__init__("Inoperable user.")
