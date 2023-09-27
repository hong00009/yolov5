# Generated by Django 4.2.5 on 2023-09-27 11:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_food_nutrition_userfoodnutritions_nutrition_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(300.0)]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weight',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(300.0)]),
        ),
    ]
