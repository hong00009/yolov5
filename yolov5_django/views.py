from django.shortcuts import render, redirect
from .forms import UploadImageForm
from .models import UploadedImage
# Create your views here.

def index(request):
    return render(request, 'yolov5_django/index.html')


def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')  # 이미지 목록 페이지로 리디렉션
    else:
        form = UploadImageForm()
    return render(request, 'yolov5_django/upload_image.html', {'form': form})


def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, 'yolov5_django/image_list.html', {'images': images})

