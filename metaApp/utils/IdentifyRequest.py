import os
from uuid import uuid4


def make_new_dir(new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def delete_dir(path_to_dir):
    os.rmdir(path_to_dir)


server_tokens = []
print('initialize tokens')


class IdentifyRequest:

    def __init__(self):
        self.token = self.__get_token()
        self.request_folder_dir = 'loadedFiles/' + str(self.token)
        make_new_dir(self.request_folder_dir)
        server_tokens.append(self)

    @staticmethod
    def __get_token():
        request_token = uuid4()
        return str(request_token)

    def expire_token(self):
        delete_dir(self.request_folder_dir)
