# Generated by Django 2.2.4 on 2020-04-09 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0001_initial'),
        ('Orders', '0004_auto_20200409_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete='CASCADE', to='Billing.BillingProfile'),
        ),
        migrations.DeleteModel(
            name='Commande',
        ),
    ]
