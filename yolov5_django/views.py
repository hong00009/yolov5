from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadImageForm, EditImageForm, DateRangeFilterForm
from .models import UploadedImage, FoodNutrition
from django.contrib.auth.decorators import login_required
from uuid import uuid4 # 고유번호 생성
from datetime import datetime, timedelta

from .yolo_detect import y_detect
from accounts.personal_nutrition import save_personal_food_nutrition
from .chart import chart
import os
from django.conf import settings
# Create your views here.

def index(request):
    return render(request, 'yolov5_django/index.html')

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.uploaded_at = datetime.now()
            image.save() # 사진 먼저 저장

            detected_foods = y_detect(image.image.path) # 저장된 사진으로 detect
            # detected_foods = None 또는 문자열(숫자1개/숫자,숫자 여러개)

            image.detection_result = detected_foods
            image.save() # detect된 결과 추가 저장

            save_personal_food_nutrition(image.user, detected_foods) # 개인 영양 정보 저장

            return redirect('yolov5_django:detail_image', image_id=image.id)
    else:
        form = UploadImageForm()
    context = {
        'form': form,
    }
    return render(request, 'yolov5_django/upload_image.html', context)

@login_required
def my_page(request):
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
    return render(request, 'yolov5_django/my_page.html', context)


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
            return redirect('yolov5_django:my_page')
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

        file_path = os.path.join(settings.MEDIA_ROOT, str(image.image))

        if os.path.exists(file_path):
            os.remove(file_path)

        # 이미지 삭제 로직을 추가
        image.delete()

        # 삭제가 완료되면 이미지 목록 페이지로 리디렉션
        return redirect('yolov5_django:my_page')
    context = {
        'image': image,
    }

    return render(request, 'yolov5_django/delete_image.html', context)


@login_required
def detail_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id)

    food_list = []
    food_names = []
    if image.detection_result:
        food_list = [int(x) for x in image.detection_result.split(',')]
        
        for class_idx in food_list:
            each_food = FoodNutrition.objects.get(class_index=class_idx)
            food_names.append(each_food.food_name)
    else:
        food_names.append('')

    food_name_list = ','.join(food_names)

    context = {
        'image': image,
        'food_idx_list': image.detection_result,
        'food_name_list': food_name_list,
        'chart_info_json': chart(food_list),
    }

    return render(request, 'yolov5_django/detail_image.html', context)