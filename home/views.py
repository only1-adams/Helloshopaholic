from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import paginator
from django.http import HttpResponse
from .models import *
from product.models import *
from user.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def index(request):
    profile = Profile.objects.get(pk=1)
    manufacturers = Manufacturers.objects.all()
    category = Category.objects.all()[:9]
    category_a = Category.objects.all()[:4]
    new_prod= Product.objects.filter(new_prod=True)[:6]
    carousel_a=Carousel_a.objects.get(pk=1)
    carousel_b=Carousel_b.objects.get(pk=1)
    carousel_c=Carousel_c.objects.get(pk=1)
    carousel_d=Carousel_d.objects.get(pk=1)
    featured=Product.objects.filter(featured=True)[:6]
    new_prod_slide=Product.objects.filter(new_prod_slide=True)[:4]
    new_prod_slidea=Product.objects.filter(new_prod_slidea=True)[:4]
    popular=Product.objects.filter(popular=True)[:6]
    upcoming=Product.objects.filter(upcoming=True)[:10]
    bestselling=Product.objects.filter(bestselling=True)[:6]
    # profiles = UserProfile.objects.get(user__username = request.user.username) 
    

    context = {
        'profile': profile,
        # 'profiles': profiles,
        'manufacturers': manufacturers,
        'category': category,
        'category_a': category_a,
        'new_prod': new_prod,
        'carousel_a': carousel_a,
        'carousel_b': carousel_b,
        'carousel_c': carousel_c,
        'carousel_d': carousel_d,
        'featured': featured,
        'popular':popular,
        'upcoming': upcoming,
        'new_prod_slide':new_prod_slide,
        'new_prod_slidea': new_prod_slidea,
        'bestselling': bestselling,
        
    }


    
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Message has been sent! Our Customer Service Team will reach you soon")
            return redirect('/contact')

    profile = Profile.objects.get(pk=1)
    form = ContactForm
    manufacturers = Manufacturers.objects.all()
    # profiles = UserProfile.objects.get(user__username = request.user.username)

    context = {
        'profile': profile,
        'form': form,
        'manufacturers': manufacturers,
        # 'profiles': profiles,
    }


    return render(request,'contact.html', context)


def category(request):
    profile=Profile.objects.get(pk=1)
    # profiles = UserProfile.objects.get(user__username = request.user.username) 
    manufacturers= Manufacturers.objects.all()
    category = Category.objects.order_by('-created_at').filter(status=True)
    category_a = Category.objects.all()[:4]
    paginator = Paginator(category, 8)
    page = request.GET.get('page')
    paged_category = paginator.get_page(page)

    context = {
        'profile': profile,
        # 'profiles': profiles,
        'manufacturers': manufacturers,
        'category': paged_category,
        'category_a': category_a,
    }


    return render(request, 'category.html', context)


def prod_list(request,id,slug):
    profile=Profile.objects.get(pk=1)
    category=Category.objects.all()
    category_a = Category.objects.all()[:4]
    product=Product.objects.filter(category_id=id)
    # products=Product.objects.get(pk=id)
    manufacturers=Manufacturers.objects.all()
    # profiles = UserProfile.objects.get(user__username = request.user.username) 

    context = {
        'profile': profile,
        # 'profiles': profiles,
        'category': category,
        'product': product,
        # 'products': products,
        'manufacturers': manufacturers,
        'category_a': category_a,
    }

    return render(request, 'prod-list.html', context)

def prod_detail(request,id,slug):
    profile=Profile.objects.get(pk=1)
    category=Category.objects.all()
    category_a = Category.objects.all()[:4]
    product=Product.objects.filter(category_id=id)
    products=Product.objects.get(pk=id)
    manufacturers=Manufacturers.objects.all()
    images = Images.objects.filter(product_id=id)
    # profiles = UserProfile.objects.get(user__username = request.user.username) 

    context = {
        'profile': profile,
        # 'profiles': profiles,
        'category': category,
        'product': product,
        'products': products,
        'manufacturers': manufacturers,
        'category_a': category_a,
        'images': images,
    }
    return render(request, 'prod-details.html', context)
