class RaisingErrors:
    no_such_file = ValueError('No such file', 400)
    no_such_token = ValueError('No such token', 400)
    no_such_content_type = ValueError('No such content type', 400)
    no_files_to_download = ValueError('No files to download', 400)

    @staticmethod
    def no_such_file_extension(file_extension):
        return ValueError(str(file_extension) + ' file extension is not supporting now', 422)

    @staticmethod
    def no_such_param(param):
        return ValueError('\'' + param + '\' is required in request', 400)
