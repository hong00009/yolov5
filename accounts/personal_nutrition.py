# 게시물에서 검출된 음식객체 수만큼 UserFoodNutritions 영양정보를 DB에 저장하는 함수
# BMI등 건강관련 수치 계산 함수
from datetime import timedelta
from django.db.models import Sum, Avg, Count
import calendar
from django.utils import timezone

from .models import UserFoodNutritions
from yolov5_django.models import FoodNutrition, Post
from yolov5_django.forms import DateRangeFilterForm
from .models import UserFoodNutritions

def save_personal_food_nutrition(user, post, detected_foods):

    if detected_foods is not None:
        food_list = [int(index) for index in detected_foods.split(",")]

        for each_food in food_list:
            each_food_nutris = FoodNutrition.objects.get(class_index=each_food)

            nutrition_info = UserFoodNutritions(
                user = user,
                post = post,

                nutrition_info = each_food_nutris,
                
                datetime = post.post_time,
            )
            nutrition_info.save()

def bmi_calculator(user):
    user_profile = user.userprofile

    height = user_profile.height / 100  
    weight = user_profile.weight
    gender = user_profile.gender

    # 표준 체중 계산
    if gender == 'male':
        standard_weight = round(height * height * 22, 1)
    else:
        standard_weight = round(height * height * 21, 1)

    # BMI 계산
    bmi = round(weight / (height * height), 1)

    age = user.userprofile.age
    print(age)

    daily_kcal = 0
    meal_kcal = 0

    # 연령별 권장 섭취 칼로리 계산
    if age < 30: 
        if gender == 'male':
            daily_kcal = 2600
            meal_kcal = 870
        elif gender == 'female':
            daily_kcal = 2100
            meal_kcal = 700
    elif 30 <= age < 40:
        if gender == 'male':
            daily_kcal = 2500
            meal_kcal = 820
        elif gender == 'female':
            daily_kcal = 2000
            meal_kcal = 670
    elif 40<= age < 50:
        if gender == 'male':
            daily_kcal = 2400
            meal_kcal = 780
        elif gender == 'female':
            daily_kcal = 1900
            meal_kcal = 630
    elif 50 <= age < 60:
        if gender == 'male':
            daily_kcal = 2200
            meal_kcal = 730
        elif gender == 'female':
            daily_kcal = 1800
            meal_kcal = 600
    else:
        if gender == 'male':
            daily_kcal = 2000
            meal_kcal = 650
        elif gender == 'female':
            daily_kcal = 1600
            meal_kcal = 530

    return bmi, standard_weight, daily_kcal, meal_kcal


# 10~20대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,600kcal
# 한 끼 권장 칼로리 : 870kcal
# 30대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,500kcal
# 한 끼 권장칼로리 : 820kcal
# 40대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,400kcal
# 한 끼 권장칼로리 : 780kcal
# 50대 남자 권장 칼로리
# 하루 권장 칼로리 : 2,200kcal
# 한 끼 권장 칼로리 : 730kcal
# 60대 이상 남자 권장 칼로리
# 하루 권장칼로리 : 2,000kcal
# 한 끼 권장 칼로리 : 650kcal


# 10~20대 여자 권장 칼로리
# 하루 권장 칼로리 : 2,100kcal
# 한 끼 권장 칼로리 : 700kcal
# 30대 여자 권장 칼로리
# 하루 권장 칼로리 : 2,000kcal
# 한 끼 권장 칼로리 : 670kcal
# 40대 여자 권장 칼로리
# 하루 권장칼로리 : 1,900kcal
# 한 끼 권장 칼로리 : 630kcal
# 50대 여자 권장 칼로리
# 하루 권장칼로리 : 1,800kcal
# 한끼 권장칼로리 : 600kcal
# 60대 여자 권장 칼로리
# 하루 권장 칼로리 : 1,600kcal
# 한 끼 권장칼로리 : 530kcal

def stats(user):
    today = timezone.now().date()
    
    try:
        # 오늘 기준으로 통계량 계산
        daily_nutrition = UserFoodNutritions.objects.filter(user=user, datetime__date=today).aggregate(
            total_energy=Sum('nutrition_info__energy'),
            total_carbohydrate=Sum('nutrition_info__carbohydrate'),
            total_protein=Sum('nutrition_info__protein'),
            total_fat=Sum('nutrition_info__fat'),
        )

        start_of_week = today - timedelta(days=6)
        end_of_week = today
        
        # 이번 주의 모든 메뉴 합계(AVG를 구하기 위해)
        weekly_nutrition = UserFoodNutritions.objects.filter(
            user=user, datetime__date__range=[start_of_week, end_of_week]
        ).aggregate(
            total_energy=Sum('nutrition_info__energy'),
            total_carbohydrate=Sum('nutrition_info__carbohydrate'),
            total_protein=Sum('nutrition_info__protein'),
            total_fat=Sum('nutrition_info__fat'),
        )
        

        start_of_month = today.replace(day=1)
        # 현재 날짜로부터 이번 달의 마지막 날짜를 계산
        _, last_day_of_month = calendar.monthrange(today.year, today.month)

        # 이번 달의 마지막 날짜로 설정
        end_of_month = today.replace(day=last_day_of_month)

        # 이번 달의 모든 메뉴 합계(AVG를 구하기 위해)
        monthly_nutrition = UserFoodNutritions.objects.filter(
            user=user, datetime__date__range=[start_of_month, end_of_month]
        ).aggregate(
            total_energy=Sum('nutrition_info__energy'),
            total_carbohydrate=Sum('nutrition_info__carbohydrate'),
            total_protein=Sum('nutrition_info__protein'),
            total_fat=Sum('nutrition_info__fat'),
        )

        # 일주일 동안 게시글을 업로드한 날짜 count
        post = Post.objects.filter(user=user, post_time__range=(start_of_week, end_of_week))
        weekly_post_count = post.values('post_time__date').distinct().count()
        # 해당 월 동안 게시글을 업로드한 날짜 count
        post = Post.objects.filter(user=user, post_time__range=(start_of_month, end_of_month))
        monthly_post_count = post.values('post_time__date').distinct().count()
        
        # 주간 합계를 기간으로 나누어 하루에 어떤 영양소를 평균적으로 얼마나 섭취하는지 계산
        weekly_nutrition_avg = {
            'avg_energy': weekly_nutrition['total_energy'] / weekly_post_count,
            'avg_carbohydrate': weekly_nutrition['total_carbohydrate'] / weekly_post_count,
            'avg_protein': weekly_nutrition['total_protein'] / weekly_post_count,
            'avg_fat': weekly_nutrition['total_fat'] / weekly_post_count,
        }
        # 월간 합계를 기간으로 나누어 하루에 어떤 영양소를 평균적으로 얼마나 섭취하는지 계산
        monthly_nutrition_avg = {
            'avg_energy': monthly_nutrition['total_energy'] / monthly_post_count,
            'avg_carbohydrate': monthly_nutrition['total_carbohydrate'] / monthly_post_count,
            'avg_protein': monthly_nutrition['total_protein'] / monthly_post_count,
            'avg_fat': monthly_nutrition['total_fat'] / monthly_post_count,
        }
    except :
        return 0, 0, 0, 0

    return daily_nutrition, weekly_nutrition_avg, monthly_nutrition_avg, start_of_week