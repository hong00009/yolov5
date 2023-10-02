from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

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


@login_required
def profile(request):
    user = request.user

    try:
        # 프로필이 있는지 확인
        profile = UserProfile.objects.get(user=user)
        bmi, standard_weight, daily_kcal, meal_kcal = bmi_calculator(user)  
        ages = profile.age//10*10
        print('**try', profile)

    except UserProfile.DoesNotExist:
        # 프로필이 없으면 None으로 설정
        profile = bmi = standard_weight = daily_kcal = meal_kcal = ages = None
        print('**프로필없음', profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            print('**POST 저장', profile)

            profile.save()
            
            # 데이터 저장 후 새롭게 BMI 계산
            bmi, standard_weight, daily_kcal, meal_kcal = bmi_calculator(user)
            ages = profile.age//10*10

    else:
        form = UserProfileForm(instance=profile)
        print('**else GET')


    context = {
        'user': user,
        'profile': profile,
        'form': form,
        'bmi': bmi,
        'standard_weight': standard_weight, 
        'daily_kcal': daily_kcal,
        'meal_kcal': meal_kcal,
        'ages': ages,
    }

    return render(request, 'accounts/profile.html', context)
