import tarfile

from django.http import HttpResponse

from metaApp.utils.RaisingErrors import RaisingErrors


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


def get_request_to_download_tar(file_paths):
    tar_name = 'perfectFiles.tar'
    tar_obj = tarfile.open(tar_name, 'w')

    for file_path in file_paths:
        print('loading path: ', file_path)
        tar_obj.add(file_path)

    tar_obj.close()

    with open(tar_name, 'rb') as f:
        tar_data = f.read()

    response = HttpResponse(tar_data, content_type='application/x-tar')
    response['Content-Disposition'] = 'attachment; filename="' + 'perfectFiles.tar' + '"'

    f.close()

    return response
