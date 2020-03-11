from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from employee.serializers import EmployeeSerializer, AuthTokenSerializer


class CreateEmployeeView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = EmployeeSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
