from __future__ import annotations
from typing import Optional

from django.contrib import auth

from api.views_dir import base_view


class SignInView(base_view.BaseView):

    def __init__(self):
        super().__init__()
        self.url_parameters = ['email', 'password_hash']

    def handle_post(self) -> Optional[SignInView]:
        user = auth.authenticate(self.request, username=self.request.GET['email'],
                                 password=self.request.GET['password_hash'])
        if user is None:
            return self.error(f'Wrong credentials')
        else:
            auth.login(self.request, user)
            return self

    def chain_post(self):
        self.no_authorize() \
            .require_url_parameters(self.url_parameters) \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
