from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadImageForm, EditImageForm
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
from .models import FoodNutrition
<<<<<<< HEAD
from uuid import uuid4 # 고유번호 생성
from . import yolo_detect

from PIL import Image
from django.conf import settings

import os
from django.core.files.storage import FileSystemStorage
=======
>>>>>>> 98000a749257ad6bf1db3d08463dea0e11dfd2d4
from datetime import datetime 
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
            return redirect('yolov5_django:detail_image', image_id=image.id)
    else:
        form = UploadImageForm()
    context = {
        'form': form,
    }
    return render(request, 'yolov5_django/upload_image.html', context)

@login_required
def image_list(request):
    images = UploadedImage.objects.filter(user=request.user)

    context = {
        'images': images,
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
    context = {
        'image': image,
    }
    return render(request, 'yolov5_django/detail_image.html', context)


def chart(request):
    nutris = FoodNutrition.objects.all()

    context = {
        'nutris' : nutris,
    }
    return render(request, 'yolov5_django/chart.html', context)


# 실습 코드 그대로 가져옴 / 수정필요
def rename_imagefile_to_uuid(filename): # 고유번호로 이미지파일명 변경
    ext = filename.split('.')[-1] # 파일 이름에서 확장자만 분리
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid,ext)

    return filename


def detect(request):
    img = request.FILES.get('images') # 사용자가 전송한 이미지 파일 가져오기
    fs = FileSystemStorage() # 파일 저장소 접근 객체 생성

    # 전송된 파일명 변경해서 저장
    # 서버에서 사용할 유일한 파일면 생성
    file_name = rename_imagefile_to_uuid(img.name)
    img_up_url = fs.save(file_name, img) # media 디렉터리에 저장

    img_path = os.path.join(settings.MEDIA_ROOT, img_up_url)
    img_url = fs.url(img_up_url)

    # 이미지 객체 검출 함수 호출 yolov5_detect.py
    res_url = yolo_detect.y_detect(img_path, img_up_url)

    # 원본 이미지와 검출된 이미지를 로드합니다.
    original_image = Image.open(img_path)
    detected_image = Image.open(os.path.join(settings.MEDIA_ROOT, res_url))

    context = {
        'original_image': original_image,
        'detected_image': detected_image,
    }

    return render(request, 'detect/result.html', context)





