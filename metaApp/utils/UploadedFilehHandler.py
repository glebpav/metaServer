import os

from metaApp.metaHelper.ExifManager import ExifManager


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
    elif file_extension in []:
        pass
    elif file_extension in []:
        pass
    elif file_extension in []:
        pass
