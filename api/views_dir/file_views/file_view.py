import datetime
import hashlib
import os
import re
from typing import Optional

from django.http import HttpResponse

from api.views_dir import base_view
from api.models_dir import file, group
from family_organizer import settings


def check_for_duplicate(this_file_path, that_file_path):
    buffer = 1024

    this_file = open(this_file_path, 'rb')
    that_file = open(that_file_path, 'rb')

    this_data, that_data = read_files_chunk(buffer, that_file, this_file)

    while this_data and that_data:
        if this_data != that_data:
            return False
        this_data, that_data = read_files_chunk(buffer, that_file, this_file)
    this_file.close()
    that_file.close()
    return this_data == that_data


def read_files_chunk(buffer, that_file, this_file):
    return this_file.read(buffer), that_file.read(buffer)


def get_file_attributes(file_name: str) -> tuple:
    name = file_name
    for banned_symbol in FileView.banned_symbols:
        name = name.replace(banned_symbol, '_')
    name = re.sub(r'\.*$', '', name)

    extension = re.findall(r'^.+?\.', name[::-1])
    if len(extension):
        extension = extension[0][-2:-17:-1]
    else:
        extension = ''

    path = name
    name = re.sub(r'^.*?\.', '', name[::-1])[::-1]

    if file.File.objects.filter(file_path=path).count():
        path = name + datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S.') + extension

    return name, extension, path


class FileView(base_view.BaseView):
    banned_symbols = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    def handle_post(self: base_view.BaseView) -> Optional[base_view.BaseView]:
        # Check for files number in request
        if not self.request.FILES:
            return self.error('No file was found')
        if len(list(self.request.FILES.values())) > 1:
            return self.error('Several files were found. Can accept only one')

        # Get file and it's name attributes
        request_file = list(self.request.FILES.values())[0]
        file_name, file_extension, file_path = get_file_attributes(request_file.name)

        # Write file and get it's checksum
        checksum_md5 = hashlib.md5()
        with open(settings.FILE_STORAGE + file_path, 'wb') as storage_file:
            for chunk in request_file.chunks(4096):
                storage_file.write(chunk)
                checksum_md5.update(chunk)
        storage_file.close()
        checksum_md5 = checksum_md5.hexdigest()

        # Get group data if it need
        if 'group_id' in self.request.GET.keys():
            if self.request.GET['group_id']:
                if not (self.get_model_by_id(group.Group, self.request.GET['group_id'])
                        and self.user_belong_to_group()):
                    return
            else:
                return self.error('No "group_id" value is granted')
        else:
            self.dict['group'] = None

        # Get list of same file in group or by user that uploads
        same_files = file.File.objects.filter(checksum_md5=checksum_md5)
        if 'group_id' in self.request.GET.keys():
            same_files = same_files.filter(group=self.dict['group'])
        else:
            same_files = same_files.filter(user_uploader=self.request.user)

        # Check for duplicates
        if same_files.count():
            for same_file in same_files.iterator():
                if check_for_duplicate(settings.FILE_STORAGE + file_path, settings.FILE_STORAGE + same_file.file_path):
                    os.remove(settings.FILE_STORAGE + file_path)
                    self.response_dict['file_id'] = same_file.id
                    return self.error(f'Same file is already exists')

        # Get more data to save object
        if 'file_name' in self.request.GET.keys() and self.request.GET['file_name']:
            file_name = self.request.GET['file_name']
        file_size = os.path.getsize(settings.FILE_STORAGE + file_path)

        new_file = file.File.objects.create(name=file_name, extension=file_extension, size=file_size,
                                            user_uploader=self.request.user, file_path=file_path,
                                            group=self.dict['group'], checksum_md5=checksum_md5)

        self.response_dict['file_id'] = new_file.id
        return self

    def chain_post(self: base_view.BaseView):
        self.authorize() \
            .request_handlers['POST']['specific'](self)

    def handle_get(self: base_view.BaseView) -> Optional[base_view.BaseView]:
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

        file_object = open(settings.FILE_STORAGE + self.dict['file'].file_path, 'rb')

        file_data = file_object.read()
        file_object.close()
        self.dict['response'] = HttpResponse(file_data, content_type='application/file; charset=utf-8')

        #################
        # wsgi.headers.Headers.__bytes__ was manually edited from 'iso-8859-1' to 'utf-8',
        # so it would be encoded on base64
        # (may cause error on client side http-library if it decodes response headers in 'latin-1')
        #################

        # noinspection PyProtectedMember
        self.dict['response']._headers['content-disposition'] = (
            'Content-Disposition', f'attachment; filename="{self.dict["file"].file_path}"')

        # by default need to use this (but header may be in base64, that browser do not handle):
        # self.dict['response']['Content-Disposition'] = f'attachment; filename="{self.dict["file"].file_path}"'
        return self

    def chain_get(self: base_view.BaseView):
        self.authorize() \
            .require_url_parameters(['file_id']) \
            .get_model_by_id(file.File, self.request.GET['file_id']) \
            .request_handlers['GET']['specific'](self)

    def handle_delete(self: base_view.BaseView) -> Optional[base_view.BaseView]:
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

        self.dict['file'].delete()
        return self

    def chain_delete(self: base_view.BaseView):
        self.authorize() \
            .require_url_parameters(['file_id']) \
            .get_model_by_id(file.File, self.request.GET['file_id']) \
            .request_handlers['DELETE']['specific'](self)

    request_handlers = {
        'POST': {
            'chain': chain_post,
            'specific': handle_post
        },
        'GET': {
            'chain': chain_get,
            'specific': handle_get
        },
        'DELETE': {
            'chain': chain_delete,
            'specific': handle_delete
        }
    }
