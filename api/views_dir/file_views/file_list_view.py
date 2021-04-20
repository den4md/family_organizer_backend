from api.models_dir import group, file
from api.serializers_dir import file_serializers
from api.views_dir import base_view


class FileListView(base_view.BaseView):

    def handle_get(self):
        if 'group_id' in self.request.GET.keys():
            if self.request.GET['group_id'] is None:
                return self.error('No "group_id" value is granted')
            else:
                if not self.get_model_by_id(group.Group, self.request.GET['group_id']) or \
                        not self.user_belong_to_group():
                    return
        else:
            self.dict['group'] = None

        if self.dict['group'] is not None:
            file_list = file.File.objects.filter(group=self.dict['group'])
        else:
            file_list = file.File.objects.filter(group=None, user_uploader=self.request.user)

        self.response_dict['file_list'] = file_serializers.FileServSerializer(file_list, many=True).data
        return self

    # noinspection PyArgumentList
    def chain_get(self):
        self.authorize()\
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        }
    }
