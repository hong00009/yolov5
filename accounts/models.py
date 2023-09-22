from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    gender = models.CharField(max_length=10)  # 성별 (남성, 여성, 기타 등)
    birthdate = models.DateField()  # 생년월일
    height = models.FloatField(validators=[MinValueValidator(0.0)])  # 키 (예: 175.5 cm)
    weight = models.FloatField(validators=[MinValueValidator(0.0)])  # 현재 몸무게 (예: 70.5 kg)
    
    def __str__(self):
        return f"{self.user.username}님 프로필"
    

class UserFoodNutritions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User 모델과 연결
    
    energy = models.FloatField() # 열량
    carbohydrate = models.FloatField() # 탄수화물
    protein = models.FloatField() # 단백질
    fat = models.FloatField() # 지방
    sodium = models.FloatField() # 나트륨
    datetime = models.DateTimeField(default=timezone.now) # 

    def __str__(self):
        return f"{self.user.username}님의 섭취영양정보"