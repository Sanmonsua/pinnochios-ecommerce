from django.contrib import admin
from .models import Product, Category, Topping, AddOn, CartItem, Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total_price',]

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(AddOn)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
