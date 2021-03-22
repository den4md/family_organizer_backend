from __future__ import annotations
import json
import string
import traceback
from typing import Optional, Type, List, Any

from django.core import exceptions
from django.db import models
from django.http import HttpResponse, HttpRequest
from rest_framework.exceptions import ValidationError

from api.serializers_dir import base_serializer


class BaseView:
    request_handlers = {}

    def __init__(self):
        if type(self) == BaseView:
            raise TypeError('Can\'t initialize abstract class \'BaseView\'')

        self.response_dict = {
            'result': 'Ok'
        }
        self.status_code = 200
        self.request = None
        self.dict = {}  # Helping dict to store special vars

    @classmethod
    def as_view(cls, request: HttpRequest) -> HttpResponse:
        return cls().request_handle(request)

    def request_handle(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        try:
            self.transmit_handle()
        except AttributeError:
            pass  # This error means that chain of responsibility was interrupted
        except Exception as e:
            self.response_dict = {'result': f'Unexpected error: {str(e)}'}
            self.status_code = 500
            print(traceback.print_exc())
        finally:
            return HttpResponse(json.dumps(self.response_dict), status=self.status_code)

    def transmit_handle(self):
        if self.request.method in self.request_handlers.keys():
            self.request_handlers[self.request.method]['chain'](self)
        else:
            self.response_dict['result'] = f'Only ({", ".join(self.request_handlers.keys())})-method(-s) is permitted'
            self.status_code = 405

    @classmethod
    def validate(cls, obj: Any, validating_type):
        if type(obj) != validating_type:
            try:
                validating_type(obj)
            except ValueError:
                return False
        return True

    # Predefined chain elements#
    ############################
    def no_authorize(self) -> Optional[BaseView]:
        if self.request.user.is_authenticated:
            self.response_dict['result'] = 'You are already signed in'
            self.status_code = 400
        else:
            return self

    def authorize(self) -> Optional[BaseView]:
        if not self.request.user.is_authenticated:
            self.response_dict['result'] = 'You should sign in first'
            self.status_code = 401
        else:
            return self

    def require_url_parameters(self, parameters: List[str]) -> Optional[BaseView]:
        for parameter in parameters:
            if parameter not in self.request.GET.keys():
                self.response_dict['result'] = f'Can\'t find {parameter} in url parameters'
                self.status_code = 400
                return None
        return self

    def deserialize_json_body(self) -> Optional[BaseView]:
        try:
            self.dict['body_json'] = json.loads(self.request.body.decode('utf8'))
        except json.JSONDecodeError as e:
            self.response_dict['result'] = f'Error while deserializing: \n{str(e)}'
            self.status_code = 400
        else:
            return self

    def body_match_serializer(self, serializer: Type[base_serializer.BaseAppSerializer], required: bool = True) -> \
            Optional[BaseView]:
        for key in self.dict['body_json'].keys():
            if key not in serializer.Meta.possible_fields:
                self.response_dict['result'] = f'Can\'t edit value for \'{str(key)}\''
                self.status_code = 400
                return None
        if required:
            for required_field in serializer.Meta.required_fields:
                if required_field not in self.dict['body_json'].keys():
                    self.response_dict[
                        'result'] = f'Can\'t find value for \'{str(required_field)}\', but it\'s required'
                    self.status_code = 400
                    return None
        return self

    # Doesn't save
    def put_serializer(self, model: models.Model, serializer: Type[base_serializer.BaseAppSerializer]) -> \
            Optional[BaseView]:
        for key, value in self.dict['body_json'].items():
            if key in serializer.Meta.fields:
                setattr(model, key, value)
        return self

    def deserializer_validation(self, serializer: Type[base_serializer.BaseAppSerializer]) -> Optional[BaseView]:
        self.dict['serializer'] = serializer(data=self.dict['body_json'])
        try:
            self.dict['serializer'].is_valid(raise_exception=True)
        except ValidationError as e:
            self.response_dict['result'] = f'Error while validating object: {str(e)}'
            self.status_code = 400
        else:
            return self

    @staticmethod
    def var_name_from_model(model: Type[models.Model]):
        model_name = model.__name__
        temp = []
        while True:
            found_upper = False
            for i in range(1, len(model_name)):
                if model_name[i] in string.ascii_uppercase:
                    temp.append(model_name[:i].lower())
                    model_name = model_name[i:]
                    found_upper = True
                    break
            if not found_upper:
                break
        temp.append(model_name.lower())
        return '_'.join(temp)

    def get_model_by_id(self, model: Type[models.Model], model_id) -> Optional[BaseView]:
        try:
            self.dict[self.var_name_from_model(model)] = model.objects.get(id=model_id)
        except exceptions.ObjectDoesNotExist:
            self.response_dict['result'] = f'{model.__name__} does not exist'
            self.status_code = 400
        except ValueError as e:
            self.response_dict['result'] = f'Wrong parameter type: \n{str(e)}'
            self.status_code = 400
        else:
            return self

    def user_belong_to_group(self) -> Optional[BaseView]:
        if self.request.user not in self.dict['group'].user_member_list.all():
            self.response_dict['result'] = f'You don\'t belong to this group'
            self.status_code = 403
        else:
            return self
