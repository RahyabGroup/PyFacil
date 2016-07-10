__author__ = 'Hooman'


class AuthenticationError(Exception):
    def __init__(self):
        super(AuthenticationError, self).__init__("Not authenticated user.")
