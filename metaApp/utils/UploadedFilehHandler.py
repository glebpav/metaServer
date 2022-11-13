class UploadedFiLeHandler:

    @staticmethod
    def upload_file(file, token):
        file_name = token.request_folder_dir + '/' + str(file)
        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
