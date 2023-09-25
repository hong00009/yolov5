# 음식 사진 속 객체탐지 결과 출력을 위한 함수
# 음식 이름, 음식 탄단지 정보(차트용) 반환
# food_name_list, chart_info_json 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from accounts.models import UserFoodNutritions
from .models import Post, FoodNutrition
from .chart import chart

def food_info(post):
    class_idx_list = [int(class_idx) for class_idx in post.detection_result.split(',')]
    # 검출결과 문자열에서 음식의 class idx (int형) 개별 추출하여 리스트에 저장
    
    nutrition_info_list = FoodNutrition.objects.filter(class_index__in=class_idx_list)
    # 음식 class idx리스트마다의 영양정보 가져와 모든 음식의 영양정보DB 리스트로 저장

    food_name_list = [each_food.food_name for each_food in nutrition_info_list]
    # 모든 음식 이름 추출하여 리스트로 저장

    chart_info_json = chart(nutrition_info_list)
    # 차트에 그릴 정보 json형식으로 반환받음

    return food_name_list, chart_info_json, nutrition_info_list


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # CSRF 보안 기능 비활성화 (개발 시에만 사용)
def get_nutrition_info(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))
        food_name = post_data.get('food_name')

        try:
            if food_name:  # 특정 음식의 영양 정보를 요청한 경우
                nutrition_info = FoodNutrition.objects.get(food_name=food_name)
                nutrition_info_list = [nutrition_info]
            else:  # 모든 음식의 영양 정보를 요청한 경우
                nutrition_info_list = list(FoodNutrition.objects.all())

            chart_info_json = chart(nutrition_info_list, food_name)

            total_carbohydrates = sum(food.carbohydrate for food in nutrition_info_list)
            total_proteins = sum(food.protein for food in nutrition_info_list)
            total_fats = sum(food.fat for food in nutrition_info_list)

            response_data ={
                'carbohydrate': total_carbohydrates,
                'protein': total_proteins,
                'fat': total_fats,
                'chart_json': chart_info_json
            }

            return JsonResponse(response_data)

        except FoodNutrition.DoesNotExist:
            return JsonResponse({'error':'음식을 찾을 수 없습니다.'}, status=404)

    else:
        return JsonResponse({'error':'Invalid request method.'}, status=405)
