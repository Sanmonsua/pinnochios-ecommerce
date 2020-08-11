import stripe
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Category, Product, Topping, CartItem, AddOn, Order

stripe.api_key = "sk_test_51HE29lKcPIFcZJbWSiQEYLRm0nKCaZ8UOe5t3quNstheHtAetWh6BvqRiWPXDYw93mHMbwG2hNtioopiVsd3ulCv00D0AMeu2g "


def index(request):
    """
    Renders the main of the app
    :param request
    :return: If user is authenticated render index.html
        if not redirect to login
    """
    if request.user.is_authenticated:
        categories_objects = Category.objects.all()
        categories = []
        for category in categories_objects:
            c = {'name': category, 'products': [
                p for p in category.options.all()
            ]}
            categories.append(c)
        context = {
            "categories": categories,
            "username": request.user.username
        }
        return render(request, 'orders/index.html', context=context)

    return redirect('/login')


def product_detail(request, product_id):
    """
    Get data from the product id specified
    :param request
    :param product_id
    :return: Json Response
    """
    try:
        p = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    toppings = []
    for topping in p.toppings.all():
        t = {'name': topping.name, 'id': topping.id}
        toppings.append(t)
    addons = []
    for addon in p.addons.all():
        a = {'name': addon.name, 'id': addon.id, 'price': addon.price}
        addons.append(a)
    product_data = {
        "id": p.id,
        "image_url": p.image.url,
        "name": p.name,
        "description": p.description,
        "category": p.category.name,
        "smallPrice": format(p.small_price, '.2f'),
        "largePrice": format(p.large_price, '.2f'),
        "toppings": toppings,
        "max_toppings": p.max_toppings,
        "addons": addons
    }
    return JsonResponse(product_data)


def get_cart(request):
    """
    Get the cart data from the user logged in
    :param request
    :return: Json response
    """
    cart = request.user.cart.all()
    cart_data = {
        "cart": [
            {
                "product": {
                    "name": str(item.product),
                    "img": item.product.image.url
                },
                "toppings": [{
                    "name": str(t)
                } for t in item.toppings.all()],
                "addons": [{
                    "name": a.name,
                    "price": a.price
                } for a in item.add_ons.all()],
                "quantity": item.quantity,
                "price": item.price
            }
            for item in cart
        ]
    }
    return JsonResponse(cart_data)


def add_to_cart(request):
    """
    Add product to cart
    :param request
    :return: Json response to confirm that
        the items were added to the cart
    """
    if request.method == 'POST':
        data = request.POST.copy()
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        toppings = data.get('toppings').split(',')
        addons = data.get('addons').split(',')
        price = data.get('price')
        try:
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

            return JsonResponse({'success': True})
        except Product.DoesNotExist:
            return JsonResponse({"success": False})


def clear_cart(request):
    """
    Clear the user cart
    :param request
    :return: Redirect to index
    """
    cart = request.user.cart.all()
    cart.delete()
    return redirect('/')


def do_login(request):
    """
    This view logs in the user
    :param request
    :return: Login view
    """
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
        "form": form
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
        "form": form
    }
    return render(request, 'orders/signup.html', context=context)


def do_logout(request):
    """
    Logs the user out
    :param request
    :return: Redirect to index
    """
    logout(request)
    return redirect('/')


def calculate_order_amount(cart):
    """
    Calculates the order total amount
    :param cart
    :return: Total
    """
    total = 0
    for item in cart:
        total += item.price
    return total


def checkout(request):
    """
    Checkout view that controls and verifies the payments
    :param request
    :return: If is a get request returns checkout view,
            if is a post request validates that the payment was done to redirect to
            orders page.
    """
    cart = request.user.cart.all()
    total = calculate_order_amount(cart)

    if request.method == 'GET':
        return render(request, 'orders/checkout.html', context={
            "cart": cart,
            "total": total
        })
    else:
        payment_intent_id = request.POST.get('paymentIntentId')
        if payment_intent_id is not None:
            order = Order(total_price=total, costumer=request.user)
            order.save()
            cart = request.user.cart.all()
            cart.delete()
            return redirect('/your-orders')


def charge(request):
    """
    Creates a stripe charge
    :param request
    :return: Json response
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(calculate_order_amount(request.user.cart.all()) * 100),
            currency='usd'
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})


def get_orders(request):
    """
    Get the orders for a user
    :param request
    :return: Render the orders template
    """
    context = {
        "orders": request.user.orders.all(),
        "username": request.user.username
    }
    return render(request, 'orders/orders.html', context=context)
