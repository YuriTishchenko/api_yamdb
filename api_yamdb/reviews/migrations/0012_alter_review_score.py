# Generated by Django 3.2 on 2023-06-30 23:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_remove_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Оценка должна быть не меньше 1'), django.core.validators.MaxValueValidator(10, message='Оценка должна быть не больше 10')], verbose_name='оценка'),
        ),
    ]
