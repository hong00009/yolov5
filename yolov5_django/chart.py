from accounts.models import UserFoodNutritions
import json

def chart(user=None, post=None, selected_foods=None):

    # 마이페이지용, 선택된 게시물이 없으면 사용자의 전체 게시물의 영양소 불러오기
    if post is None:
        user_nutrition_list = UserFoodNutritions.objects.filter(user=user)

    # 게시물 단독 처리용. 하나의 게시물에 대한 영양정보 불러오기
    else:
        user_nutrition_list = UserFoodNutritions.objects.filter(user=user, post=post)

    nutrition_3 = {
        'carbohydrate': 0,
        'protein': 0,
        'fat': 0,
    }

    food_list = []

    for each_record in user_nutrition_list:
        food_nutrition = each_record.nutrition_info
        food_list.append(food_nutrition)

        # 선택 없으면 건너뛰기, 선택한 음식만 합산
        if selected_foods is not None and food_nutrition not in selected_foods:
            continue

        nutrition_3['carbohydrate'] += getattr(food_nutrition, 'carbohydrate')
        nutrition_3['protein'] += getattr(food_nutrition, 'protein')
        nutrition_3['fat'] += getattr(food_nutrition, 'fat')

    print('food_list:',food_list)
    # json형식으로 전달해 차트 그림
    chart_info_json = json.dumps(nutrition_3)

    return chart_info_json, food_list