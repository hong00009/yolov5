# Generated by Django 4.2.5 on 2023-09-24 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_userfoodnutritions_carbohydrate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfoodnutritions',
            old_name='food_nutrition',
            new_name='nutrition_info',
        ),
    ]
