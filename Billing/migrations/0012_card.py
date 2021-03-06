# Generated by Django 2.2.4 on 2020-05-13 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0011_remove_billingprofile_new_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(blank=True, max_length=120, null=True)),
                ('brand', models.CharField(blank=True, max_length=120, null=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('exp_month', models.IntegerField()),
                ('exp_year', models.IntegerField()),
                ('last4', models.CharField(blank=True, max_length=20, null=True)),
                ('billing_profile', models.ForeignKey(on_delete='CASCADE', to='Billing.BillingProfile')),
            ],
        ),
    ]
