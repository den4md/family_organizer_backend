import json

from django.http import HttpRequest, HttpResponseNotFound


class View404:

    response = json.dumps({'result': 'Such URL was not found'})

    # noinspection PyUnusedLocal
    @staticmethod
    def as_view(request: HttpRequest, exception: Exception):
        return HttpResponseNotFound(View404.response)
