# Django imports
from django.db import models

# Local imports
from ..authentication.models import User


"""
    Model  on user checkout
"""


class UserCheckout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=254, null=False)
    creditCardNumber = models.CharField(max_length=254, unique=True)
    cvvNumber = models.IntegerField(null=False)
    expirationYear = models.IntegerField(null=False)
    expirationMonth = models.IntegerField(null=False)
