from django.urls import path, include
from yolov5_django import views 

urlpatterns = [
    path('', views.index, name='index'),
]
