from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

from yolov5_django.models import Post, FoodNutrition

# Create your models here.
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', '남성'),
        ('female', '여성'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthdate = models.DateField()  # 생년월일
    height = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(300.0)])
    weight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(350.0)])
    
    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        else:
            return None
        
    def __str__(self):
        return f"{self.user.username}님 프로필"
    

class UserFoodNutritions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    nutrition_info = models.ForeignKey(FoodNutrition, on_delete=models.SET_NULL, null=True)
    # FoodNutrition으로 연결, 음식객체 검출 안될 시 null저장

    datetime = models.DateTimeField() # 식사시간

    def __str__(self):
        datetime_reshape = self.datetime.strftime("%y%m%d_%H")
        return f"{datetime_reshape} - {self.user.username} - {self.post} - {self.nutrition_info.food_name if self.nutrition_info else None}"
