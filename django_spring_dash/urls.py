"""django_spring_dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from django_spring_api import views

# Automatically determining the URL configuration
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
	# Our API with automatic URL routing
    path('', include(router.urls)),
    # Our admin panel
    path('admin/', admin.site.urls),
    # URL for POST requests to get the token
    path('api-token-auth/', auth_views.obtain_auth_token, name='api-tokn-auth'),
    # Login URLs for the browsable API
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]