"""
jwt封装
"""

import jwt


class Jwt:
    def __init__(self):
        self.secret = '%^&*qwertyuiop%^&%%^'

    def encode_token(self, data):
        return jwt.encode(data, self.secret, algorithm='HS256')

    def decode_token(self, token):
        return jwt.decode(token, self.secret, algorithms='HS256')

    def checked_token(self, tokens):
        payload = jwt.decode(tokens, self.secret, algorithms='HS256')
        token = jwt.encode(payload, self.secret, algorithm='HS256')
        if token == tokens:
            return True
        return False


jwt_token = Jwt()
