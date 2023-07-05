from django.urls import path
from .views import RegistrationView, ActivationView, LoginView, LogoutView, ChangePasswordView


urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("activate/", ActivationView.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]