from django.shortcuts import render
from .models import Category, Product, Topping


def index(request):
    categories = Category.objects.all()
    context = {
        "categories" : categories
    }
    return render(request, 'orders/index.html', context=context)
