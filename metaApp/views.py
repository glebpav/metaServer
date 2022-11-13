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
from .utils.UploadedFilehHandler import UploadedFiLeHandler, get_file_manager


def hello(request):
    return HttpResponse(json.dumps('{potdata:4321}'), content_type="application/json")


class UploadFileFromForm(FormView):
    form_class = FileFieldForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadFileFromForm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        # form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        print("My files: ", files)
        identify_request_token = IdentifyRequest()
        list_managers = []
        if len(files) != 0:
            for file in files:
                UploadedFiLeHandler.upload_file(file=file, token=identify_request_token)
                print(identify_request_token.request_folder_dir + '/' + str(file))
                list_managers.append(get_file_manager(identify_request_token.request_folder_dir + '/' + str(file)))

        list_metadata = []
        for item in list_managers:
            list_metadata.append(item.get_all_metadata())

        print(list_metadata)
        response_dict = {'token': identify_request_token.token, 'file_data': list_metadata}
        return HttpResponse(json.dumps(response_dict), content_type="application/json")


class ChangeFile(APIView):

    def get(self, request):

        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        token = body_data['token']
        file_name = body_data['file_name']

        for server_token in server_tokens:
            if server_token.token == token:
                file_path = server_token.request_folder_dir + '/' + file_name
                if os.path.isfile(file_path):
                    file_manager = get_file_manager(file_path)

                    with open(file_path, 'rb') as f:
                        file_data = f.read()

                    response = HttpResponse(file_data, content_type=file_manager.get_content_type())
                    response['Content-Disposition'] = 'attachment; filename="' + file_path + '"'

                    return response
                else:
                    return JsonResponse({'message': 'No such file'}, status=400)
                break
        else:
            return JsonResponse({'message': 'No such token'}, status=400)

    def put(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        token = body_data['token']
        file_name = body_data['file_name']
        list_changing_params = body_data['changing_params']
        print('list of changing params: ', list_changing_params)
        print('len of tokens: ', len(server_tokens))
        for server_token in server_tokens:
            print('tokens: ', server_token.token)
            if server_token.token == token:
                print(server_token.request_folder_dir)
                print(server_token.request_folder_dir + '/' + file_name)
                file_path = server_token.request_folder_dir + '/' + file_name
                if os.path.isfile(file_path):
                    file_manager = get_file_manager(file_path)
                    for item in list_changing_params:
                        param = item['param']
                        new_value = item['value']
                        print('param: new value <===> ', param, new_value)
                        file_manager.set_property(key=param, value=new_value)
                        return JsonResponse({'message': 'OK'}, status=200)
                else:
                    return JsonResponse({'message': 'No such file'}, status=400)
                break
        else:
            return JsonResponse({'message': 'No such token'}, status=400)
        return HttpResponse(json.dumps('{post_data:4321}'), content_type="application/json")
