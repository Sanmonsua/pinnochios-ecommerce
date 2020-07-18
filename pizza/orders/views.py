from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.core import serializers
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Product, Topping


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
    product_data = {
        "name" : p.name,
        "description" : p.description,
        "category" : p.category.name,
        "smallPrice" : format(p.smallPrice, '.2f'),
        "largePrice" : format(p.largePrice, '.2f'),
        "toppings" : [
            t.name for t in p.toppings.all()
        ]
    }
    return JsonResponse(product_data)


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
