from django.db import models


# Create your models here.
class Invoice(models.Model):
    invoice_no = models.IntegerField()
    client_name = models.CharField(max_length=200)
    date=models.CharField(max_length=20)
    total_amount = models.FloatField()


class Item(models.Model):
    desc = models.CharField(max_length=200)
    rate= models.FloatField()
    quantity = models.IntegerField()


class User(models.Model):
    user_id = models.IntegerField()
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=16)
