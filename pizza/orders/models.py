from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    smallPrice = models.FloatField()
    largePrice = models.FloatField()
    category = models.ForeignKey(Category, related_name='options', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.name} - {self.category}"


class Topping(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(Product, blank=True, related_name='toppings')

    def __str__(self):
        return f"{self.name}"
