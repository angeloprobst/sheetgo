import io
import os
import unittest
import warnings

import jwt
from PIL import Image

import sheetgo


class TestSheetGo(unittest.TestCase):

    def test_check_auth_token(self):
        # empty token
        err, res = sheetgo.check_auth_token({})
        self.assertTrue(err == 400)
        self.assertTrue(res == 'empty token')
        err, res = sheetgo.check_auth_token({'Authorization': ''})
        self.assertTrue(err == 400)
        self.assertTrue(res == 'empty token')
        err, res = sheetgo.check_auth_token({'X-Authentication-Token': ''})
        self.assertTrue(err == 400)
        self.assertTrue(res == 'empty token')

        warnings.filterwarnings("ignore", category=DeprecationWarning)
        jwt_secret_key = 'z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00'
        authorized_emails = ["lucas@sheetgo.com", "mauricio@sheetgo.com", "rafael@sheetgo.com"]

        # success
        for email in authorized_emails:
            payload = {
                'email': email,
                'access_token': os.environ.get('DROPBOX_ACCESS_TOKEN', '')
            }
            auth_token = jwt.encode(payload, jwt_secret_key).decode()
            headers = {'Authorization': f'Bearer {auth_token}'}
            err, res = sheetgo.check_auth_token(headers)
            self.assertFalse(err)
            self.assertDictEqual(res, payload)

        # invalid token
        payload = {
            'email': "lucas@sheetgo.com",
            'access_token': os.environ.get('DROPBOX_ACCESS_TOKEN', '')
        }
        invalid_token = 'aaaa1234'
        auth_token = jwt.encode(payload, invalid_token).decode()
        headers = {'Authorization': f'Bearer {auth_token}'}
        err, res = sheetgo.check_auth_token(headers)
        self.assertTrue(err == 400)
        self.assertTrue(res == 'invalid token')

        # unauthorized email
        payload['email'] = "test@test.com"
        auth_token = jwt.encode(payload, jwt_secret_key).decode()
        headers = {'Authorization': f'Bearer {auth_token}'}
        err, res = sheetgo.check_auth_token(headers)
        self.assertTrue(err == 401)
        self.assertTrue(res == 'unauthorized')

    def test_convert_image(self):
        # invalid output format arg
        with self.assertRaises(ValueError) as ctx:
            sheetgo.convert_image(None, 'bmp')
            self.assertTrue('invalid value' in ctx.exception)
            sheetgo.convert_image(None, 'jpg')  # should be "jpeg" instead of "jpg"
            self.assertTrue('invalid value' in ctx.exception)

        # input image in jpeg format, output format arg is also jpeg
        with open('tests/street-lights.jpg', 'rb') as f:
            input_image = io.BytesIO(f.read())
        output_image = sheetgo.convert_image(input_image, 'jpeg')
        oi = Image.open(output_image)
        self.assertEqual(input_image, output_image)  # must be the same file
        self.assertTrue(oi.format.lower() == 'jpeg')

        # conversion from jpeg to png
        output_image = sheetgo.convert_image(input_image, 'png')
        oi = Image.open(output_image)
        self.assertTrue(oi.format.lower() == 'png')

        # input image in png format, output format arg is also png
        with open('tests/street-lights.png', 'rb') as f:
            input_image = io.BytesIO(f.read())
        output_image = sheetgo.convert_image(input_image, 'png')
        oi = Image.open(output_image)
        self.assertEqual(input_image, output_image)  # must be the same file
        self.assertTrue(oi.format.lower() == 'png')

        # conversion from png to jpeg
        output_image = sheetgo.convert_image(input_image, 'jpeg')
        oi = Image.open(output_image)
        self.assertTrue(oi.format.lower() == 'jpeg')
