import json
from django.http import HttpResponse
from user.helper.string import *


def createJsonResponse(json_dict, error_header, status_code=200, dumps=True):
    # if dumps equals to False then jsonDict is already in json format
    if dumps:
        json_dict = json.dumps(json_dict)

    response = HttpResponse(json_dict, content_type=CONTENT_TYPE_JSON, status=status_code)
    response['error_code'] = error_header['error_code']
    response['error_message'] = error_header['error_message']

    return response
