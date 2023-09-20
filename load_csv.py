import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project.settings")
import django
django.setup()
import csv
from yolov5_django.models import FoodNutrition
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project.settings")


# CSV 파일 경로
csv_file_path = './NutritionDB.csv'

try:
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            if '\ufeffclass' in row:
                row['class'] = row.pop('\ufeffclass')

            # "-" 값을 0으로 변환
            for key in row:
                if row[key] == "-":
                    row[key] = 0

            try:
                food_nutrition = FoodNutrition(
                    class_index=int(row["class"]),
                    category=row["분류"],
                    code=row["코드"],
                    food_name=row["음 식 명"],
                    weight=float(row["중량(g)"]),
                    energy=float(row["에너지(kcal)"]),
                    carbohydrate=float(row["탄수화물(g)"]),
                    protein=float(row["단백질(g)"]),
                    fat=float(row["지방(g)"]),
                    sodium=float(row["나트륨(mg)"]),
                    saccharide=float(row["당류(g)"]),
                    calcium=float(row["칼슘(mg)"]),
                    phosphorus=float(row["인(mg)"]),
                    potassium=float(row["칼륨(mg)"]),
                    magnesium=float(row["마그네슘(mg)"]),
                    iron=float(row["철(mg)"]),
                    zinc=float(row["아연(mg)"]),
                    cholesterol=float(row["콜레스테롤(mg)"])
                )
                food_nutrition.save()
            except Exception as e:
                print(f"Error saving row: {row}, Error: {str(e)}")

except FileNotFoundError:
    print(f"CSV file not found at path: {csv_file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")