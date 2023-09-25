# 음식에 대한 영양정보를 json형식으로 변환하여 프론트엔드측으로 전달하는 함수
# 탄단지 외 영양소 추가 확장 가능
from .models import FoodNutrition
import json

def chart(nutrition_info_list):

    total_nutrition_3 = {
        'carbohydrate': 0,
        'protein': 0,
        'fat': 0,
    }

    each_nutrition_3 = {}

    for each_food in nutrition_info_list:
        # 개별
        carbohydrate = getattr(each_food, 'carbohydrate')
        protein = getattr(each_food, 'protein')
        fat = getattr(each_food, 'fat')
        
        # 합산
        total_nutrition_3['carbohydrate'] += carbohydrate
        total_nutrition_3['protein'] += protein
        total_nutrition_3['fat'] += fat

        each_nutrition_3[each_food.food_name] = {
            'carbohydrate': carbohydrate,
            'protein': protein,
            'fat': fat,
         }
    print('***total_nutrition_3:',total_nutrition_3)
    print('***each_nutrition_3:',each_nutrition_3)

    # JSON 형식으로 변환
    total_chart_info_json = json.dumps(total_nutrition_3)
    each_chart_info_json = json.dumps(each_nutrition_3)

    return total_chart_info_json, each_chart_info_json