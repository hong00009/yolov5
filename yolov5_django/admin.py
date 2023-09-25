from django.contrib import admin
from .models import Post, FoodNutrition

# Register your models here.
admin.site.register(Post)
admin.site.register(FoodNutrition)
