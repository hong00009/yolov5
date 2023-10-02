# 음식에 대한 영양정보를 json형식으로 변환하여 프론트엔드측으로 전달하는 함수
# 탄단지 외 영양소 추가 확장 가능
import json

def chart(nutrition_info_list):

    total_nutrition_3 = { # 모든 음식 탄단지 합산
        'carbohydrate': 0,
        'protein': 0,
        'fat': 0,
    }

    each_nutrition_3 = {} # 음식 개별 탄단지

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


    # 탄단지 백분율 계산
    percentage_nutirition_3 = {}
    sum_nutrition_3 = sum(total_nutrition_3.values())

    if sum_nutrition_3 == 0:
        # 영양소 합계가 0인 경우, 모든 비율을 0으로 설정하고 계산 생략
        for each_nutrition in total_nutrition_3:
            percentage_nutirition_3[each_nutrition] = 0
    else:
        for each_nutrition in total_nutrition_3:
            percentage = (total_nutrition_3[each_nutrition] / sum_nutrition_3) * 100
            percentage_nutirition_3[each_nutrition] = round(percentage)

    
    # JSON 형식으로 변환
    total_chart_info_json = json.dumps(total_nutrition_3)
    each_chart_info_json = json.dumps(each_nutrition_3)

    return total_chart_info_json, each_chart_info_json, percentage_nutirition_3