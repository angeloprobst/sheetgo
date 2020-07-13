import os
import unittest
import warnings

import jwt

from generate_jwt import generate_jwt


class TestGenerateJwt(unittest.TestCase):

    def test_generate_jwt(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        jwt_secret_key = 'z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00'
        authorized_emails = ["lucas@sheetgo.com", "mauricio@sheetgo.com", "rafael@sheetgo.com"]
        for email in authorized_emails:
            payload = {
                'email': email,
                'access_token': os.environ.get('DROPBOX_ACCESS_TOKEN', '')
            }
            decoded_payload = jwt.decode(
                generate_jwt(email, jwt_secret_key),
                jwt_secret_key
            )
            self.assertDictEqual(payload, decoded_payload)
