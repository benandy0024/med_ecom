# Generated by Django 2.2.4 on 2020-05-06 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0005_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
