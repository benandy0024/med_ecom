# Generated by Django 2.2.4 on 2020-05-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0002_billingprofile_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='billingprofile',
            name='customer_id',
        ),
        migrations.AddField(
            model_name='billingprofile',
            name='stripecustomer',
            field=models.ForeignKey(default=False, on_delete='CASCADE', to='Billing.StripeCustomer'),
        ),
    ]
