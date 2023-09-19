from django.shortcuts import render, redirect
from .forms import UploadImageForm
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
            return redirect('yolov5_django:image_list')  # 이미지 목록 페이지로 리디렉션
    else:
        form = UploadImageForm()
    return render(request, 'yolov5_django/upload_image.html', {'form': form})

@login_required
def image_list(request):
    images = UploadedImage.objects.filter(user=request.user)
    return render(request, 'yolov5_django/image_list.html', {'images': images})

