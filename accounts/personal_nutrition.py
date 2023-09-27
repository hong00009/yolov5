# 게시물에서 검출된 음식객체 수만큼 UserFoodNutritions 영양정보를 DB에 저장하는 함수
# BMI등 건강관련 수치 계산 함수
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from .models import UserFoodNutritions, UserProfile
from yolov5_django.models import Post, FoodNutrition
from datetime import datetime


def save_personal_food_nutrition(user, detected_foods):
    post = Post.objects.filter(user=user).order_by('-post_time').first()

    if detected_foods is not None:
        food_list = [int(index) for index in detected_foods.split(",")]

        for each_food in food_list:
            each_food_nutris = FoodNutrition.objects.get(class_index=each_food)

            nutrition_info = UserFoodNutritions(
                user = user,
                post = post,

                nutrition_info = each_food_nutris,
                
                datetime=post.post_time

            )
            nutrition_info.save()

def bmi_calculator(user):
    user_profile = user.userprofile

    height = user_profile.height / 100  
    weight = user_profile.weight
    gender = user_profile.gender

    # 표준 체중 계산
    if gender == '남성':
        standard_weight = round(height * height * 22, 1)
    else:
        standard_weight = round(height * height * 21, 1)

    # BMI 계산
    bmi = round(weight / (height * height), 1)

    # 나이계산
    birthdate = user.userprofile.birthdate
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    daily_kcal = 0
    meal_kcal = 0

    if age < 30: 
        if gender == '':
            daily_kcal = 2600
            meal_kcal = 870
        elif gender == 'female':
            daily_kcal = 2100
            meal_kcal = 700
    elif 30 <= age < 40:
        print('30대')
        if gender == 'male':
            daily_kcal = 2500
            meal_kcal = 820
        elif gender == 'female':
            daily_kcal = 2000
            meal_kcal = 670
            print(gender)
    elif 40<= age < 50:
        print('40대')
        if gender == 'male':
            daily_kcal = 2400
            meal_kcal = 780
        elif gender == 'female':
            daily_kcal = 1900
            meal_kcal = 630
    elif 50 <= age < 60:
        if gender == 'male':
            daily_kcal = 2200
            meal_kcal = 730
        elif gender == 'female':
            daily_kcal = 1800
            meal_kcal = 600
    else:
        if gender == 'male':
            daily_kcal = 2000
            meal_kcal = 650
        elif gender == 'female':
            daily_kcal = 1600
            meal_kcal = 530

    context = {
        'bmi' : bmi,
        'standard_weight': standard_weight,
        'daily_kcal': daily_kcal,
        'meal_kcal': meal_kcal,

    }
    return bmi, standard_weight, daily_kcal, meal_kcal


# 10~20대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,600kcal
# 한 끼 권장 칼로리 : 870kcal
# 30대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,500kcal
# 한 끼 권장칼로리 : 820kcal
# 40대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,400kcal
# 한 끼 권장칼로리 : 780kcal
# 50대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,200kcal
# 한 끼 권장 칼로리 : 730kcal
# 60대 이상 남자 권장 칼로리
# 하루 권장칼로리 : 2,000kcal
# 한 끼 권장 칼로리 : 650kcal


# 10~20대 여자 권장 칼로리
# 하루 권장 칼로리 : 2,100kcal
# 한 끼 권장 칼로리 : 700kcal
# 30대 여자 권장 칼로리
# 하루 권장 칼로리 : 2,000kcal
# 한 끼 권장 칼로리 : 670kcal
# 40대 여자 권장 칼로리
# 하루 권장칼로리 : 1,900kcal
# 한 끼 권장 칼로리 : 630kcal
# 50대 여자 권장 칼로리
# 하루 권장칼로리 : 1,800kcal
# 한끼 권장칼로리 : 600kcal
# 60대 여자 권장 칼로리
# 하루 권장 칼로리 : 1,600kcal
# 한 끼 권장칼로리 : 530kcal