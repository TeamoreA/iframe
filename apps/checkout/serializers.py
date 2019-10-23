# python modules
from datetime import datetime

# rest framework imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Local imports
from .models import UserCheckout


"""
    serializer to handle data to and from db for checkout Post functionality
"""


class AddCheckoutSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fullName = serializers.CharField(required=True)
    creditCardNumber = serializers.CharField(required=True,
                                             validators=[
                                                 UniqueValidator(
                                                     queryset=UserCheckout.objects.all(),
                                                     message=(
                                                         'Credit card number already exists'
                                                     )
                                                 )
                                             ])
    cvvNumber = serializers.IntegerField(required=True)
    expirationYear = serializers.IntegerField(required=True)
    expirationMonth = serializers.IntegerField(required=True)

    class Meta:
        model = UserCheckout
        fields = "__all__"

    def validate_card(data):

        # """
        #     Expiry year Validation
        # """

        if data['expirationYear'] < datetime.now().year:
            raise serializers.ValidationError(
                {"message": "The year entered indicates card has expired"}
            )

        # """
        #     Month validation
        # """

        elif data['expirationMonth'] not in range(1, 13):
            raise serializers.ValidationError(
                {"message": "Enter a valid month between 1 to 12 as per the card"}
            )

        """
        Card validation using luhn algorithm
        steps:
            1. Convert the card number to list of integers
            2. Parse through the list picking numbers at even list indexes
            3. Double the numbers from each even index and store te values in a different list
            4. Within the list above if any number is less than 9 store it in a diffrent list
            5. Within the list above if any number is greater than 9 store it in a diffrent list
            6. For the list on step 5 above flatten it and store the integers to list in step 4 above
            7. Traverse the original list picking numbers on odd indexes starting with index 1
            8. If the sum of list generated in step 6 and step 7 is equally divisible by 10 , Card valid!
            9 . If not 8 above raise card validation error
        """

        card_num = data['creditCardNumber']
        card_num = list(map(int, str(card_num)))

        even_indexes = card_num[0::2]
        new_list = [x * 2 for x in even_indexes]
        even_9_less = [i for i in new_list if i <= 9]

        str_nums_greater_9 = [str(i) for i in new_list if i > 9]

        for i in str_nums_greater_9:
            even_9_less.append(int(i[0]))
            even_9_less.append(int(i[1]))

        odd_indexes = card_num[1::2]
        total = sum(odd_indexes) + sum(even_9_less)

        if total % 10 == 0:
            return "Your visa card is valid"

        else:
            raise serializers.ValidationError(
                {"message": "Your card is invalid, Visit issuer to sort out the problem!!"}
            )

    # Method to save checkout data to db
    def create(self, data):
        user_checkout = UserCheckout(**data)
        user_checkout.save()
        return user_checkout
