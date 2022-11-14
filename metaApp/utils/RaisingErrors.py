
class RaisingErrors:
    no_such_file = ValueError('No such file', 400)
    no_such_token = ValueError('No such token', 400)
    no_such_content_type = ValueError('No such content type', 400)
    no_such_file_extension = ValueError('This file extension is not supporting now', 422)