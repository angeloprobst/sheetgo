import os
import random
import sys

import jwt

def generate_jwt(email, jwt_secret_key):
    payload = {
        'email': email,
        'access_token': os.environ.get('DROPBOX_ACCESS_TOKEN', '')
    }
    return f'Bearer {jwt.encode(payload, jwt_secret_key).decode()}'

if __name__ == '__main__':
    jwt_secret_key = 'z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00'
    authorized_emails = ["lucas@sheetgo.com", "mauricio@sheetgo.com", "rafael@sheetgo.com"]
    print(
        generate_jwt(
            authorized_emails[random.randrange(len(authorized_emails))],
            jwt_secret_key
        )
    )
    sys.exit(0)
