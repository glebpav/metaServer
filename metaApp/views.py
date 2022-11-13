import json
from django import forms

from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from .utils.IdentifyRequest import IdentifyRequest
from .utils.UploadedFilehHandler import UploadedFiLeHandler

from metaApp.utils.forms import UploadFileForm, FileFieldForm


def hello(request):
    return HttpResponse(json.dumps('otdata:4321}'), content_type="application/json")


class FileFieldFormView(FormView):
    form_class = FileFieldForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FileFieldFormView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        print("My files: ", files)
        identify_request_token = IdentifyRequest()
        if len(files) != 0:
            for file in files:
                UploadedFiLeHandler.upload_file(file=file, token=identify_request_token)

        return HttpResponse(json.dumps('files: ' + str([str(item) for item in files]).replace("'", "")), content_type="application/json")

    """else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})"""
