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
    smallPrice = models.FloatField()
    largePrice = models.FloatField()
    category = models.ForeignKey(Category, related_name='options', on_delete=models.CASCADE, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='products/')
    def __str__(self):
        return f"{self.name} - {self.category}"


class Topping(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(Product, blank=True, related_name='toppings')

    def __str__(self):
        return f"{self.name}"


class AddOn(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(Product, blank=True, related_name='toppings')
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.price}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField()

    LARGE = 'Large'
    SMALL = 'Small'

    SIZE_CHOICES = (
        (LARGE, 'L'),
        (SMALL, 'S')
    )
    size = models.CharField(max_length=64, choices=SIZE_CHOICES, default=SMALL)

    toppings = models.ManyToManyField(Topping, blank=True)
    add_ons = models.ManyToManyField(AddOn, blank=True)

    def calculateTotalPrice(self):
        if self.size==LARGE:
