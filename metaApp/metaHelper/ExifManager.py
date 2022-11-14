import os

from exif import Image

from metaApp.metaHelper.FileManager import FileManager


class ExifManager(FileManager):

    def get_content_type(self):
        filename, file_extension = os.path.splitext(self.dir_to_file)
        file_extension = str(file_extension).lower().replace('.', '')
        content_type = 'image/'
        if file_extension == 'gif':
            content_type += 'gif'
        elif file_extension == 'jpeg':
            content_type += 'jpeg'
        elif file_extension == 'jpg':
            content_type += 'jpg'
        elif file_extension == 'svg':
            content_type += 'svg+xml'
        elif file_extension == 'tiff':
            content_type += 'tiff'
        elif file_extension == 'ico':
            content_type += 'vnd.microsoft.icon'
        elif file_extension == 'wbmp':
            content_type += 'wbmp'
        elif file_extension == 'webp':
            content_type += 'webp'
        else:
            raise ValueError('No such content type 1', 400)
        return content_type

    def clear_all_data(self):
        with open(self.dir_to_file, 'rb') as img_file:
            img = Image(img_file)
        img.delete_all()
        with open(self.dir_to_file, 'wb') as new_image_file:
            new_image_file.write(img.get_file())

    def get_all_metadata(self):
        with open(self.dir_to_file, 'rb') as img_file:
            img = Image(img_file)
        metadata = {}
        if img.has_exif:
            for item in img.list_all():
                if item == 'flash':
                    continue
                metadata[item] = img.get(item)
            return metadata
        else:
            return {}

    def set_property(self, key, value):
        with open(self.dir_to_file, 'rb') as img_file:
            img = Image(img_file)
        if img.has_exif:
            img[key] = value
            with open(self.dir_to_file, 'wb') as new_image_file:
                new_image_file.write(img.get_file())
