from django.shortcuts import render,redirect

from django.http import HttpResponse

from django.contrib import messages
from home.models import *
from product.models import *
from .models import *
from user.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
import json
import random
import string
import uuid
from django.views.decorators.http import require_POST

# Create your views here.


def order(request):
    return HttpResponse('e good')

@require_POST
@login_required(login_url='/login')
def addtoshopcart(request):
    url = request.META.get('HTTP_REFERER')
    thequantity = int(request.POST['quantity'])
    thecolor = request.POST.get('color', None)
    theprodid = request.POST['prodid']
    aprod = Product.objects.get(pk=theprodid)

    cart= ShopCart.objects.filter(order_placed=False).filter(user__username=request.user.username)

    if cart: #an existing cart is noticed 
        prodchecker = ShopCart.objects.filter(product_id = aprod.id, color=thecolor, quantity=thequantity,user__username=request.user.username).first()

        if prodchecker: #product exists in the cart increment it
            prodchecker.quantity += thequantity
            prodchecker.color = thecolor
            prodchecker.save()
            messages.success(request, "Product added to Shopcart")
            return redirect(url)

        else: #product is not in cart add it
            anitem = ShopCart()
            anitem.product=aprod
            anitem.user=request.user
            anitem.order_code=cart[0].order_code
            anitem.quantity=thequantity
            anitem.color=thecolor
            anitem.order_placed=False
            anitem.save()
    
    else: #create a new cart,  generate order code
         ordercode = str(uuid.uuid4())
         newcart = ShopCart()
         newcart.product =aprod
         newcart.user =request.user
         newcart.order_code=ordercode
         newcart.quantity=thequantity
         newcart.color=thecolor 
         newcart.order_placed-False
         newcart.save()
    
    messages.success(request, "Product added to Shopcart")

    return redirect(url)



@login_required(login_url='/login')
def shopcart(request):

    profile= Profile.objects.get(pk=1)
    category = Category.objects.all()
    category_a = Category.objects.all()[:4]
    shopcart = ShopCart.objects.filter(order_placed=False).filter(user__username=request.user.username)
    profiles = UserProfile.objects.get(user__username = request.user.username)
    manufacturers = Manufacturers.objects.all()
    

    


    Subtotal=0
    Shippingfee=0
    vat=0
    total=0

    for item in shopcart:
        if item.product.discount_price:
            Subtotal += item.product.discount_price * item.quantity
        else:
            Subtotal += item.product_price *  item.quantity

    # Shipping rules: 8% fees to all orders above 450.0 fees to orders lower
    if Subtotal > 450:
        Shippingfee = 0.08 * Subtotal
    else:
        Shippingfee=0

    vat = 0.085 * Subtotal

    total = Subtotal + Shippingfee + vat

    context ={
        'profile': profile,
        'manufacturers': manufacturers,
        'profiles': profiles,
        'category': category,
        'category_a': category_a,
        'shopcart': shopcart,
        'Shipping': Shippingfee,
        'Subtotal': Subtotal,
        'vat': vat,
        'total': total,
        
    }
    
    return render(request,'shopcart.html', context)

@require_POST
@login_required(login_url='/login')
def updatequantity(request):
    url = request.META.get('HTTP_REFERER')
    newquantity = request.POST['itemquan']
    theitem = ShopCart.objects.get(id=request.POST ['itemid'])
    theitem.quantity = newquantity
    theitem.save()

    messages.success(request, "Product Quantity successfully updated")
    return redirect(url)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Item deleted from Shopcart.")
    return redirect('order:shopcart')



@login_required(login_url='/login')
def checkout(request):
    category = Category.objects.all()
    category_a = Category.objects.all()[:4]
    profile = Profile.objects.get(pk=1)
    shopcart = ShopCart.objects.filter(user__username = request.user.username).filter(order_placed=False)
    profiles = UserProfile.objects.get(user__username = request.user.username)
    manufacturers= Manufacturers.objects.all()

    Subtotal = 0
    Shippingfee = 0
    vat =0
    total = 0

    for item in shopcart:
        if item.product.discount_price:
            Subtotal += item.product.discount_price * item.quantity
        else:
            Subtotal += item.product.price * item.quantity

    # Shipping rules: 8% fees to all ordesa above 150.0. 0 fees nto orders lower
    if Subtotal > 150:
        Shippingfee = 0.08 * Subtotal
    else:
        Shippingfee = 0

    # vat is at 7.50% of the total purchase to be made
    vat = 0.075 * Subtotal

    total = Subtotal + Shippingfee + vat

    context = {
        'profile': profile,
        'manufacturers': manufacturers,
        'shopcart': shopcart,
        'order_code': shopcart[0].order_code,
        'profiles': profiles,
        'category': category,
        'category_a': category_a,
        'Subtotal': Subtotal,
        'Shipping': Shippingfee,
        'vat': vat,
        'total': total,
        
    }
    return render(request, 'checkout.html', context)



@require_POST
@login_required(login_url='/login')
def placeorder(request):
    api_key = 'sk_test_301780e41d9eca28ddbdeae67de0ea92ca974883'
    url = 'https://api.paystack.co/transaction/initialize'
    callback_url = 'http://3.17.204.0/order/ordercompleted/'
    ordercode = request.POST['order_number']
    autogen_ref = ''.join(random.choices(string.digits + string.ascii_letters, k=8))
    current_user = User.objects.get(username = request.user.username)
    user = UserProfile.objects.get(user_id = current_user.id)
    total = float(request.POST['amount']) * 100

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference': autogen_ref, 'amount': int(total), "currency": "NGN", 'order_number':ordercode, 'email':user.email, 'callback_url':callback_url}

    #making a request to PAYSTACK
    try:
        r=requests.post(url, headers=headers, json=data)
    except Exception:
        messages.error(request, "Network busy. Please try again in few minutes. Thank You")
    else:
        #create an order
        transback = json.loads(r.text)

        rd_url = transback['data']['authorization_url']
        theuser = UserProfile.objects.filter(user=request.user).first()
        order = Order()
        order.first_name=theuser.user.first_name
        order.last_name=theuser.user.last_name
        order.phone=theuser.phone
        order.city=theuser.city
        order.order_code=ordercode
        order.payment_code= autogen_ref
        order.total=total
        order.order_placed= True
        order.save()
        return redirect(rd_url)
    return redirect('order:checkout')



@login_required(login_url='/login')
def ordercompleted(request):
    category = Category.objects.all()
    profile = Profile.objects.get(pk=1)
    manufacturers= Manufacturers.objects.all()
    profiles = UserProfile.objects.get(user__username = request.user.username)
    shopcart = ShopCart.objects.filter(order_placed=False).filter(user__username =request.user.username)

    #cleaning thr shopcart
    for item in shopcart:
        item.order_placed = True
        item.save()

        #reducing quantity in stock
        aproduct= Product.objects.get(id=item.product.id)
        aproduct.quantity_instock -= item.quantity
        aproduct.save()

    context ={
        'profile': profile,
        'category': category,
        'manufacturers': manufacturers,
        'shopcart': shopcart,
        'profiles': profiles,
    }      

    return render(request, 'ordercompleted.html', context)