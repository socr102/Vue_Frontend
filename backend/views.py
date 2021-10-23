from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer
from .schema import auth_schema

@auth_schema
class CustomTokenObtainPairView(TokenObtainPairView):
    """Get token pair"""
    serializer_class = CustomTokenObtainPairSerializer
