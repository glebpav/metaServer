from django.urls import path
from .views import *

urlpatterns = [
    path('', hello),
    path('changeFile', ChangeFile.as_view()),
    path('uploadFile', UploadFileFromForm.as_view(), name='list'),
    path('downloadFile', DownloadFile.as_view()),
    path('downloadAllFiles', DownloadAllFiles.as_view()),
    path('endSession', EndSession.as_view())
]
