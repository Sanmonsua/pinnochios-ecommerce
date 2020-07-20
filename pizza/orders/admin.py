from django.contrib import admin
from .models import Product, Category, Topping, AddOn, CartItem, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(AddOn)
admin.site.register(CartItem)
admin.site.register(Order)
