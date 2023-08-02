from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manageUser import UserManager

# Create your models here.
class Invoice(models.Model):
    invoice_no = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=200)
    date=models.CharField(max_length=20)
    total_amount = models.FloatField()
    item=models.ManyToManyField("Item", related_name="invoices")
    class Meta:
        indexes=[
            models.Index(fields=["client_name"],name="client-index")
        ]


class Item(models.Model):
    item_id=models.AutoField(primary_key=True,unique=True)
    desc = models.CharField(max_length=200)
    rate= models.FloatField()
    quantity = models.IntegerField()


class User(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=50)
    username=models.CharField(max_length=100,unique=True)

    USERNAME_FIELD = 'username'
    objects=UserManager()
