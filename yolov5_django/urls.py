from django.urls import path, include
from yolov5_django import views, yolo_detect, chart

app_name = 'yolov5_django'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_image, name='upload_image'),
    path('image_list/', views.image_list, name='image_list'),  # 이미지 목록 페이지 URL

    path('edit_image/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('image/<int:image_id>/', views.detail_image, name='detail_image'),

    path('chart/', chart.chart, name='chart'),
]