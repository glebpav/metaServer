from django.urls import path
from .views import *

urlpatterns = [
    path('', hello),
    path('uploadFile', FileFieldFormView.as_view(), name='list'),
]
