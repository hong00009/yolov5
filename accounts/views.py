from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

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
            return redirect('yolov5_django:index')
        
    else:
        form = CustomAuthenticationForm()

    context = {
        'form' : form,
    }

    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('yolov5_django:index')


# BMI 계산
def calculate_bmi(height, weight):
    # 키를 미터로 변환
    height_in_meters = height / 100.0
    
    # BMI 계산 (체중(kg) / (키(m) * 키(m)))
    bmi = weight / (height_in_meters * height_in_meters)
    
    return bmi

from django.shortcuts import get_object_or_404

@login_required
def profile(request):
    user = request.user

    # 사용자에 대한 프로필이 있는지 확인
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # 프로필이 없는 경우 새로운 프로필 생성
        profile = UserProfile(user=user)

    # 프로필 업데이트
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            
            # profile.bmi = profile.calculate_bmi()
            profile.save()
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        # 'bmi': profile.calculate_bmi(),
    }

    return render(request, 'accounts/profile.html', context)