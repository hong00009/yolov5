# Generated by Django 4.2.5 on 2023-09-22 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_userfoodnutritions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(default='2000-01-01'),
        ),
    ]
