from django.urls import path
from .views import index, do_login, do_logout, signup, product_detail

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login', do_login),
    path('logout', do_logout),
    path('products/<int:product_id>', product_detail)
]
