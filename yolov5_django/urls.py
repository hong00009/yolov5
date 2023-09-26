from django.urls import path, include
from yolov5_django import views, chart

app_name = 'yolov5_django'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_post, name='upload_post'),
    path('my_page/', views.my_page, name='my_page'),

    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/', views.detail_post, name='detail_post'),

    path('chart/', chart.chart, name='chart'),
    
]