# Generated by Django 2.2.4 on 2020-06-08 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200608_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomment',
            name='contact',
            field=models.CharField(default=None, max_length=120),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='pharmacy_name',
            field=models.CharField(default=None, max_length=120),
        ),
    ]
