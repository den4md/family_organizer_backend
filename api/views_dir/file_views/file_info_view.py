from api.models_dir import file, group
from api.serializers_dir import file_serializers
from api.views_dir import base_view


class FileInfoView(base_view.BaseView):

    def handle_get(self):
        if 'group_id' in self.request.GET.keys():
            if not self.request.GET['group_id']:
                return self.error('No "group_id" value is granted')
            else:
                if not self.get_model_by_id(group.Group,
                                            self.request.GET['group_id']) or not self.user_belong_to_group():
                    return
        else:
            self.dict['group'] = None

        if self.dict['file'].group != self.dict['group'] or (
                not self.dict['group'] and self.dict['file'].user_uploader != self.request.user):
            return self.error(f'File with id "{self.request.GET["file_id"]}" does not exist', 404)

        self.response_dict['file_data'] = file_serializers.FileServSerializer(self.dict['file']).data
        return self

    def chain_get(self):
        self.authorize()\
            .require_url_parameters(['file_id'])\
            .get_model_by_id(file.File, self.request.GET['file_id']) \
            .request_handlers['GET']['specific'](self)

    request_handlers = {
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        }
    }
