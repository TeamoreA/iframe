# Generated by Django 2.2.6 on 2019-10-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCheckout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('full_name', models.CharField(max_length=254)),
                ('credit_card_number', models.CharField(max_length=254, unique=True)),
                ('cvv_number', models.IntegerField()),
                ('expiration_year', models.IntegerField()),
                ('expiration_month', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('invoice_number', models.IntegerField(default=0, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.FloatField()),
                ('currency_code', models.CharField(max_length=15)),
                ('date_of_purchase', models.DateTimeField(auto_now_add=True)),
                ('fortnox_invoice_url', models.CharField(max_length=100)),
                ('fortnox_customer_id', models.IntegerField()),
                ('fortnox_response_body', models.TextField()),
            ],
        ),
    ]
