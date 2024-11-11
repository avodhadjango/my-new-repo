from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)

class loginTable(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)
    type=models.CharField(max_length=200)

class Booking(models.Model):
    BOOKING_OPTIONS =[
        ('standard','Standard Booking'),
        ('deluxe','Deluxe Booking'),
        ('suite','Suite Booking'),
    ]

    name=models.CharField(max_length=100)
    email=models.EmailField()
    no_of_people=models.IntegerField()
    booking_type=models.CharField(max_length=20,choices=BOOKING_OPTIONS)
    resort_name=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}-{self.resort_name}'

    def get_rate(self):
        rates ={
            'standard':300,
            'deluxe':150,
            'suite':800,
        }
        return rates.get(self.booking_type,0)

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Booking)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    bookings = models.ForeignKey(Booking,on_delete=models.CASCADE)
    no_of_people = models.PositiveIntegerField(default=1)
    booking_total = models.PositiveIntegerField(default=1)
