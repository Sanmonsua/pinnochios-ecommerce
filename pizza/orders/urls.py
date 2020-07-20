from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login', do_login),
    path('logout', do_logout),
    path('products/<int:product_id>', product_detail),
    path('cart', get_cart)
]
