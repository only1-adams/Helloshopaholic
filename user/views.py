from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import UserProfile
from home.models import *
from product.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash 

# Create your views here.

def user(request):
    profile = Profile.objects.get(pk=1)
    profiles = UserProfile.objects.get(user__username = request.user.username) 
    manufacturers=Manufacturers.objects.all()
    category_a = Category.objects.all()[:4]
    
    
    context ={
        'profile': profile,
        'profiles':profiles,
        'profile': profile,
        'manufacturers': manufacturers,
        'category_a': category_a,
    }
    return render(request,'userprofile.html', context)


def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Invalid username/password')
    
    profile=Profile.objects.get(pk=1)
    manufacturers=Manufacturers.objects.all()
    category_a = Category.objects.all()[:4]

    context={
        'profile': profile,
        'manufacturers':manufacturers,
        'category_a': category_a,
    }

    return render(request, 'login.html', context)

def logoutfunc(request):
    logout(request)
    return redirect('loginform')

def registerform(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            myuser = form.save()
            p = UserProfile(user=myuser)
            p.first_name = myuser.first_name
            p.last_name = myuser.last_name
            p.save()
            login(request,myuser)
            return redirect('loginform')
        else:
                messages.warning(request,form.errors)
                return redirect('registerform')
    
    profile=Profile.objects.get(pk=1)
    manufacturers=Manufacturers.objects.all()
    category_a = Category.objects.all()[:4]

    context={
        'profile': profile,
        'manufacturers':manufacturers,
        'category_a': category_a,
    }

    return render(request, 'register.html', context)


@login_required(login_url='/login')
def userupdate(request):
    if request.method == 'POST':
        profileform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profileform.is_valid: 
            profileform.save()
            messages.success(request, 'Your Account has been updated')
            return redirect('user')
    else:
        profileform = ProfileUpdateForm(instance=request.user.userprofile)
        profile= Profile.objects.get(pk=1)
        category= Category.objects.all()
        manufacturers= Manufacturers.objects.all()
        profiles= UserProfile.objects.filter(user_id=request.user.id).first()
        category_a = Category.objects.all()[:4]

        context = {
            'profileform': profileform,
            'profile': profile,
            'category': category,
            'profiles': profiles,
            'manufacturers': manufacturers,
            'category_a': category_a,
        }

    return render(request, 'user.html', context)








@login_required(login_url='/login')
def userpassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user')
        else:
            messages.error(request, 'please correct the error elow. <br>' + str(form.errors))
            return redirect('userpassword')
    else:
        form=PasswordChangeForm(request.user)
        profile=Profile.objects.get(pk=1)
        category= Category.objects.all()
        profiles= UserProfile.objects.filter(user__username = request.user.username).first()
        manufacturers= Manufacturers.objects.all()
        category_a = Category.objects.all()[:4]

        context ={
            'form': form,
            'profile': profile,
            'category': category,
            'profiles': profiles,
            'manufacturers': manufacturers,
            'category_a': category_a,
        }
    
    return render(request, 'userpassword.html', context)
