# django imports

# restframe work imports
from rest_framework import status
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Local imports
from .serializers import (
    AddCheckoutSerializer,
    PurchaseSerializer
)
from .checkout_utility import (
    append_user_id,
    FortnoxInvoice
)


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
        # append user id to request 
        request = append_user_id(request)

        serializer = self.serializer_class(
            data=request['request'].data,
            context={'request': request}
        )

        # Validate data entered
        AddCheckoutSerializer.validate_card(data=request['request'].data)

        if serializer.is_valid():
            serializer.save()

            response_message = {
                "message": "Checkout data successfully posted"
            }

            return Response(response_message, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPurchaseInvoiceView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PurchaseSerializer

    def post(self, request):
        # append user id to request
        request = append_user_id(request)

        # process data with fortnox
        fortnox_response = FortnoxInvoice().post_invoice_to_fortnox(request)
        invoice_data = eval(fortnox_response['message']['body'])

        # import pdb; pdb.set_trace()
        if fortnox_response['message']['status'] == '201':
            # set invoice number to the one sent to fortnox
            request['request'].data['invoice_number'] = fortnox_response['invoice_number']
            request['request'].data['fortnox_invoice_url'] = invoice_data['Invoice']['@url']
            request['request'].data['fortnox_customer_id'] = invoice_data['Invoice']['CustomerNumber']
            request['request'].data['fortnox_response_body'] = str(invoice_data['Invoice'])

            serializer = self.serializer_class(
                data=request['request'].data
            )

            # Save checkout data
            if serializer.is_valid():
                serializer.save()

                response_message = {
                    "message": "Purchase is being processed",
                    "data": serializer.data,
                    "fortnox_response": fortnox_response
                }

                return Response(response_message, status=status.HTTP_201_CREATED)
            # Raise validation error if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return any error that was not caught
        return Response({
            "message": "Sorry, It's not you its us",
            "status": fortnox_response['message']['status'],
            "data": fortnox_response['message']
        })
