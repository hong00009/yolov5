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
    food_name = models.CharField(max_length=255)
    calories = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    protein = models.FloatField()
    # 다른 필요한 필드 추가 가능

    def __str__(self):
        return self.food_name