from cryptography.fernet import Fernet

__author__ = 'Hooman '


class StringCoder:
    def __init__(self, key):
        self.key = key

    def encode(self, string):
        encoder = Fernet(self.key)
        encoded_bytes = encoder.encrypt(string.encode())
        return encoded_bytes.decode()

    def decode(self, encoded_string):
        decoder = Fernet(self.key)
        decoded_bytes = decoder.decrypt(encoded_string.encode())
        return decoded_bytes.decode()
