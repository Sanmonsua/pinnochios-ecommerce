from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.core import serializers
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Category, Product, Topping, CartItem, AddOn, Order
import stripe

stripe.api_key = "sk_test_51HE29lKcPIFcZJbWSiQEYLRm0nKCaZ8UOe5t3quNstheHtAetWh6BvqRiWPXDYw93mHMbwG2hNtioopiVsd3ulCv00D0AMeu2g"

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
        "id" : p.id,
        "image_url" : p.image.url,
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
                "toppings" : [{
                    "name": str(t)
                } for t in item.toppings.all()],
                "addons" : [{
                    "name":a.name,
                    "price":a.price
                } for a in item.add_ons.all()],
                "quantity" : item.quantity,
                "price" : item.price
            }
            for item in cart
        ]
    }
    return JsonResponse(cart_data)


def addToCart(request):
    if request.method == 'POST':
        data = request.POST.copy()
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        toppings = data.get('toppings').split(',')
        addons = data.get('addons').split(',')
        price = data.get('price')
        product = Product.objects.get(pk=product_id)
        cart_item = CartItem(product=product, costumer=request.user, quantity=quantity, price=price)
        cart_item.save()
        for t in toppings:
            if t != '':
                topping = Topping.objects.get(pk=t)
                cart_item.toppings.add(topping)

        for a in addons:
            if a != '':
                addon = AddOn.objects.get(pk=a)
                cart_item.add_ons.add(addon)

        return JsonResponse({'success':True})


def clear_cart(request):
    cart = request.user.cart.all()
    cart.delete()
    return redirect('/')


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


def calculate_order_amount(cart):
    total = 0
    for item in cart:
        total += item.price
    return total


def checkout(request):

    cart = request.user.cart.all()
    total = calculate_order_amount(cart)

    if request.method == 'GET':
        return render(request, 'orders/checkout.html', context={
            "cart":cart,
            "total":total
        })
    else:
        paymentIntentId = request.POST.get('paymentIntentId')
        if paymentIntentId != None:
            order = Order(total_price=total, costumer=request.user)
            order.save()
            cart = request.user.cart.all()
            cart.delete()
            return redirect('/your-orders')



def charge(request):
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(calculate_order_amount(request.user.cart.all())*100),
            currency='usd'
        )
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({'error':str(e)})


def get_orders(request):
    context = {
        "orders" : request.user.orders.all(),
        "username" : request.user.username
    }
    return render(request, 'orders/orders.html', context=context)
