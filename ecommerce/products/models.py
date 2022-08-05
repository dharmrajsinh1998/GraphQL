from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class UserOTP(models.Model):
#     """
#     storing user otp in database.
#     after three invalid otp attempt will be expired your otp
#     """
#
#     user = models.ForeignKey(User, related_name="user_otp", on_delete=models.CASCADE)
#     otp = models.IntegerField(blank=True, null=True)
#     invalid_attempt = models.IntegerField(default=0)
#     is_expired = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.user.username)


class Category(models.Model):
    name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return str(self.name)


class Brand(models.Model):
    name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=225)
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE
    )
    brand = models.ForeignKey(Brand, related_name="brand", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return str(self.name)


class Order(models.Model):

    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name="items")
    placed = models.BooleanField(default=False)
    total_price = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2
    )
    total_qty = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
