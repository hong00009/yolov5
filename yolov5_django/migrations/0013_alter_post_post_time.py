# Generated by Django 4.2.5 on 2023-10-02 01:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('yolov5_django', '0012_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
