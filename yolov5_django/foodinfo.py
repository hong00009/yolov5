# 음식 사진 속 객체탐지 결과 출력을 위한 함수
# 음식 클래스 인덱스번호, 음식 이름, 음식 탄단지 정보(차트용) 3가지 반환
# food_idx_list, food_name_list, chart_info_json 

from accounts.models import UserFoodNutritions
from .models import Post, FoodNutrition
from .chart import chart

def food_info(post):

    foods = UserFoodNutritions.objects.filter(post=post)
    print(foods)
    food_idx_list = '*123*'
    food_name_list = '*456*'

    chart_info_json, food_list = chart(post=post)

    return food_idx_list, food_name_list, chart_info_json 