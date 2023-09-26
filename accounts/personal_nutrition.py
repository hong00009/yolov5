# 게시물에서 검출된 음식객체 수만큼 UserFoodNutritions 영양정보를 DB에 저장하는 함수

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserFoodNutritions, UserProfile
from yolov5_django.models import Post, FoodNutrition
from datetime import date

def save_personal_food_nutrition(user, detected_foods):
    post = Post.objects.filter(user=user).order_by('-uploaded_at').first()

    if detected_foods is not None:
        food_list = [int(index) for index in detected_foods.split(",")]

        for each_food in food_list:
            each_food_nutris = FoodNutrition.objects.get(class_index=each_food)

            nutrition_info = UserFoodNutritions(
                user = user,
                post = post,

                nutrition_info = each_food_nutris,
                
                datetime=post.uploaded_at
            )
            nutrition_info.save()

def bmi_calculator(user):
    user_profile = user.userprofile

    height = user_profile.height / 100  
    weight = user_profile.weight
    gender = user_profile.gender

    # 표준 체중 계산
    if gender is '남성':
        standard_weight = height * height * 22
    else:
        standard_weight = height * height * 21

    # BMI 계산
    bmi = weight / (height * height)

    return standard_weight, bmi

def recommendKcal(user):
    user_profile = user.userprofile

    # 나이계산
    birthdate = user_profile.birthdate
    gender = user_profile.gender

    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age >= 10 and age <= 20:
        if gender == '남자':
            daily_kcal = 2600
            meal_kcal = 870
        elif gender == '여자':
            daily_kcal = 2100
            meal_kcal = 700
    elif age >= 30 and age < 40:
        if gender == '남자':
            daily_kcal = 2500
            meal_kcal = 820
        elif gender == '여자':
            daily_kcal = 2000
            meal_kcal = 670
    elif age >= 40 and age < 50:
        if gender == '남자':
            daily_kcal = 2400
            meal_kcal = 780
        elif gender == '여자':
            daily_kcal = 1900
            meal_kcal = 630
    elif age >= 50 and age < 60:
        if gender == '남자':
            daily_kcal = 2200
            meal_kcal = 730
        elif gender == '여자':
            daily_kcal = 1800
            meal_kcal = 600
    else:
        # 60대 이상
        if gender == '남자':
            daily_kcal = 2000
            meal_kcal = 650
        elif gender == '여자':
            daily_kcal = 1600
            meal_kcal = 530

    return daily_kcal, meal_kcal




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