from django import forms
from django.forms import ModelForm
from django.forms import TextInput, EmailInput, FileInput, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='username')
    first_name = forms.CharField(max_length=50, help_text='first_name')
    last_name = forms.CharField(max_length=50, help_text='last_name')
    email = forms.EmailField(max_length=50, help_text='email')
    date_of_birth= forms.DateField(help_text='date_of_birth')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',  'password1', 'password2', 'date_of_birth')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user




STATE = [
    ('Abia', 'Abia'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Edo', 'Edo'),
    ('Imo', 'Imo'),
    ('Lagos', 'Lagos'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Oyo', 'Oyo'),
    ('Rivers', 'Rivers')
]



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile 
        fields = ('first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country', 'image')
        widgets = {
            'first_name': TextInput(attrs={'class':'rew', 'placeholder':'First Name'}),
            'last_name': TextInput(attrs={'class': 'rew', 'placeholder': 'Last Name'}),
            'email': EmailInput(attrs={'class': 'rew', 'placeholder': 'Email Address'}),
            'phone': TextInput(attrs={'class': 'rew', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'rew', 'placeholder':'Address'}),
            'city': TextInput(attrs={'class': 'rew', 'placeholder': 'city'}),
            'state': Select(attrs={'class': 'select', 'placeholder': 'State'}, choices=STATE),
            'country': TextInput(attrs={'class': 'rew', 'placeholder': 'Country'}),
            'image': FileInput(attrs={'placeholder': 'image'}), 
        }




