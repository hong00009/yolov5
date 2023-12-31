from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import logging
from uuid import uuid4 # 고유번호 생성
import os
from django.forms import modelformset_factory
from urllib.parse import urlencode
from datetime import datetime, time
from django.utils import timezone
# ▲ 기본 라이브러리만

# ▼ 자체 제작
from .forms import PostForm, EditPostForm, DateRangeFilterForm
from .yolo_detect import y_detect
from .foodinfo import food_info
from .models import Post
from accounts.personal_nutrition import save_personal_food_nutrition
from accounts.forms import UserNutritionsEditForm, AddFoodForm
from accounts.models import UserFoodNutritions
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
            print('업로드 valid 에러',form['title'].errors)
    else:
        form = PostForm()   
    
    context = {'form': form}
    return render(request, 'yolov5_django/upload_post.html', context)


@login_required
def my_page(request):
    form = DateRangeFilterForm(request.GET)
    
    posts = Post.objects.filter(user=request.user).order_by('-post_time')

    total_posts = posts.count()

    filter_O = False

    # 날짜필터폼
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if start_date:
            posts = posts.filter(post_time__gte=start_date)
            filter_O = True

        if end_date:
            # end_date와 23시59분59초를 더함 (그날의 가장 마지막 시간으로 설정) timezone-aware 형식으로 저장
            end_date = timezone.make_aware(datetime.combine(end_date, time.max))
            posts = posts.filter(post_time__lte=end_date)
            filter_O = True

    filtered_posts = posts.count()

    # 페이지 설정
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # 필터적용이후 페이지 넘길때도 필터 지속 적용
    current_params = request.GET.copy()
    base_url = f"/my_page/?{urlencode(current_params)}"

    context = {
        'posts': posts,
        'form': form,
        'filter_O': filter_O,
        'total_posts_count': total_posts,
        'filtered_posts_count' : filtered_posts,
        'base_url':base_url,
    }
    return render(request, 'yolov5_django/my_page.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    Formset = modelformset_factory(UserFoodNutritions, form=UserNutritionsEditForm, extra=0)

    if request.method == 'POST':
        post_form = EditPostForm(request.POST, request.FILES, instance=post)
        add_food_form = AddFoodForm(request.POST)
        formset = Formset(request.POST)

        if post_form.is_valid() : 
            post_form.save()

            if add_food_form.is_valid():
                add_food = UserFoodNutritions(user=request.user,
                                               post=post,
                                               nutrition_info=add_food_form.cleaned_data['add_food'],
                                               datetime=post.post_time)
                add_food.save()
            
            elif formset.is_valid():    
                for form in formset:
                    if form.cleaned_data['delete']:
                        form.instance.delete()

                    else:
                        instance = form.save(commit=False)
                        instance.user = request.user
                        instance.post = post
                        instance.save()
            

            return redirect('yolov5_django:detail_post', post_id=post.id)
    else:
        post_form = EditPostForm(instance=post)

        query_set = UserFoodNutritions.objects.filter(post=post, user=request.user)
        formset = Formset(queryset=query_set)
        add_food_form = AddFoodForm()

    food_name_list, nutrition_info_list, _, _, _ = food_info(post)

    has_nutrition = UserFoodNutritions.objects.filter(post_id=post_id).exists()

    context = {
        'form': post_form,
        'nutrition_edit_form': formset, 
        'add_food_form': add_food_form,

        'post': post,
        'hours': [str(hour) for hour in range(24)],
        'food_name_list':food_name_list,
        'nutrition_info_list':nutrition_info_list,
        'no_food_state': not has_nutrition,
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