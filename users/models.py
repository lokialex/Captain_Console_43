from django.db import models
from django_countries.fields import CountryField
from carts.models import Order, ShippingInformation, PaymentInformation
from games.models import Game
from django.contrib.auth.models import User


from main.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=255, null=True)
    address_2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    postcode = models.IntegerField(null=True)
    country = CountryField(null=True)
    profile_image = models.CharField(max_length=999, null=True)
    payment_information_id = models.ForeignKey(PaymentInformation, on_delete=models.SET_NULL, null=True)
    shipping_information_id = models.ForeignKey(ShippingInformation, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "username: " + self.user.username


class Review(models.Model):
    profileID = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    gameID = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    recommend = models.BooleanField(default=True)
    feedback = models.CharField(max_length=999)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)


class GameReview(models.Model):
    gameID = models.ForeignKey(Game, on_delete=models.CASCADE)
    reviewID = models.ForeignKey(Review, on_delete=models.CASCADE)


class OrderHistory(models.Model):
    profileID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)


class SearchHistory(models.Model):
    search = models.TextField()
    profileID = models.ForeignKey(Profile, on_delete=models.CASCADE)
