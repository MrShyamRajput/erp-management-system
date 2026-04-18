from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.


# Table to group products
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#For Brand Filtering in UI

class Brand(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="brands/",blank=True,null=True)

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

    brand=models.ForeignKey(Brand,
        on_delete=models.CASCADE
        )

    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
     )
    decription=models.TextField(blank=True)

    image=models.ImageField(upload_to="products/",null=True,blank=True)

    def __str__(self):
        return self.name
    

#Warehourse Table for Cspacity Chart

class Warehouse(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    capacity=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#Inventory table to keep track of remaining stocks
class InventoryStocks(models.Model):
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


    warehouse=models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    quantity=models.IntegerField(default=0)
    updated_at=models.DateTimeField(auto_now=True)

class StockTransaction(models.Model):

    TRANSACTION_TYPES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("TRANSFER", "Transfer"),
        ("ADJUSTMENT", "Adjustment"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)