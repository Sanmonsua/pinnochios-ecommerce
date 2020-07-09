from django.contrib import admin
from .models import Dish, Category, Topping

# Register your models here.
admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Topping)
