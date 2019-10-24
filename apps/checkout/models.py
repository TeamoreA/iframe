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
