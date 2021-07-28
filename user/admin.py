from django.contrib import admin

from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined','date_of_birth', 'first_name', 'last_name', 'image', 'email', 'address', 'phone', 'city', 'country']
    readonly_fields = ['username',   'email', 'address', 'phone', 'city', 'country', 'zipcode', 'state']


# Register your models here.
admin.site.register(UserProfile,UserProfileAdmin)
