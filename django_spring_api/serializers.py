# serializers.py
from rest_framework import serializers

from django_countries.serializer_fields import CountryField

from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    sex = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False)
    country = CountryField(required=False, default=None)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'age', 'sex', 'country')