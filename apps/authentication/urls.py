from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ApiTokenAPIView

app_name = 'authentication'

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name="register"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('api-token', ApiTokenAPIView.as_view(), name="api-token"),
]
