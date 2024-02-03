from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserForm
from django.http import JsonResponse
import json
# Create your views here.


def home(request):
    products = Products.objects.filter(trending=1)
    return render(request, 'shop/index.html', {'products': products})


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "registration success,login now")
            return redirect('login')

    return render(request, 'shop/register.html', {'form': form})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in succesfully')
                return redirect('/')
            else:
                messages.error(request, "invalid user name or password")
                return redirect('/login')
        return render(request, 'shop/login.html')


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'logged out succesfully')
    return redirect('/')


def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, 'shop/collections.html', {'category': category})


def collectionsview(request, name):
    if (Category.objects.filter(name=name, status=0)):
        products = Products.objects.filter(catregory__name=name)
        return render(request, 'shop/products/index.html', {'products': products, 'category_name': name})
    else:
        messages.warning(request, "no such categories found")
        return redirect('collections')


def product_detials(request, cname, pname):
    if (Category.objects.filter(name=cname, status=0)):
        if (Products.objects.filter(name=pname, status=0)):
            product = Products.objects.filter(name=pname, status=0).first()
            return render(request, 'shop/products/product_details.html', {'product': product})
        else:
            messages.error(request, 'no such product found')
            return redirect('collections')
    else:
        messages.error(request, 'no such category found')
        return redirect('collections')


def addtocart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            # print('userid', request.user.id)
            # print('username', request.user.username)
            product_status = Products.objects.get(id=product_id)

            if product_status:
                if Cart.objects.filter(user=request.user, product_id=product_id):
                    return JsonResponse({'status': 'product already added'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(
                            user=request.user, product_id=product_id, product_qty=product_qty,)
                        return JsonResponse({'status': 'succesfully added'}, status=200)
                    else:
                        return JsonResponse({'status': 'product stoct not available added'}, status=200)

        else:
            return JsonResponse({'status': 'login to add cart'}, status=200)

    else:
        return JsonResponse({'status': 'invalid access'}, status=200)


def cartpage(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'shop/cart.html', {'cart': cart})
    else:
        return redirect('/')


def remove_cart(request, cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')


def fav(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = data['pid']
            product_status = Products.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'product already in favourite'})
                else:
                    Favourite.objects.create(
                        user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'product added to favourite'})

        else:
            return JsonResponse({'status': 'login to add favourite'}, status=200)

    else:
        return JsonResponse({'status': 'invalid access'}, status=200)


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, 'shop/fav.html', {'fav': fav})
    else:
        return redirect('/')


def remove_favourite(request, fid):
    item = Favourite.objects.get(id=fid)
    item.delete()
    return redirect('/favviewpage')
