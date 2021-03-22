from __future__ import annotations
from typing import Optional

from django.contrib import auth

from api.views_dir import base_view


class PasswordChangeView(base_view.BaseView):

    def __init__(self):
        super().__init__()
        self.url_parameters = ['current_password_hash', 'new_password_hash']

    def handle_put(self) -> Optional[PasswordChangeView]:
        if self.request.user.check_password(self.request.GET['current_password_hash']):
            self.request.user.set_password(self.request.GET['new_password_hash'])
            self.request.user.save()
            auth.login(self.request, self.request.user)
            return self
        else:
            return self.error(f'Wrong current password')

    # noinspection PyArgumentList
    def chain_put(self):
        self.authorize() \
            .require_url_parameters(self.url_parameters) \
            .request_handlers['PUT']['specific'](self)

    request_handlers = {
        'PUT': {
            'chain': chain_put,
            'specific': handle_put
        }
    }
