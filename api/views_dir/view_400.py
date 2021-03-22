import json

from django.http import HttpRequest, HttpResponseBadRequest


class View400:

    response = json.dumps({'result': 'Bad request (ask admin to check ip in "ALLOWED_HOSTS"'})

    # noinspection PyUnusedLocal
    @staticmethod
    def as_view(request: HttpRequest, exception: Exception):
        return HttpResponseBadRequest(View400.response)
