# django imports

# restframe work imports
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Local imports
from .serializers import AddCheckoutSerializer
from ..authentication.backends import authenticate_credentials


"""
    View to post user checkout data
        the body should include
        {
            "api_token": "API token provided",
            "full_name": "As per the card ",
            "credit_card_number": card numbers without hyphens or spaces,
            "cvv_number": 3 digit number at back of card,
            "expiration_year": Card expiration year,
            "expiration_month": Card expiration month
        }

        The token will be collected from the header
"""


class PostUserCheckoutView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = AddCheckoutSerializer

    def post(self, request):

        # Validate token in payload
        user = authenticate_credentials(request.data['api_token'])
        # Pass user id as part of the data
        request.data['user_id'] = user.id

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        # Validate data entered
        AddCheckoutSerializer.validate_card(data=request.data)

        if serializer.is_valid():
            serializer.save()

            response_message = {
                "message": "Checkout data successfully posted"
            }

            return Response(response_message, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
