__author__ = 'Hooman'


class AuthorizationError(Exception):
    def __init__(self):
        super(AuthorizationError, self).__init__("Not authorized user.")
