from __future__ import annotations
import json
import os
import traceback
from typing import Optional, Type, List

from django.core import exceptions
from django.db import models
from django.http import HttpResponse, HttpRequest
from rest_framework.exceptions import ValidationError

from api.helpers import write_style_helpers
from api.serializers_dir import base_app_serializer
from family_organizer import settings


def make_float(obj):
    return 0. if obj is None else float(obj)


def delete_file(file_path):
    os.remove(settings.FILE_STORAGE + file_path)


class BaseView:
    request_handlers = {}
    url_parameters = []

    def __init__(self):
        if type(self) == BaseView:
            raise TypeError('Can\'t initialize abstract class "BaseView"')

        self.response_dict = {
            'result': 'Ok'
        }
        self.status_code = 200
        self.request = None
        self.dict = {}  # Helping dict to store special vars

    @classmethod
    def as_view(cls, request: HttpRequest) -> HttpResponse:
        return cls().request_handle(request)

    def error(self, error_message: str, status_code: int = 400) -> None:
        self.response_dict['result'] = error_message
        self.status_code = status_code

    def request_handle(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        # noinspection PyUnusedLocal
        try:
            self.transmit_handle()
        except AttributeError as e:
            pass  # This error means that chain of responsibility was interrupted
        except Exception as e:
            self.response_dict = {}
            self.error(f'Unexpected error: {str(e)}', 500)
            traceback.print_exc()
        finally:
            if self.status_code >= 400:
                print(self.response_dict['result'])
            if 'response' not in self.dict.keys():
                self.dict['response'] = HttpResponse(json.dumps(self.response_dict), status=self.status_code)
        return self.dict['response']

    def transmit_handle(self):
        if self.request.method in self.request_handlers.keys():
            self.request_handlers[self.request.method]['chain'](self)
        else:
            self.error(f'Only ({", ".join(self.request_handlers.keys())})-method(-s) is permitted', 405)

    @staticmethod
    def var_name_from_model(model: Type[models.Model]):
        return write_style_helpers.camel_case_to_snake_case(model.__name__)

    # Predefined chain elements#
    ############################

    def no_authorize(self) -> Optional[BaseView]:
        if self.request.user.is_authenticated:
            return self.error('You are already signed in')
        else:
            return self

    def authorize(self) -> Optional[BaseView]:
        if not self.request.user.is_authenticated:
            return self.error('You should sign in first', 401)
        else:
            return self

    def require_url_parameters(self, parameters: List[str]) -> Optional[BaseView]:
        for parameter in parameters:
            if parameter not in self.request.GET.keys() or not self.request.GET[parameter]:
                return self.error(f'Can\'t find {parameter} in url parameters')
        return self

    def deserialize_json_body(self) -> Optional[BaseView]:
        try:
            self.dict['body_json'] = json.loads(self.request.body.decode('utf8'))
        except json.JSONDecodeError as e:
            return self.error(f'Error while deserializing: \n{str(e)}')
        else:
            return self

    def no_image_file_id(self: BaseView) -> Optional[BaseView]:
        if 'image_file_id' not in self.dict['body_json'].keys():
            return self
        else:
            return self.error(f'Image for registration is forbidden')

    def body_match_app_serializer(self, serializer: Type[base_app_serializer.BaseAppSerializer],
                                  required: bool = True) -> Optional[BaseView]:
        for key in self.dict['body_json'].keys():
            if key not in serializer.Meta.possible_fields:
                return self.error(f'Can\'t edit value for "{str(key)}"')
        if required:
            for required_field in serializer.Meta.required_fields:
                if required_field not in self.dict['body_json'].keys():
                    return self.error(f'Can\'t find value for "{str(required_field)}", but it\'s required')
        return self

    # Doesn't save
    def put_serializer(self, model: models.Model, serializer: Type[base_app_serializer.BaseAppSerializer]) -> \
            Optional[BaseView]:
        for key, value in self.dict['body_json'].items():
            if key in serializer.Meta.fields:
                setattr(model, key, value)
        return self

    def app_serializer_validation(self, serializer: Type[base_app_serializer.BaseAppSerializer]) -> Optional[BaseView]:
        self.dict['serializer'] = serializer(data=self.dict['body_json'])
        try:
            self.dict['serializer'].is_valid(raise_exception=True)
        except ValidationError as e:
            return self.error(f'Error while validating object: {str(e)}')
        else:
            return self

    def get_model_by_id(self, model: Type[models.Model], model_id: int) -> Optional[BaseView]:
        try:
            self.dict[self.var_name_from_model(model)] = model.objects.get(id=model_id)
        except exceptions.ObjectDoesNotExist:
            return self.error(f'{model.__name__} with id "{model_id}" does not exist', 404)
        except ValueError as e:
            return self.error(f'Wrong parameter type: \n{str(e)}')
        else:
            return self

    def user_belong_to_group(self, need_to_be=True) -> Optional[BaseView]:
        if self.request.user in self.dict['group'].user_member_list.all():
            if need_to_be:
                return self
            else:
                return self.error(f'You already belong to this group', 403)
        else:
            if need_to_be:
                return self.error(f'You don\'t belong to this group', 403)
            else:
                return self

    def model_belong_to_group(self, model_name: str) -> Optional[BaseView]:
        if (hasattr(self.dict[model_name], 'group') and self.dict[model_name].group != self.dict['group']) or (
                hasattr(self.dict[model_name], 'group_list') and
                self.dict['group'] not in self.dict[model_name].group_list.all()):
            return self.error(f'{model_name} with id = "{self.dict[model_name].id}" doesn\'t belong to group', 403)
        return self
