# Django imports
from django.urls import path

# Local imports
from .views import (
    PostUserCheckoutView,
    UserPurchaseInvoiceView
)

urlpatterns = [
    path('', PostUserCheckoutView.as_view(), name="post_user_checkout"),
    path('purchase', UserPurchaseInvoiceView.as_view(), name="user_purchase")
]
