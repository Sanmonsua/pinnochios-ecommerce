from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from .models import Category, Product, Topping


def index(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        context = {
            "categories" : categories
        }
        return render(request, 'orders/index.html', context=context)

    return redirect('/login')


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
