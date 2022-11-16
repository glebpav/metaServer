from django.urls import path
from .views import *

urlpatterns = [
    path('', hello),
    path('uploadFile', UploadFileFromForm.as_view(), name='list'),
    path('downloadFile', DownloadFile.as_view()),
    path('downloadAllFiles', DownloadAllFiles.as_view()),
]
