import django
django.setup()

import csv
from yolov5_django.models import FoodNutrition
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project.settings")


# CSV 파일 경로
csv_file_path = './NutritionDB.csv'

# CSV 파일 열기
with open(csv_file_path, 'r', encoding='utf-8 sig') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    
    for row in csv_reader:
        if '\ufeffclass' in row:
            row['class'] = row.pop('\ufeffclass')

        # "-" 값을 0으로 변환
        for key in row:
            if row[key] == "-":
                row[key] = "0"

        class_index = int(row["class"])  # 클래스 0~399
        category = row["분류"]
        code = row["코드"]
        food_name = row["음 식 명"]
        weight = float(row["중량(g)"])
        energy = float(row["에너지(kcal)"])
        carbohydrate = float(row["탄수화물(g)"])
        protein = float(row["단백질(g)"])
        fat = float(row["지방(g)"])
        sodium = float(row["나트륨(mg)"])
        saccharide = float(row["당류(g)"])
        calcium = float(row["칼슘(mg)"])
        phosphorus = float(row["인(mg)"])
        potassium = float(row["칼륨(mg)"])
        magnesium = float(row["마그네슘(mg)"])
        iron = float(row["철(mg)"])
        zinc = float(row["아연(mg)"])
        cholesterol = float(row["콜레스테롤(mg)"])
        
        # Django 모델 객체 생성 및 저장
        food_nutrition = FoodNutrition(
            class_index=class_index,
            food_name=food_name,
            weight=weight,
            energy=energy,
            carbohydrate=carbohydrate,
            protein=protein,
            fat=fat,
            sodium=sodium,
            saccharide=saccharide,
            calcium=calcium,
            phosphorus=phosphorus,
            potassium=potassium,
            magnesium=magnesium,
            iron=iron,
            zinc=zinc,
            cholesterol=cholesterol,
        )
        food_nutrition.save()