# 음식 사진 속 객체탐지 결과 출력을 위한 함수
# 음식 이름, 음식 탄단지 정보(차트용) 반환
# food_name_list, chart_info_json 
from .models import FoodNutrition, Post
from accounts.models import UserFoodNutritions
from .chart import chart

def food_info(post):
    if post.detection_result is None:
        #검출된 객체가 없으면
        print('**food_info함수 : 객체검출X')
        return 0, 0, 0, 0, 0

    # 해당 post와 연결되어 저장된 UserFoodNutritions 모두 찾아오기
    user_food_nutritions_list = UserFoodNutritions.objects.filter(user=post.user_id, post=post.id)

    # 영양정보 추출하여 리스트로 저장
    nutrition_info_list = [each_item.nutrition_info for each_item in user_food_nutritions_list]

    food_name_list = [each_food.food_name for each_food in nutrition_info_list]
    # 모든 음식 이름 추출하여 리스트로 저장

    total_chart_info_json, each_chart_info_json, percentage = chart(nutrition_info_list)
    # 차트에 그릴 정보 json형식으로 반환받음

    return food_name_list, nutrition_info_list, total_chart_info_json, each_chart_info_json, percentage