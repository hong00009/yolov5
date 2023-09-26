from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm
from .personal_nutrition import bmi_calculator, recommendKcal

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


@login_required
def profile(request):
    user = request.user

    # 사용자에 대한 프로필이 있는지 확인
    try:
        # 프로필이 있으면 db에서 기존 정보 불러옴
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # 프로필이 없는 경우 새로운 프로필 생성
        profile = UserProfile(user=user)

    # 프로필 업데이트
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=profile)

    standard_weight, bmi_value = bmi_calculator(user)
    daily_kcal, meal_kcal = recommendKcal(user)

    context = {
        'form': form,
        'profile': profile,
        'standard_weight': standard_weight,
        'bmi_value': bmi_value,
        'daily_kcal': daily_kcal,
        'meal_kcal': meal_kcal,
    }

    return render(request, 'accounts/profile.html', context)