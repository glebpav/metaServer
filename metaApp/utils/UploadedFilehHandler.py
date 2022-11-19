import os

from metaApp.metaHelper.ExifManager import ExifManager
from metaApp.metaHelper.PdfManager import PdfManager
from metaApp.metaHelper.XlsxManager import XlsxManager
from metaApp.utils.IdentifyRequest import make_new_dir
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

    print('sent path: ', path_to_file[0:path_to_file.rfind('/')])

    file_manager = None
    if file_extension in ['png', 'jpg', 'jpeg', 'svg']:
        print('file is exif format')
        file_manager = ExifManager(path_to_file)
    elif file_extension in ['pdf']:
        print('file is pdf format')
        file_manager = PdfManager(path_to_file)
    elif file_extension in ['xlsx']:
        print('file is xlsx format')
        file_manager = XlsxManager(path_to_file)

    if file_manager is None:
        raise RaisingErrors.no_such_file_extension(file_extension=file_extension)
    else:
        make_new_dir(path_to_file[0:path_to_file.rfind('/')])
        return file_manager
