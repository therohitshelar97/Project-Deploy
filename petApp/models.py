from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class Animals(models.Model):
    pname = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=300, null=True)
    breed = models.CharField(max_length=200,null=True)
    desc =models.CharField(max_length=500,null=True)
    price = models.FloatField(null=True)
    image = models.ImageField(upload_to='media',null=True)

    # def __str__(self):
    #     return  self.category

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    animals = models.ForeignKey(Animals, on_delete=models.CASCADE, null=True)

class Address(models.Model):
    cname = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    animals = models.ForeignKey(Animals,on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=100,null=True)
    pincode = models.IntegerField(null=True)
    detail = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=100, null=True)
    phone = models.BigIntegerField(null=True)
    alternate_phone = models.BigIntegerField(null=True)
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    animals = models.ForeignKey(Animals,on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True)
    order_id = models.CharField(max_length=100,null=True)
    payment = models.FloatField(null=True)
    delivery_date = models.CharField(max_length=100,null=True)

# class Amount(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
#     order = models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
#     amount = models.IntegerField(null=True)

class Order_History(models.Model):
    user = models.IntegerField()
    pname = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=300, null=True)
    breed = models.CharField(max_length=200,null=True)
    desc =models.CharField(max_length=500,null=True)
    price = models.FloatField(null=True)
    image = models.ImageField(upload_to='media',null=True)
    cname = models.CharField(max_length=100,null=True)
    user = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    pincode = models.IntegerField(null=True)
    detail = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=100, null=True)
    phone = models.BigIntegerField(null=True)
    alternate_phone = models.BigIntegerField(null=True)
    order_id = models.CharField(max_length=100,null=True)

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    animals = models.ForeignKey(Animals,on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000, null=True)