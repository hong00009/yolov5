from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg
import calendar
from .models import UserFoodNutritions
from yolov5_django.forms import DateRangeFilterForm

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import UserProfile
from .personal_nutrition import bmi_calculator

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if  form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('yolov5_django:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form' : form
    }

    return render(request, 'accounts/form.html', context)


def login(request):

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('yolov5_django:my_page')
        
    else:
        form = CustomAuthenticationForm()

    context = {
        'form' : form,
    }

    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('yolov5_django:index')


# @login_required
# def profile(request):
#     user = request.user

#     try:
#         # 프로필이 있는지 확인
#         profile = UserProfile.objects.get(user=user)
#         bmi, standard_weight, daily_kcal, meal_kcal = bmi_calculator(user)  
#         ages = profile.age//10*10
#         print('**try', profile)

#     except UserProfile.DoesNotExist:
#         # 프로필이 없으면 None으로 설정
#         profile = bmi = standard_weight = daily_kcal = meal_kcal = ages = None
#         print('**프로필없음', profile)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
        
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = user
#             print('**POST 저장', profile)

#             profile.save()
            
#             # 데이터 저장 후 새롭게 BMI 계산
#             bmi, standard_weight, daily_kcal, meal_kcal = bmi_calculator(user)
#             ages = profile.age//10*10

#     else:
#         form = UserProfileForm(instance=profile)
#         print('**else GET')


#     context = {
#         'user': user,
#         'profile': profile,
#         'form': form,
#         'bmi': bmi,
#         'standard_weight': standard_weight, 
#         'daily_kcal': daily_kcal,
#         'meal_kcal': meal_kcal,
#         'ages': ages,
#     }

#     return render(request, 'accounts/profile.html', context)

@login_required
def profile(request):
    user = request.user
    today = timezone.now().date()

    try:
        # 프로필이 있는지 확인
        profile = UserProfile.objects.get(user=user)
        bmi, standard_weight, daily_kcal, meal_kcal = bmi_calculator(user)
        ages = profile.age // 10 * 10

    except UserProfile.DoesNotExist:
        # 프로필이 없으면 None으로 설정
        profile = bmi = standard_weight = daily_kcal = meal_kcal = ages = None

    # 오늘 기준으로 통계량 계산
    daily_nutrition = UserFoodNutritions.objects.filter(user=user, datetime__date=today).aggregate(
        total_energy=Sum('nutrition_info__energy'),
        total_carbohydrate=Sum('nutrition_info__carbohydrate'),
        total_protein=Sum('nutrition_info__protein'),
        total_fat=Sum('nutrition_info__fat'),
    )

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # 이번 주의 모든 메뉴 합계(AVG를 구하기 위해)
    weekly_nutrition = UserFoodNutritions.objects.filter(
        user=user, datetime__date__range=[start_of_week, end_of_week]
    ).aggregate(
        total_energy=Sum('nutrition_info__energy'),
        total_carbohydrate=Sum('nutrition_info__carbohydrate'),
        total_protein=Sum('nutrition_info__protein'),
        total_fat=Sum('nutrition_info__fat'),
    )

    start_of_month = today.replace(day=1)
    # 현재 날짜로부터 이번 달의 마지막 날짜를 계산
    _, last_day_of_month = calendar.monthrange(today.year, today.month)
    # 이번 달의 마지막 날짜로 설정
    end_of_month = today.replace(day=last_day_of_month)

    # 이번 달의 모든 메뉴 합계(AVG를 구하기 위해)
    monthly_nutrition = UserFoodNutritions.objects.filter(
        user=user, datetime__date__range=[start_of_month, end_of_month]
    ).aggregate(
        total_energy=Sum('nutrition_info__energy'),
        total_carbohydrate=Sum('nutrition_info__carbohydrate'),
        total_protein=Sum('nutrition_info__protein'),
        total_fat=Sum('nutrition_info__fat'),
    )

    # 주간/월간 평균 계산
    num_days_in_week = (end_of_week - start_of_week).days + 1
    num_days_in_month = (end_of_month - start_of_month).days + 1

    # 주간 합계를 기간으로 나누어 하루에 어떤 영양소를 평균적으로 얼마나 섭취하는지 계산
    weekly_nutrition_avg = {
        'avg_energy': weekly_nutrition['total_energy'] / num_days_in_week,
        'avg_carbohydrate': weekly_nutrition['total_carbohydrate'] / num_days_in_week,
        'avg_protein': weekly_nutrition['total_protein'] / num_days_in_week,
        'avg_fat': weekly_nutrition['total_fat'] / num_days_in_week,
    }
    # 월간 합계를 기간으로 나누어 하루에 어떤 영양소를 평균적으로 얼마나 섭취하는지 계산
    monthly_nutrition_avg = {
        'avg_energy': monthly_nutrition['total_energy'] / num_days_in_month,
        'avg_carbohydrate': monthly_nutrition['total_carbohydrate'] / num_days_in_month,
        'avg_protein': monthly_nutrition['total_protein'] / num_days_in_month,
        'avg_fat': monthly_nutrition['total_fat'] / num_days_in_month,
    }

    context = {
        'user': user,
        'profile': profile,
        'bmi': bmi,
        'standard_weight': standard_weight,
        'daily_kcal': daily_kcal,
        'meal_kcal': meal_kcal,
        'ages': ages,
        'daily_nutrition': daily_nutrition,
        'weekly_nutrition': weekly_nutrition_avg,
        'monthly_nutrition': monthly_nutrition_avg,
    }

    return render(request, 'accounts/profile.html', context)