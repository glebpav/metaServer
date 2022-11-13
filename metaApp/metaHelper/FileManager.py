from abc import ABC, abstractmethod


class FileManager(ABC):

    def __init__(self, path_to_file):
        self.dir_to_file = path_to_file

    @abstractmethod
    def get_all_metadata(self):
        pass

    @abstractmethod
    def set_property(self, key, value):
        pass

    @abstractmethod
    def clear_all_data(self):
        pass

    @abstractmethod
    def get_content_type(self):
        pass
