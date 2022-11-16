import json
import glob
import os.path
import tarfile

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from rest_framework.views import APIView

from metaApp.utils.forms import FileFieldForm
from .utils.DownloadManager import get_request_to_download_tar, get_request_to_download_file
from .utils.IdentifyRequest import IdentifyRequest, server_tokens
from .utils.RaisingErrors import RaisingErrors
from .utils.UploadedFilehHandler import UploadedFiLeHandler, get_file_manager


def hello(request):
    return HttpResponse(json.dumps('{potdata:4321}'), content_type="application/json")


class UploadFileFromForm(FormView):
    form_class = FileFieldForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileFromForm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('file_field')
            identify_request_token = IdentifyRequest()
            list_managers = []
            if len(files) != 0:
                for file in files:
                    list_managers.append(get_file_manager(identify_request_token.request_folder_dir + '/' + str(file)))
                    UploadedFiLeHandler.upload_file(file=file, token=identify_request_token)

            list_metadata = []
            for item in list_managers:
                list_metadata.append(item.get_all_metadata())

            response_dict = {'token': identify_request_token.token, 'file_data': list_metadata}
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except ValueError as error:
            return JsonResponse({'message': str(error.args[0])}, status=error.args[1])


class ChangeFile(APIView):

    def put(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        token = body_data['token']
        file_name = body_data['file_name']
        list_changing_params = body_data['changing_params']

        for server_token in server_tokens:
            if server_token.token == token:

                file_path = server_token.request_folder_dir + '/' + file_name

                if os.path.isfile(file_path):
                    file_manager = get_file_manager(file_path)
                    for item in list_changing_params:
                        param = item['param']
                        new_value = item['value']
                        file_manager.set_property(key=param, value=new_value)
                        return JsonResponse({'message': 'OK'}, status=200)
                else:
                    return JsonResponse({'message': 'No such file'}, status=400)
                break
        else:
            return JsonResponse({'message': 'No such token'}, status=400)
        return HttpResponse(json.dumps('{post_data:4321}'), content_type="application/json")


class DownloadFile(APIView):

    def get(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        token = body_data['token']
        file_name = body_data['file_name']
        print()
        try:
            for server_token in server_tokens:
                if server_token.token == token:
                    file_path = server_token.request_folder_dir + '/' + file_name
                    if os.path.isfile(file_path):

                        file_manager = get_file_manager(file_path)
                        response = get_request_to_download_file(file_path=file_path, file_manager=file_manager)
                        server_token.expire_token()

                        return response
                    else:
                        raise RaisingErrors.no_such_file
                    break
            else:
                raise RaisingErrors.no_such_token
        except ValueError as error:
            return JsonResponse({'message': str(error.args[0])}, status=error.args[1])


class DownloadAllFiles(APIView):

    def get(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        token = body_data['token']
        try:
            for server_token in server_tokens:
                if server_token.token == token:
                    file_paths = glob.glob(server_token.request_folder_dir + '/*')

                    if len(file_paths) == 0:
                        raise RaisingErrors.no_files_to_download

                    response = get_request_to_download_tar(file_paths)
                    server_token.expire_token()

                    return response
            else:
                raise RaisingErrors.no_such_token
        except ValueError as error:
            return JsonResponse({'message': str(error.args[0])}, status=error.args[1])
