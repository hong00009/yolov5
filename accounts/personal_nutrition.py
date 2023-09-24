from django.shortcuts import render, redirect, get_object_or_404
from .models import UserFoodNutritions
from yolov5_django.models import UploadedImage, FoodNutrition

def save_personal_food_nutrition(user, detected_foods):
    post = UploadedImage.objects.filter(user=user).order_by('-uploaded_at').first()

    energy = carbohydrate = protein = fat = sodium = 0

    if detected_foods is not None:
        food_list = [int(index) for index in detected_foods.split(",")]

        for each_food in food_list:
            each_food_nutris = FoodNutrition.objects.get(class_index=each_food)

            energy += each_food_nutris.energy  
            carbohydrate += each_food_nutris.carbohydrate 
            protein += each_food_nutris.protein 
            fat += each_food_nutris.fat 
            sodium += each_food_nutris.sodium 

    nutrition_info = UserFoodNutritions(
    user=user,
    post=post,
    energy=energy,
    carbohydrate=carbohydrate,
    protein=protein,
    fat=fat,
    sodium=sodium,
    datetime=post.uploaded_at
    )
    nutrition_info.save()