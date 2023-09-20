from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class UploadedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FoodNutrition(models.Model):
    class_index = models.IntegerField() # 클래스 0~399
    category = models.CharField(max_length=255) # 분류
    code = models.CharField(max_length=255) # 코드 01-011-001
    food_name = models.CharField(max_length=255) # 음식이름
    weight = models.FloatField() # 중량
    energy = models.FloatField() # 열량
    carbohydrate = models.FloatField() # 탄수화물
    protein = models.FloatField() # 단백질
    fat = models.FloatField() # 지방
    sodium = models.FloatField() # 나트륨
    saccharide = models.FloatField() #당류
    calcium = models.FloatField() # 칼슘
    phosphorus = models.FloatField() # 인
    potassium = models.FloatField() # 칼륨
    magnesium = models.FloatField() # 마그네슘
    iron = models.FloatField() # 철
    zinc = models.FloatField()# 아연
    cholesterol = models.FloatField() # 콜레스테롤

    def __str__(self):
        return self.code, self.food_name