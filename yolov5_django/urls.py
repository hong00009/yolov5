from django.urls import path, include
from yolov5_django import views 

app_name = 'yolov5_django'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload_image'),
    path('image_list/', views.image_list, name='image_list'),  # 이미지 목록 페이지 URL
]