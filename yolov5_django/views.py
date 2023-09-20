from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadImageForm, EditImageForm
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
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