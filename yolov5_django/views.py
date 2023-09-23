from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadImageForm, EditImageForm, DateRangeFilterForm
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
from .models import FoodNutrition
from uuid import uuid4 # 고유번호 생성
from . import yolo_detect

from PIL import Image
from django.conf import settings

import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta

import json
from .chart import chart

# Create your views here.

def index(request):
    return render(request, 'yolov5_django/index.html')

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user  # 현재 로그인한 사용자 설정
            image.uploaded_at = datetime.now() # 현재 날짜와 시간 저장
            image.save()
            image.detection_result = yolo_detect.y_detect(image.image.path)
            image.save()
            

            return redirect('yolov5_django:detail_image', image_id=image.id)
    else:
        form = UploadImageForm()
    context = {
        'form': form,
    }
    return render(request, 'yolov5_django/upload_image.html', context)

@login_required
def image_list(request):
    form = DateRangeFilterForm(request.GET)
    images = UploadedImage.objects.filter(user=request.user)

    # 사용자가 날짜 범위를 선택한 경우
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # 이미지를 선택한 날짜 범위로 필터링합니다.
        if start_date:
            images = images.filter(uploaded_at__gte=start_date)
        if end_date:
            # end_date를 다음날의 0시 0분 0초로 설정하여 1초 전까지 조회합니다.
            end_date += timedelta(days=1)  # 다음날로 이동
            end_date -= timedelta(seconds=1)  # 1초 전까지 조회
            images = images.filter(uploaded_at__lte=end_date)
    
    context = {
        'images': images,
        'form': form,
    }
    return render(request, 'yolov5_django/image_list.html', context)


@login_required
def edit_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id, user=request.user)

    if request.method == 'POST':
        # 이미지 수정 로직을 추가 (예: 폼 처리)
        form = EditImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            # 새로운 제목과 이미지 파일을 업데이트
            form.save()

            # 수정이 완료되면 이미지 목록 페이지로 리디렉션
            return redirect('yolov5_django:image_list')
    else:
        form = EditImageForm(instance=image)
    context = {
        'form': form, 
        'image': image,
    }
    return render(request, 'yolov5_django/edit_image.html', context)


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id, user=request.user)

    if request.method == 'POST':
        # 이미지 삭제 로직을 추가
        image.delete()

        # 삭제가 완료되면 이미지 목록 페이지로 리디렉션
        return redirect('yolov5_django:image_list')
    context = {
        'image': image,
    }

    return render(request, 'yolov5_django/delete_image.html', context)


@login_required
def detail_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id)

    detected_classes = []
    if image.detection_result:
        detected_classes = [int(x) for x in image.detection_result.split(',')]
        
    food_names = []
    
    for class_index in detected_classes:
        try:
            food_item = FoodNutrition.objects.get(class_index=class_index)
            food_names.append(food_item.food_name)
        except FoodNutrition.DoesNotExist:
            food_names.append("알수없음")

    print('이미지:',image.detection_result)

    print('결과:',image.detection_result)

    detection_result_str= ','.join(food_names)

    context = {
        'image': image,
        'detection_result_int': image.detection_result,
        'detection_result_str': detection_result_str,
        'total_nutrition_json': chart(detected_classes),
    }

    return render(request, 'yolov5_django/detail_image.html', context)

