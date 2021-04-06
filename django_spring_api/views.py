# views.py
from rest_framework import viewsets

from .serializers import UserSerializer
from .models import User

# Definition of the view behavior in the API
class UserViewSet(viewsets.ModelViewSet):
	# Users will be ordered by their last names and not ids
    queryset = User.objects.all().order_by('last_name')
    serializer_class = UserSerializer