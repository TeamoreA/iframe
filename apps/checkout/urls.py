# Django imports
from django.urls import path

# Local imports
from .views import PostUserCheckoutView

urlpatterns = [
    path('', PostUserCheckoutView.as_view(), name="post_user_checkout"),
]
