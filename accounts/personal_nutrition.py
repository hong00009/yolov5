# 게시물에서 검출된 음식객체 수만큼 UserFoodNutritions 영양정보를 DB에 저장하는 함수

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserFoodNutritions
from yolov5_django.models import Post, FoodNutrition
from datetime import datetime

def save_personal_food_nutrition(user, detected_foods):
    post = Post.objects.filter(user=user).order_by('-year', '-month', '-day', '-hour').first()

    if detected_foods is not None:
        food_list = [int(index) for index in detected_foods.split(",")]

        for each_food in food_list:
            each_food_nutris = FoodNutrition.objects.get(class_index=each_food)

            nutrition_info = UserFoodNutritions(
                user = user,
                post = post,

                nutrition_info = each_food_nutris,
                
                datetime=datetime(
                    year=post.year,
                    month=post.month,
                    day=post.day,
                    hour=post.hour,)
            )
            nutrition_info.save()
