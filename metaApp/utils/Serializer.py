from rest_framework.utils import json
from metaApp.utils.RaisingErrors import RaisingErrors


def get_token_from_request(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    if 'token' not in body_data:
        raise RaisingErrors.no_such_param('token')

    token = body_data['token']
    return token


def serialize_download_request(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    if 'token' not in body_data:
        raise RaisingErrors.no_such_param('token')
    if 'file_name' not in body_data:
        raise RaisingErrors.no_such_param('file_name')

    token = body_data['token']
    file_name = body_data['file_name']

    return token, file_name


def serialize_update_file_request(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)

    list_params = ['token', 'file_name', 'changing_params']
    for param in list_params:
        if param not in body_data:
            raise RaisingErrors.no_such_param('param')

    token = body_data['token']
    file_name = body_data['file_name']
    list_changing_params = body_data['changing_params']

    return token, file_name, list_changing_params
