# Generated by Django 2.2.4 on 2020-06-08 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_usercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='contact',
            field=models.CharField(default=False, max_length=120),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='pharmacy_name',
            field=models.CharField(default=False, max_length=120),
        ),
    ]
