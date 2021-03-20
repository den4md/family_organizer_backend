from api.views_dir import base_view


class SignInView(base_view.BaseView):

    def view_post(self):
        self.no_authorize()

    # specific_handlers = {
    #     'POST': handle_post
    # }

    method_handlers = {
        'POST': view_post
    }
