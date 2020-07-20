from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=128)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    small_price = models.FloatField()
    large_price = models.FloatField()
    category = models.ForeignKey(Category, related_name='options', on_delete=models.CASCADE, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='products/')
    max_toppings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.category}"


class Topping(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(Product, blank=True, related_name='toppings')

    def __str__(self):
        return f"{self.name}"


class AddOn(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(Product, blank=True, related_name='addons')
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.price}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField()
    toppings = models.ManyToManyField(Topping, blank=True)
    add_ons = models.ManyToManyField(AddOn, blank=True)
    price = models.FloatField()
    costumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", blank=True, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class Order(models.Model):
    items = models.ManyToManyField(CartItem, related_name="orders")
    total_price = models.IntegerField(default=0)
    costumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", blank=True, default=0)

    def __str__(self):
        return f"{self.id}"
