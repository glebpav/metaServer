import docx

from metaApp.metaHelper.FileManager import FileManager
from metaApp.utils.RaisingErrors import RaisingErrors


class DocsManager(FileManager):

    attributes = [
        'author',
        'category',
        'comments',
        'content_status',
        'created',
        'identifier',
        'keywords',
        'language',
        'last_modified_by',
        'last_printed',
        'modified',
        'revision',
        'subject',
        'title',
        'version'
    ]

    def get_all_metadata(self):
        document = docx.Document(self.dir_to_file)
        core_properties = document.core_properties

        metadata = {}
        for item in self.attributes:
            metadata[item] = str(getattr(core_properties, item))

        return metadata

    def set_property(self, key, value):
        document = docx.Document(self.dir_to_file)
        core_properties = document.core_properties

        if key not in self.attributes:
            RaisingErrors.no_such_attribute(key)

        setattr(core_properties, key, value)
        document.save(self.dir_to_file)

    def clear_all_data(self):
        pass

    def get_content_type(self):
        return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'