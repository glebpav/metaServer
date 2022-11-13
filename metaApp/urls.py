from django.urls import path
from .views import *

urlpatterns = [
    path('', hello),
    path('uploadFile', UploadFileFromForm.as_view(), name='list'),
    path('changeFile', ChangeFile.as_view())
]
