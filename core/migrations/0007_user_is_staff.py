# Generated by Django 2.2.4 on 2020-05-31 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200531_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
