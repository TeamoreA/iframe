# django imports

# restframe work imports
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Local imports
from .serializers import AddCheckoutSerializer


"""
    View to post user checkout data
        the body should include
        {
            "fullName": "As per the card ",
            "creditCardNumber": card numbers without hyphens or spaces,
            "cvvNumber": 3 digit number at back of card,
            "expirationYear": Card expiration year,
            "expirationMonth": Card expiration month
        }

        The token will be collected from the header
"""


class PostUserCheckoutView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AddCheckoutSerializer

    def post(self, request):

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
