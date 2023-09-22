from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodNutrition
import json
def chart(request):
    # all_nutris = FoodNutrition.objects.all()

    # 클래스_인덱스 2번 => 콩밥
    one_food_data = FoodNutrition.objects.filter(class_index=2).first() 

    field_names = [field.name for field in FoodNutrition._meta.fields] 

    # 음식g, 열량 등..
    nutri_labels = field_names[5:]  

    one_food_data_dict = {}
    for field in one_food_data._meta.fields:
        field_name = field.name
        field_value = getattr(one_food_data, field_name)
        one_food_data_dict[field_name] = field_value
    

    # 필요한 데이터를 JSON 형식으로 변환
    one_food_data_json = json.dumps(one_food_data_dict)
    print(one_food_data_json)

    context = {
        # 'all_nutris' : all_nutris,
        # 'one_food_data': one_food_data,
        'nutri_labels' : nutri_labels,
        'one_food_data_json':one_food_data_json,
    }
    return render(request, 'yolov5_django/chart.html', context)