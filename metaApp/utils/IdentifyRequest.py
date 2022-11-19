import os
import shutil
from uuid import uuid4


def delete_file(path_to_file):
    os.remove(path_to_file)


def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def make_new_dir(new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def delete_dir(path_to_dir):
    shutil.rmtree(path_to_dir)


clear_folder('loadedFiles')
server_tokens = []


class IdentifyRequest:

    def __init__(self):
        self.token = self.__get_token()
        self.request_folder_dir = 'loadedFiles/' + str(self.token)
        server_tokens.append(self)

    @staticmethod
    def __get_token():
        request_token = uuid4()
        return str(request_token)

    def expire_token(self):
        delete_dir(self.request_folder_dir)
        server_tokens.remove(self)
