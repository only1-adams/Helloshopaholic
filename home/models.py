from django.db import models

from django.forms import Textarea, TextInput
from django.forms import ModelForm
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Profile(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length=100)
    keywords= models.CharField(max_length=225)
    description = models.CharField(max_length=225, null=True)
    company = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50, blank=True)
    icon = models.ImageField(blank=True, null=True, upload_to='images/')
    logo = models.ImageField(blank=True, null=True, upload_to='images/')
    cart_icon = models.ImageField(blank=True, null=True, upload_to='images/')
    menu_icon = models.ImageField(blank=True, null=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    about = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    bannertext= models.CharField(max_length=300)

    def __str__ (self):
        return self.title


class Manufacturers(models.Model):
    title = models.CharField(max_length=10, blank=True, null=True)
    manufacturers = models.ImageField(blank=True, null=True, upload_to='images/')

    def __str__(self):
        return self.title
     


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    )

    first_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    note = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    
class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
