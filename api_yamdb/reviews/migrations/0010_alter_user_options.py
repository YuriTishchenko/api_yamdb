# Generated by Django 3.2 on 2023-06-27 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_alter_title_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Позьзователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
