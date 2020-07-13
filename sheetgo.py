import io
import os
import sys

import dropbox
import flask
import jwt
from flask import Flask, Response, make_response, request, send_file
from openpyxl import load_workbook
from PIL import Image

app = Flask(__name__)


def check_auth_token(headers):
    auth_token = headers.get('Authorization', '') or \
        headers.get('X-Authentication-Token', '')
    if not str(auth_token).strip():
        return 400, 'empty token'
    jwt_secret_key = 'z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00'
    authorized_emails = ["lucas@sheetgo.com", "mauricio@sheetgo.com", "rafael@sheetgo.com"]
    try:
        payload = jwt.decode(str(auth_token).replace('Bearer ', '').strip(), jwt_secret_key)
        if payload.get('email', '') in authorized_emails:
            return False, payload
        else:
            raise jwt.InvalidTokenError()
    except jwt.DecodeError:
        return 400, 'invalid token'
    except jwt.InvalidTokenError:
        return 401, 'unauthorized'


def make_error_response(code, error_message, exception_message=None):
    return flask.make_response(
        flask.jsonify(
            {'error': error_message}
            if exception_message is None else
            {'error': error_message, 'exception': exception_message}
        ),
        code
    )


@app.route('/excel/info', methods=['POST'], strict_slashes=False)
def excel_info():
    err, res = check_auth_token(request.headers)
    if err:
        return make_error_response(err, res)

    f = request.files.get('file', None)
    if not f:
        return make_error_response(400, 'file is missing')

    sheet_file = io.BytesIO()
    f.save(sheet_file)
    try:
        wb = load_workbook(sheet_file)
        return flask.make_response(flask.jsonify(sorted(wb.get_sheet_names())), 200)

    except Exception as ex:
        return make_error_response(400, 'error reading xlsx file', str(ex))


def convert_image(input_image, output_format):
    if output_format.lower() not in ['png', 'jpeg']:
        raise ValueError('invalid value in format parameter')
    input_image.seek(0)
    ii = Image.open(input_image)
    if ii.format.lower() == output_format.lower():
        return input_image
    output_image = io.BytesIO()
    ii.convert('RGB').save(fp=output_image, format=output_format)
    output_image.seek(0)
    return output_image


def make_image_convert_response(input_image, output_format):
    if output_format.lower() not in ['png', 'jpeg']:
        return make_error_response(400, 'invalid value in format parameter')
    try:
        return send_file(
            convert_image(input_image, output_format),
            mimetype=f'image/{output_format.lower()}'
        )
    except Exception as ex:
        return make_error_response(400, 'error converting image', str(ex))


@app.route('/image/convert', methods=['POST'], strict_slashes=False)
def image_convert():
    err, res = check_auth_token(request.headers)
    if err:
        return make_error_response(err, res)

    output_format = request.args.get('format', '')
    if not output_format:
        return make_error_response(400, 'format parameter is missing')

    f = request.files.get('file', None)
    if not f:
        return make_error_response(400, 'file is missing')

    input_image = io.BytesIO()
    f.save(input_image)
    input_image.seek(0)
    return make_image_convert_response(input_image, output_format)


@app.route('/image/convert/fromdropbox', methods=['POST'], strict_slashes=False)
def image_convert_fromdropbox():
    err, res = check_auth_token(request.headers)
    if err:
        return make_error_response(err, res)

    output_format = request.args.get('format', '')
    if not output_format:
        return make_error_response(400, 'format parameter is missing')

    image_path = request.args.get('image_path', '')
    if not image_path:
        return make_error_response(400, 'image_path parameter is missing')

    dropbox_access_token = res.get('access_token', '')
    if not dropbox_access_token:
        return make_error_response(400, 'dropbox access token is missing')

    try:
        dbx = dropbox.Dropbox(dropbox_access_token)
        _, res = dbx.files_download(path=image_path)
    except Exception as ex:
        return make_error_response(400, 'error on dropbox access', str(ex))

    input_image = io.BytesIO(res.content)
    return make_image_convert_response(input_image, output_format)


if __name__ == '__main__':
    app.run()
