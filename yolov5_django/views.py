from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.core.paginator import Paginator
import logging
from django.db.models.functions import ExtractWeek
from uuid import uuid4 # 고유번호 생성
from datetime import timedelta
import os
# ▲ 기본 라이브러리만

# ▼ 자체 제작
from .forms import PostForm, EditPostForm, DateRangeFilterForm
from .yolo_detect import y_detect
from .foodinfo import food_info
from .models import Post
from accounts.personal_nutrition import save_personal_food_nutrition
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('yolov5_django:my_page')
    else:
        return render(request, 'yolov5_django/index.html')


@login_required
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            # 파일 저장시 이름에 uuid hex적용
            image = request.FILES['image']
            ext = image.name.split('.')[-1]
            uuid = uuid4().hex
            filename = '{}.{}'.format(uuid, ext)
            post.image.name = filename

            post.save() # 사진먼저저장

            detected_foods = y_detect(post.image.path) # 저장된사진으로 탐지

            post.detection_result = detected_foods
            post.save()  # 탐지결과 추가 저장

            save_personal_food_nutrition(request.user, post, detected_foods)  # 개인 영양정보 저장

            return redirect('yolov5_django:detail_post', post_id=post.id)
        if not form.is_valid():
            print(form.errors)
            print(form['title'].errors)
    else:
        form = PostForm()
        logger.error("%s", form.errors)
        
    
    context = {'form': form}
    return render(request, 'yolov5_django/upload_post.html', context)


@login_required
def my_page(request):
    form = DateRangeFilterForm(request.GET)
    
    posts = Post.objects.filter(user=request.user).order_by('-post_time')

    postw = Post.objects.annotate(week=ExtractWeek('post_time')).order_by('week')
    total_posts = Post.objects.filter(user=request.user).count()

    filter_O = False

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if start_date:
            posts = posts.filter(post_time__gte=start_date)
            filter_O = True

        if end_date:
            end_date += timedelta(days=1)
            end_date -= timedelta(seconds=1)
            posts = posts.filter(post_time__lte=end_date)
            filter_O = True

    filtered_posts = posts.count()

    # 페이지 설정
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'form': form,
        'postw': postw,
        'filter_O': filter_O,
        'total_posts_count': total_posts,
        'filtered_posts_count' : filtered_posts,
    }
    return render(request, 'yolov5_django/my_page.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect('yolov5_django:detail_post', post_id=post.id)
    else:
        form = EditPostForm(instance=post)
        logger.error("%s", form.errors)

    context = {
        'form': form, 
        'post': post,
        'hours':range(24),
    }
    return render(request, 'yolov5_django/edit_post.html', context)


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)

    file_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
    if os.path.exists(file_path):
        os.remove(file_path)

    post.delete()

    return redirect('yolov5_django:my_page')


@login_required
def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    print('**', post.user,'의 detection_result:', post.detection_result)
    
    food_name_list, nutrition_info_list, total_chart_info_json, each_chart_info_json, percentage = food_info(post)

    context = {
        'post': post,

        'food_idx_list': post.detection_result,
        'food_name_list': food_name_list,
        'nutrition_info_list':nutrition_info_list,
        'total_chart_info_json': total_chart_info_json,
        'each_chart_info_json':each_chart_info_json,
        'percentage': percentage,
    }
    
    return render(request, 'yolov5_django/post.html', context)