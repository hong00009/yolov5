from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timedelta
import os
# ▲ 기본 라이브러리만

# ▼ 자체 제작
from .forms import PostForm, EditPostForm, DateRangeFilterForm
from .yolo_detect import y_detect
from .foodinfo import food_info
from .models import Post
from accounts.personal_nutrition import save_personal_food_nutrition

# Create your views here.

def index(request):
    return render(request, 'yolov5_django/index.html')

@login_required
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.uploaded_at = datetime.now()
            post.save() # 사진 먼저 저장

            detected_foods = y_detect(post.image.path) # 저장된 사진으로 detect
            # detected_foods = None 또는 문자열(숫자1개/숫자,숫자 여러개)

            post.detection_result = detected_foods
            post.save() # detect된 결과 추가 저장

            save_personal_food_nutrition(post.user, detected_foods) # 개인 영양 정보 저장

            return redirect('yolov5_django:detail_post', post_id=post.id)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'yolov5_django/upload_post.html', context)

@login_required
def my_page(request):
    form = DateRangeFilterForm(request.GET)
    posts = Post.objects.filter(user=request.user)

    # 사용자가 날짜 범위를 선택한 경우
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # 이미지를 선택한 날짜 범위로 필터링합니다.
        if start_date:
            posts = posts.filter(uploaded_at__gte=start_date)
        if end_date:
            # end_date를 다음날의 0시 0분 0초로 설정하여 1초 전까지 조회합니다.
            end_date += timedelta(days=1)  # 다음날로 이동
            end_date -= timedelta(seconds=1)  # 1초 전까지 조회
            posts = posts.filter(uploaded_at__lte=end_date)
    
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'yolov5_django/my_page.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        # 이미지 수정 로직을 추가 (예: 폼 처리)
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # 새로운 제목과 이미지 파일을 업데이트
            form.save()

            # 수정이 완료되면 이미지 목록 페이지로 리디렉션
            return redirect('yolov5_django:my_page')
    else:
        form = EditPostForm(instance=post)
    context = {
        'form': form, 
        'post': post,
    }
    return render(request, 'yolov5_django/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        file_path = os.path.join(settings.MEDIA_ROOT, str(post.image))

        if os.path.exists(file_path):
            os.remove(file_path)
        
        post.delete()

        return redirect('yolov5_django:my_page')
    context = {
        'post': post,
    }

    return render(request, 'yolov5_django/delete_post.html', context)


@login_required
def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    print('**', post.user,'의 detection_result:', post.detection_result)
    
    food_name_list, nutrition_info_list, total_chart_info_json, each_chart_info_json = food_info(post)

    context = {
        'post': post,

        'food_idx_list': post.detection_result,
        'food_name_list': food_name_list,
        'total_chart_info_json': total_chart_info_json,
        'each_chart_info_json':each_chart_info_json,
        'nutrition_info_list':nutrition_info_list,
    }
    
    return render(request, 'yolov5_django/post.html', context)