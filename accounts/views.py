from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer

class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
