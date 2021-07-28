from django.contrib import admin
from . models import *




class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject', 'message', 'status', 'note']
    readonly_fields = ['first_name', 'last_name', 'subject', 'email', 'message']
    list_filter = ['status']
    list_display_links = ['status', 'first_name', 'last_name', 'note']
    search_fields = ['first_name', 'last_name', 'email', 'subject', 'message', 'status', 'note']
    list_per_page = 20


# Register your models here.
admin.site.register(Profile)
admin.site.register(Manufacturers)
admin.site.register(ContactMessage,ContactMessageAdmin)
