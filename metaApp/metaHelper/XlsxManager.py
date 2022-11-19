import json

import openpyxl as openpyxl

from metaApp.metaHelper.FileManager import FileManager


class XlsxManager(FileManager):
    attributes = [
        "contentStatus",
        "lastPrinted",
        "revision",
        "version",
        "creator",
        "lastModifiedBy",
        "modified",
        "created",
        "title",
        "subject",
        "description",
        "identifier",
        "language",
        "keywords",
        "category",
    ]

    def get_all_metadata(self):
        fh = openpyxl.load_workbook(self.dir_to_file)
        obj = fh.properties
        metadata = {}
        for item in self.attributes:
            metadata[item] = str(getattr(obj, item))
        print(metadata)
        return metadata

    def set_property(self, key, value):
        fh = openpyxl.load_workbook(self.dir_to_file)
        obj = fh.properties
        setattr(fh.properties, key, value)
        fh.save(self.dir_to_file)

    def clear_all_data(self):
        pass

    def get_content_type(self):
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
