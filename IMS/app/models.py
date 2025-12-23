from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
    
class ProductType(models.Model):
    name= models.CharField(max_length=150)
    
    
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    type = models.ForeignKey(ProductType,on_delete=models.SET_NULL,null=True)
    stock = models.IntegerField()
    department = models.ManyToManyField('Department',blank=True)
  
    

class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    vendor = models.ForeignKey('Vendor',on_delete=models.SET_NULL,null=True)


class Vendor(models.Model):
    vendorname = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    number = models.CharField(max_length=20)
    email = models.EmailField()
   
    
 
class Sell(models.Model):
    product =models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    customer_name= models.CharField(max_length=150)
    price = models.FloatField()
   



class Department(models.Model):
    name = models.CharField(max_length=50)
  
