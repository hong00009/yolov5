# 음식 사진 속 객체탐지 결과 출력을 위한 함수
# 음식 이름, 음식 탄단지 정보(차트용) 반환
# food_name_list, chart_info_json 
from .models import FoodNutrition
from .chart import chart

def food_info(post):
    if post.detection_result is None:
        #검출된 객체가 없으면
        print('**객체검출X')
        return 0, 0, 0, 0, 0
    
    # 검출결과 문자열에서 음식의 class idx (int형) 개별 추출하여 리스트에 저장
    class_idx_list = [int(class_idx) for class_idx in post.detection_result.split(',')]
    
    nutrition_info_list = FoodNutrition.objects.filter(class_index__in=class_idx_list)
    # 음식 class idx리스트마다의 영양정보 가져와 모든 음식의 영양정보DB 리스트로 저장

    food_name_list = [each_food.food_name for each_food in nutrition_info_list]
    # 모든 음식 이름 추출하여 리스트로 저장

    total_chart_info_json, each_chart_info_json, percentage = chart(nutrition_info_list)
    # 차트에 그릴 정보 json형식으로 반환받음

    return food_name_list, nutrition_info_list, total_chart_info_json, each_chart_info_json, percentage