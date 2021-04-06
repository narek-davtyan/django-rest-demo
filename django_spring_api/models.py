# models.py  
from django.db import models

from django_countries.fields import CountryField

class User(models.Model):  
    first_name = models.CharField(max_length=30)

    last_name = models.CharField(max_length=30)

    email = models.EmailField(max_length=30, default=None, blank=True, null=True)

    age_choices = list(map(lambda x: (x, x), range(15,101)))
    age = models.PositiveSmallIntegerField(
        choices=age_choices,
        default=None,
        blank=True,
        null=True
    )

    GENDER_CHOICES = (
        ('Man', 'Man'),
        ('Woman', 'Woman'),
        ('Other','Other'),
        ('Prefer not to say','Prefer not to say'),
        ('M', 'Man'),
        ('W', 'Woman'),
        ('O','Other'),
        ('P','Prefer not to say')
    )

    sex = models.CharField(max_length=17, choices=GENDER_CHOICES, 
    	default=None, blank=True, null=True)

    country = CountryField(default=None, blank=True, null=True)

    def __str__(self):  
        return self.first_name + " " + self.last_name 