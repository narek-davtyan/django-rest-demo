from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email', 'sex', 'age')#, 'country')

    search_fields = ['first_name', 'last_name', 'email', 'sex', 'age']#, 'country']

admin.site.register(User, UserAdmin)