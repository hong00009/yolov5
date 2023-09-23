from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodNutrition
import json

def chart(class_indexes):
    # 각 class_index에 해당하는 음식의 영양 정보 가져오기
    food_data_list = FoodNutrition.objects.filter(class_index__in=class_indexes)

    total_nutrition = {
        'carbohydrate': 0,
        'protein': 0,
        'fat': 0,
    }

    for food_data in food_data_list:
        total_nutrition['carbohydrate'] += getattr(food_data, 'carbohydrate')
        total_nutrition['protein'] += getattr(food_data, 'protein')
        total_nutrition['fat'] += getattr(food_data, 'fat')

    # 필요한 데이터를 JSON 형식으로 변환
    total_nutrition_json = json.dumps(total_nutrition)

    return total_nutrition_json


# 한가지 음식 차트 테스트
# def chart(class_idx):
#     all_nutris = FoodNutrition.objects.all()

#     # 클래스_인덱스 2번 => 콩밥
#     one_food_data = FoodNutrition.objects.filter(class_index=class_idx).first() 

#     field_names = [field.name for field in FoodNutrition._meta.fields] 
#     print('field_names', field_names,'\n')

#     one_food_data_dict = {}
#     for field in one_food_data._meta.fields:
#         field_name = field.name
#         field_value = getattr(one_food_data, field_name)
#         one_food_data_dict[field_name] = field_value
    
#     one_food_data_json = json.dumps(one_food_data_dict)

#     return one_food_data_json