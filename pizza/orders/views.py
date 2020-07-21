from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.core import serializers
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Product, Topping, CartItem


def index(request):
    if request.user.is_authenticated:
        categories_objects = Category.objects.all()
        categories = []
        for category in categories_objects:
            c = {}
            c['name'] = category
            c['products'] = []
            for p in category.options.all():
                c['products'].append(p)
            categories.append(c)
        context = {
            "categories" : categories,
            "username" : request.user.username
        }
        return render(request, 'orders/index.html', context=context)

    return redirect('/login')


def product_detail(request, product_id):
    try:
        p = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    toppings = []
    for topping in p.toppings.all():
        t = {}
        t['name'] = topping.name
        t['id'] = topping.id
        toppings.append(t)
    addons = []
    for addon in p.addons.all():
        a = {}
        a['name'] = addon.name
        a['id'] = addon.id
        a['price'] = addon.price
        addons.append(a)
    product_data = {
        "name" : p.name,
        "description" : p.description,
        "category" : p.category.name,
        "smallPrice" : format(p.small_price, '.2f'),
        "largePrice" : format(p.large_price, '.2f'),
        "toppings" : toppings,
        "max_toppings" : p.max_toppings,
        "addons" : addons
    }
    return JsonResponse(product_data)


def get_cart(request):
    cart = request.user.cart.all()
    cart_data = {
        "cart" : [
            {
                "product" : {
                    "name" : str(item.product),
                    "img" : item.product.image.url
                },
                "quantity" : item.quantity,
                "price" : item.price
            }
            for item in cart
        ]
    }
    return JsonResponse(cart_data)


def do_login(request):
    #This view logs in the user
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')

    context = {
        "form":form
    }

    return render(request, 'orders/login.html', context=context)


def signup(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect('/')

    context = {
        "form":form
    }
    return render(request, 'orders/signup.html', context=context)


def do_logout(request):
    logout(request)
    return redirect('/')
