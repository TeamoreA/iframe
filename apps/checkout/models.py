# Django imports
from django.db import models

"""
    Model  on user checkout
"""


class UserCheckout(models.Model):
    user_id = models.IntegerField(null=False)
    full_name = models.CharField(max_length=254, null=False)
    credit_card_number = models.CharField(max_length=254, unique=True)
    cvv_number = models.IntegerField(null=False)
    expiration_year = models.IntegerField(null=False)
    expiration_month = models.IntegerField(null=False)


class UserPurchase(models.Model):
    user_id = models.IntegerField(null=False)
    invoice_number = models.IntegerField(unique=True, null=False, default=0)
    quantity = models.IntegerField(default=0)
    amount = models.FloatField(null=False)
    currency_code = models.CharField(max_length=15, null=False)
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    fortnox_invoice_url = models.CharField(max_length=100, null=False)
    fortnox_customer_id = models.IntegerField(null=False)
    fortnox_response_body = models.TextField()
