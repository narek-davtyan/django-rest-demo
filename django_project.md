
# Django REST API Project

The goal of this project to create a simple Django REST API. The only object to be created is a user with first name, last name, age, sex, email and country of residence attributes. A simple token authentication is to be used to protect our API. 

The extra step is deploying the project to the cloud to make API publicly accessible. 

## Prerequisites 

This project is carried out within the conda environment having all packages installed using conda and pip:
```bash
conda create -n django_min python=3.8 django
```
The environment is then activated:
```bash
conda activate django_min
```

## Setting up Django project and app

### Create a Django project

Let's create a new Django project, called `django_spring_dash`:
```bash
django-admin startproject django_spring_dash
```

The following directories and files are created:
```bash
django_spring_dash
├── django_spring_dash
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
└── manage.py
1 directory, 6 files
```

Let's step into the project's root directory `django_spring_dash`:
```bash
cd django_spring_dash
```
All files and directories are now used with relative paths. 

We can check that it is working by starting the server:
```bash
python manage.py runserver
```
The project is now accessible on [localhost:8000](http://localhost:8000).

We stop the server for now with CTRL+C.

### Create a Django app

Let’s create a new app for the API, called `django_spring_api`:
```bash
python manage.py startapp django_spring_api
```

The following directories and files are created within the project's root directory `django_spring_dash`:
```bash
django_spring_api
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│ └── __init__.py
├── models.py
├── tests.py
└── views.py
1 directory, 7 files
```

### Register the app with the project

To include the `django_spring_api` app in our project, we need to add a reference to its configuration class `DjangoSpringApiConfig` in the `INSTALLED_APPS` setting, located in `django_spring_dash/settings.py`, to obtain :
```python
# this is only part of code
# ...
# Application definition

INSTALLED_APPS = [
	'django_spring_api.apps.DjangoSpringApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# ...
```
For the time being, we leave the default apps untouched.

### Migrate models to the database

Some of the apps in `INSTALLED_APPS` have models that make use of at least one database table, hence we create the tables in the database before we can use them:
```bash
python manage.py migrate
```
> Whenever we define or change a model, we need to migrate those changes.

As for the database type, we leave the default SQLite choice (defined in `django_spring_dash/settings.py`) for now.

### Create a superuser for the admin UI

It may be beneficial to make use of the Django admin web UI for the project to observe the evolution of data in the database.

In order to gain access to the admin panel, we need login credentials. Hence, we create a superuser:
```bash
python manage.py createsuperuser
```
In the context of this sample project, the login is `olivertwist`, the email is `olivertwist@mail.com` and the password is `Twist2021`.

We can check that it is working by starting the server:
```bash
python manage.py runserver
```
The admin panel is now accessible on [localhost:8000/admin](http://localhost:8000/admin).

We stop the server for now with CTRL+C.

## Setting up a model

We want to have a database of users. Hence, we need to set up the user model. Our user model should comprise several attributes for each user: a first name, a last name, an email, an age, a sex, country of residence (multiple-choice).

We would need an extra library to deal with various countries management:
```bash
pip install 'django-countries[pyuca]'
```

We would need to add this app in our project, hence we add a reference in the `INSTALLED_APPS` setting, located in `django_spring_dash/settings.py`, to obtain :
```python
# this is only part of code
# ...
# Application definition

INSTALLED_APPS = [
	'django_spring_api.apps.DjangoSpringApiConfig',
	'django_countries',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# ...
```

### Create a model

We create a `User` class in `django_spring_api/models.py` like so:
```python
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
```

### Migrate models to the database

We have created a model and want to store those changes as a migration (these files are located in `django_spring_api/migrations/`):
```bash
python manage.py makemigrations
```
We apply that migration:
```bash
python manage.py migrate
```

### Register our app in the admin site

For our app to show up in the admin web UI, we need to register it in `django_spring_api/admin.py`:
```python
from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email', 'sex', 'country')

    search_fields = ['first_name', 'last_name', 'email', 'sex', 'country']

admin.site.register(User, UserAdmin)
```

We can check that it is working by starting the server:
```bash
python manage.py runserver
```
The admin panel is now accessible on [localhost:8000/admin](http://localhost:8000/admin).

We stop the server for now with CTRL+C.

We can create and edit users from the admin panel.

## Setting up a REST framework

We need to serialize the data from our database via endpoints using a  REST framework.

We would need to install an extra library:
```bash
pip install djangorestframework
```

We would need to add this app in our project, hence we add a reference in the `INSTALLED_APPS` setting, located in `django_spring_dash/settings.py` and limiting POST requests to authenticated users only by creating `REST_FRAMEWORK` dictionary, so that we get :
```python
# this is only part of code
# ...
# Application definition

INSTALLED_APPS = [
	'django_spring_api.apps.DjangoSpringApiConfig',
	'django_countries',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

REST_FRAMEWORK = {
    # Using Django's standard `django.contrib.auth` permissions
    # or providing read-only access for unauthenticated users
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
# ...
```

## Serializing a model

First, we create a serializer file:
```bash
touch django_spring_api/serializers.py
```

Inside `django_spring_api/serializers.py`, we create a class that links our model and the serializer:
```python
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
```
## Setting up a view

In order to visualize the REST API, we need a view that is accessible without credentials (unlike the admin panel).

### Create a view

We edit `django_spring_api/views.py` to add a `UserViewSet` view:
```python
# views.py
from rest_framework import viewsets

from .serializers import UserSerializer
from .models import User

# Definition of the view behavior in the API
class UserViewSet(viewsets.ModelViewSet):
	# Users will be ordered by their last names and not ids
    queryset = User.objects.all().order_by('last_name')
    serializer_class = UserSerializer
```

### Link a view

We need to link our view to a URL by modifying `django_spring_dash/urls.py` like so:
```python
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from django_spring_api import views

# Automatically determining the URL configuration
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
	# Our API with automatic URL routing
    path('', include(router.urls)),
    # Our admin panel
    path('admin/', admin.site.urls),
    # Login URLs for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

We can check that it is working by starting the server:
```bash
python manage.py runserver
```
The REST API is now accessible on [localhost:8000](http://localhost:8000).

## Protecting an API

There are many ways to protect our API from unauthorized access. Our goal is to enable a simple token authentication. We use the one provided in the REST framework.

Careful, in the development environment using token authentication with HTTP is fine, the production environment, however, must come with HTTPS to keep our API safe.

We first need to modify our `django_spring_dash/settings.py` to add `rest_framework.authtoken` into `INSTALLED_APPS` and modify `REST_FRAMEWORK` settings:
```python
# this is only part of code
# ...
# Application definition

INSTALLED_APPS = [
    'django_spring_api.apps.DjangoSpringApiConfig',
    'django_countries',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
               'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
                'rest_framework.permissions.IsAuthenticated',
    ),
}
# ...
```

We would then need to migrate the changes:
```bash
python manage.py migrate
```
We need to provide a URL for POST requests in `django_spring_dash/urls.py` to get a token against a login and password to then access the API:
```python
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
    path('api-token-auth/', auth_views.obtain_auth_token, name='api-token-auth'),
    # Login URLs for the browsable API
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

We can check that it is working by starting the server:
```bash
python manage.py runserver
```
### Access to an API

We no longer can access the API from the web browser, since authentication credentials were not provided. 

To get access we need to get the token with our login `olivertwist` and password `Twist2021` using a POST request. We can use different tools to verify our solution (e.g. postman, httpie, curl). 

More tokens can be generated for other users with the admin panel which is still available using a web browser.

#### Access via httpie

Here is an example of use. Attention! This provided server URL (`http://localhost:8000/`) can be different!

First, we install httpie:
```bash
pip install httpie
```
We now can make our POST request:
```bash
http POST http://localhost:8000/api-token-auth/ username='olivertwist' password="Twist2021"
```
And we get our token as a string in a dictionary `{"token":"b985e5659288c2cecc3a20611a4ec6fb60057a44"}`.

Our API is accessible using our token.

Here are some example requests:
```bash
http http://localhost:8000/ "Authorization: Token b985e5659288c2cecc3a20611a4ec6fb60057a44"
;
http http://localhost:8000/users/ "Authorization: Token b985e5659288c2cecc3a20611a4ec6fb60057a44"
;
http http://localhost:8000/users/1/ "Authorization: Token b985e5659288c2cecc3a20611a4ec6fb60057a44"
;
http POST http://localhost:8000/users/ "Authorization: Token b985e5659288c2cecc3a20611a4ec6fb60057a44" age=45 first_name="M.C." last_name="Escher"
;
http PUT http://localhost:8000/users/1/ "Authorization: Token b985e5659288c2cecc3a20611a4ec6fb60057a44" sex="M" country="USA" first_name="Fernando" last_name="Martinez"
;
http DELETE http://127.0.0.1:8000/users/17/  "Authorization: Token b985e5659288c2cecc3a20611a4ec6fb60057a44"
```

## Deploying to a cloud

To use the API without the local server turning all the time, we need to deploy our Django project to the cloud.

We need to set up a GitHub project, Google Cloud project and prepare the code for the production environment.

### Prepare project environment

We use Google Cloud App Engine with standard environment. In Google Cloud, we set up a project using this [standard guide](https://cloud.google.com/python/django/appengine?authuser=1#cloud-console).  

We also create a GitHub project with a Python-specific `./.gitignore`, `./LICENSE` and a `./README.md`. The contents of the entire Django project should be in the github repo, not just the Django app. 

### Prepare project files

Production environment also requires some security-related changes.

We start off by modifying `django_spring_dash/settings.py`.

We disable `DEBUG` mode and add entries in `ALLOWED_HOSTS`, including the generated name of the public website.
```python
# this is only part of code
# ...
DEBUG = False

ALLOWED_HOSTS = ['back-api-dot-django-spring-dash-demo.ew.r.appspot.com', '127.0.0.1']
# ...
```
Since running Django with a known SECRET_KEY defeats many of Django’s security protections, we protect `SECRET_KEY` :
```python
# this is only part of code
# ...
if not os.getenv('SECRET_KEY', None):
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&amp;*(-_=+)'
    new_key = get_random_string(50, chars)
    os.environ['SECRET_KEY'] = new_key

SECRET_KEY = os.environ.get('SECRET_KEY')
# ...
```

It's rather troublesome to use SQLite with Google Cloud, so we switch to MySQL:
```python
# this is only part of code
# ...
import pymysql  # noqa: 402

pymysql.version_info = (1, 4, 6, 'final', 0)  # change mysqlclient version
pymysql.install_as_MySQLdb()

# [START db_setup]
if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/django-spring-dash-demo:europe-west2:django-mysql-dash',
            'USER': 'olivertwist',
            'PASSWORD': 'Twist2021',
            'NAME': 'Users',
        }
    }
elif os.getenv('DJANGO_DB_SQLITE', None):
    # Use a sqlite3 database when testing in local systems
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }
else:
    # Running locally so connect to either a local MySQL instance or connect to
    # Cloud SQL via the proxy. To start the proxy via command line:
    #
    #     $ cloud_sql_proxy -instances="django-spring-dash-demo:europe-west2:django-mysql-dash"=tcp:3306
    #
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'NAME': 'Users',
            'USER': 'olivertwist',
            'PASSWORD': 'Twist2021',
        }
    }
```

We need to avoid transmitting access tokens in clear:
```python
# this is only part of code
# ...
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

We need to create some extra files for the project to function properly.

`./app.yaml`:
```yaml
# [START django_app]
runtime: python38
service: back-api

handlers:
# This configures Google App Engine to serve the files in the app's static
# directory.
- url: /static
  static_dir: static/

# This handler routes all requests not caught above to your main app. It is
# required when static routes are defined, but can be omitted (along with
# the entire handlers section) when there are no static files defined.
- url: /.*
  script: auto
# [END django_app]
```

`./requirements.txt`:
```
Django==3.1.7
PyMySQL==1.0.2
djangorestframework==3.12.4
django-countries==7.1
```

`./main.py`:
```python
from django_spring_dash.wsgi import application

# App Engine by default looks for a main.py file at the root of the app
# directory with a WSGI-compatible object called app.
# This file imports the WSGI-compatible object of your Django app,
# application from mysite/wsgi.py and renames it app so it is discoverable by
# App Engine without additional configuration.
# Alternatively, you can add a custom entrypoint field in your app.yaml:
# entrypoint: gunicorn -b :$PORT mysite.wsgi
app = application
```

### Deploying

The project is then pushed to GitHub and cloned to the cloud. The required migrations have to be done for the new MySQL database.  

The final steps for deploying are :
```bash
python manage.py collectstatic
```
```bash
gcloud app deploy
```

The API is now publicly available via https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/.
