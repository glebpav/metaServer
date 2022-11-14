import os

from django.http import HttpResponse

from metaApp.metaHelper.ExifManager import ExifManager
from metaApp.utils.RaisingErrors import RaisingErrors


class UploadedFiLeHandler:

    @staticmethod
    def upload_file(file, token):
        file_name = token.request_folder_dir + '/' + str(file)
        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)


def get_file_manager(path_to_file):
    filename, file_extension = os.path.splitext(path_to_file)
    file_extension = str(file_extension).lower().replace('.', '')

    if file_extension in ['png', 'jpg', 'jpeg', 'svg']:
        print('file is exif format')
        return ExifManager(path_to_file)
    raise RaisingErrors.no_such_file_extension


def get_request_to_download_file(file_path, file_manager):
    with open(file_path, 'rb') as f:
        file_data = f.read()

    content_type = file_manager.get_content_type()

    if content_type is None:
        raise RaisingErrors.no_such_content_type

    response = HttpResponse(file_data, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="' + file_path + '"'

    f.close()

    return response
