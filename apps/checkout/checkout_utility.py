# Standard Library imports
import os
import requests
import json

# Django imports
from django.db.models import Max

# Local imports
from .models import UserPurchase
from ..authentication.backends import authenticate_credentials


def append_user_id(request):
    # Validate token in payload
    user = authenticate_credentials(request.data['api_token'])
    # Pass user id as part of the data
    request.data['user_id'] = user.id

    return {
        "request": request,
        "user": user
    }


def get_invoice_number(data):

    # import pdb; pdb.set_trace()
    highest_invoice_number = UserPurchase.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
    if highest_invoice_number is None:
        highest_invoice_number = 1

    highest_invoice_number += 1

    data['invoice_number'] = highest_invoice_number
    return highest_invoice_number


class FortnoxInvoice():
    # Class attribute on request header to fortnox
    headers = {
        "Access-Token": os.getenv('FORTNOX_ACCESS_TOKEN'),
        "Client-Secret": os.getenv('FORTNOX_CLIENT_SECRET'),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Method to use our user info to create a customer on fornox
    def create_fortnox_customer(self, data):
        # payload to create user on fortnox with user_email and username
        payload = json.dumps({
            "Customer": {
                "Name": data['user'].username,
                "Email": data['user'].email
            }
        })

        #  create user as customer on fortnox
        try:
            customer_request = requests.post(
                "https://api.fortnox.se/3/customers",
                data=payload,
                headers=self.headers
            )
            # Format the response data and message. While converting the data to json
            response_data = {
                'message': {
                    'status': '{status_code}'.format(status_code=customer_request.status_code),
                    'body': '{content}'.format(content=json.loads(customer_request.content))
                }
            }
        # Handle the error if customer creation is not successfull
        except requests.exceptions.RequestException:
            response_data = {
                'message': 'HTTP Request failed'
            }
        # Return the respond data
        return response_data

    # Method to post invoice to fortnox
    def post_invoice_to_fortnox(self, data):
        # Call the cutsomer creation methhod and fetch the customer data after creation
        customer = self.create_fortnox_customer(data)

        # Convert the customer data to a dictionary object to be able to retrieve the data
        customer_data = customer['message']['body']
        customer_data = eval(customer_data)

        # Generate an invoice number
        invoice_number = get_invoice_number(data)

        # Create a payload to create user invoice using invoice number and
        # customer number retrieved from the creation above
        payload = json.dumps({
            "Invoice": {
                "InvoiceRows": [
                    {
                        "DeliveredQuantity": data['request'].data['quantity'],
                        "ArticleNumber": invoice_number
                    }
                ],
                "CustomerNumber": customer_data['Customer']['CustomerNumber']
            }
        })

        # Create an invoice for the users purchase on fortnox
        try:
            invoice_request = requests.post(
                "https://api.fortnox.se/3/invoices",
                data=payload,
                headers=self.headers
            )
            # Format the response data and message
            response_data = {
                'message': {
                    'status': '{status_code}'.format(status_code=invoice_request.status_code),
                    'body': '{content}'.format(content=json.loads(invoice_request.content))
                },
                'invoice_number': invoice_number
            }

        # Catch the error incase of failure
        except requests.exceptions.RequestException:
            response_data = {
                'message': 'HTTP Request failed'
            }
        # return respose data and code
        return response_data
