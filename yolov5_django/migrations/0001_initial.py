# Generated by Django 4.2.5 on 2023-09-19 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodNutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_index', models.IntegerField()),
                ('category', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('food_name', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
                ('energy', models.FloatField()),
                ('carbohydrate', models.FloatField()),
                ('protein', models.FloatField()),
                ('fat', models.FloatField()),
                ('sodium', models.FloatField()),
                ('saccharide', models.FloatField()),
                ('calcium', models.FloatField()),
                ('phosphorus', models.FloatField()),
                ('potassium', models.FloatField()),
                ('magnesium', models.FloatField()),
                ('iron', models.FloatField()),
                ('zinc', models.FloatField()),
                ('cholesterol', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
