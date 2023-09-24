from django.shortcuts import render, redirect, get_object_or_404
from .models import UserFoodNutritions
from yolov5_django.models import UploadedImage, FoodNutrition

def save_personal_food_nutrition(user, detected_foods):
    post = UploadedImage.objects.filter(user=user).order_by('-uploaded_at').first()

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
