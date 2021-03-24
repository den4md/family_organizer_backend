from typing import Optional

from django.contrib import auth

from api.views_dir import base_view


class SignOutView(base_view.BaseView):

    def handle_post(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        auth.logout(self.request)
        return self

    # noinspection PyArgumentList
    def chain_post(self: base_view.BaseView):
        self.authorize() \
            .request_handlers['POST']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        }
    }
