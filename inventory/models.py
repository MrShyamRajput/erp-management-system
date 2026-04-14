from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.


# Table to group products
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return
    
#For Brand Filtering in UI

class Brand(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="brands",blank=True,null=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#Main product Table
class Product(models.Model):
    name=models.CharField(max_length=200)
    sku=models.CharField(max_length=100)

    category=models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    price=models.DecimalField(max_digits=10,decimal_places=2)
    decription=models.TextField(blank=True)

    image=models.ImageField(upload_to="products/",null=True,blank=True)

    def __str__(self):
        return self.name
    
