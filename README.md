# Django REST API Project

This project to create a simple Django REST API. The only object to be created is a user with first name, last name, age, sex, email and country of residence attributes. A simple token authentication is to be used to protect our API. The live server URL is available via https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/ cloud app.

## Sample use

The following examples use  `httpie`, however, other tools like `postman` will do.

First, get a token with a POST request providing a valid `username` and `password` in the request body:
```bash
http POST https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/api-token-auth/ username='olivertwist' password="Twist2021"
```
The following requests must include the token.

Get list of users [GET]:
```bash
http https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/users/ "Authorization: Token [TOKEN]"
```

Get a user by `id` [GET]:
```bash
http https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/users/1/ "Authorization: Token [TOKEN]"
```

Create a new user (`first_name` and `last_name` are mandatory) [POST]:
```bash
http POST https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/users/ "Authorization: Token [TOKEN]" age=45 first_name="M.C." last_name="Escher"
```

Update the user (`first_name` and `last_name` are mandatory) [PUT]:
```bash
http PUT https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/users/1/ "Authorization: Token [TOKEN]" sex="M" country="USA" first_name="Fernando" last_name="Martinez"
```

Remove the user with `id` [DELETE]:
```bash
http DELETE https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/users/17/  "Authorization: Token [TOKEN]"
```

## Admin panel

The admin panel is accessible with a web browser via https://back-api-dot-django-spring-dash-demo.ew.r.appspot.com/admin/, the credentials are the same as for getting a token.

The admin panel allows to easily manage users and tokens.

## Tutorial

The tutorial regarding this project is available via https://github.com/narek-davtyan/django_spring_dash/blob/main/django_project.md 