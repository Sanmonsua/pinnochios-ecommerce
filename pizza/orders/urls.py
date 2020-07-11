from django.urls import path
from .views import index, do_login, do_logout, signup

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login', do_login),
    path('logout', do_logout)
]
