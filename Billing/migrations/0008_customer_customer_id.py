# Generated by Django 2.2.4 on 2020-05-06 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0007_remove_customer_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
