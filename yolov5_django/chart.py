
from .models import FoodNutrition
import json

def chart(nutrition_info_list):

    total_nutrition_3 = {
        'carbohydrate': 0,
        'protein': 0,
        'fat': 0,
    }

    for each_food in nutrition_info_list:
        total_nutrition_3['carbohydrate'] += getattr(each_food, 'carbohydrate')
        total_nutrition_3['protein'] += getattr(each_food, 'protein')
        total_nutrition_3['fat'] += getattr(each_food, 'fat')

    # 필요한 데이터를 JSON 형식으로 변환
    chart_info_json = json.dumps(total_nutrition_3)

    return chart_info_json

# def chart(nutrition_info_list, food_name=None):

#     # 사용자가 선택한 음식만
#     if food_name is not None:
#         nutrition_info_list = [food for food in nutrition_info_list if food.food_name == food_name]


#     total_carbohydrates = sum(food.carbohydrate for food in nutrition_info_list)
#     total_proteins = sum(food.protein for food in nutrition_info_list)
#     total_fats = sum(food.fat for food in nutrition_info_list)

#     nutrition_totals = {
#         'total_carbohydrates': total_carbohydrates,
#         'total_proteins': total_proteins,
#         'total_fats': total_fats,
#     }

#     chart_info_json = json.dumps(nutrition_totals)

#     return chart_info_json

    # # 마이페이지용, 선택된 게시물이 없으면 사용자의 전체 게시물의 영양소 불러오기
    # if post is None:
    #     user_nutrition_list = UserFoodNutritions.objects.filter(user=user)

    # # 게시물 단독 처리용. 하나의 게시물에 대한 영양정보 불러오기
    # else:
    #     user_nutrition_list = UserFoodNutritions.objects.filter(user=user, post=post)

    # nutrition_3 = {
    #     'carbohydrate': 0,
    #     'protein': 0,
    #     'fat': 0,
    # }

    # food_list = []

    # for each_record in user_nutrition_list:
    #     food_nutrition = each_record.nutrition_info
    #     food_list.append(food_nutrition)

    #     # 선택 없으면 건너뛰기, 선택한 음식만 합산
    #     if selected_foods is not None and food_nutrition not in selected_foods:
    #         continue

    #     nutrition_3['carbohydrate'] += getattr(food_nutrition, 'carbohydrate')
    #     nutrition_3['protein'] += getattr(food_nutrition, 'protein')
    #     nutrition_3['fat'] += getattr(food_nutrition, 'fat')

    # print('*****food_list:',food_list)
    # # json형식으로 전달해 차트 그림
    # chart_info_json = json.dumps(nutrition_3)

    # return chart_info_json, food_list