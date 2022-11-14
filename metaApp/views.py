import json
import os.path

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from rest_framework.request import Request
from rest_framework.views import APIView

from metaApp.utils.forms import FileFieldForm
from .utils.IdentifyRequest import IdentifyRequest, server_tokens
from .utils.RaisingErrors import RaisingErrors
from .utils.UploadedFilehHandler import UploadedFiLeHandler, get_file_manager, get_request_to_download_file


def hello(request):
    return HttpResponse(json.dumps('{potdata:4321}'), content_type="application/json")


class UploadFileFromForm(FormView):
    form_class = FileFieldForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileFromForm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            form_class = self.get_form_class()
            # form = self.get_form(form_class)
            files = request.FILES.getlist('file_field')
            print("My files: ", files)
            identify_request_token = IdentifyRequest()
            list_managers = []
            if len(files) != 0:
                for file in files:
                    list_managers.append(get_file_manager(identify_request_token.request_folder_dir + '/' + str(file)))
                    UploadedFiLeHandler.upload_file(file=file, token=identify_request_token)
                    print(identify_request_token.request_folder_dir + '/' + str(file))

            list_metadata = []
            for item in list_managers:
                list_metadata.append(item.get_all_metadata())

            print(list_metadata)
            response_dict = {'token': identify_request_token.token, 'file_data': list_metadata}
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except ValueError as error:
            return JsonResponse({'message': str(error.args[0])}, status=error.args[1])


class ChangeFile(APIView):

    def get(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        token = body_data['token']
        file_name = body_data['file_name']

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
