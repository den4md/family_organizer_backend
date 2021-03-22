from __future__ import annotations
from typing import Optional

from django.contrib import auth

from api.views_dir import base_view


class SignOutView(base_view.BaseView):

    def handle_post(self) -> Optional[SignOutView]:
        auth.logout(self.request)
        return self

    # noinspection PyArgumentList
    def chain_post(self):
        self.authorize() \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
