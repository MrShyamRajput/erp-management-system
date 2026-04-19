from django.db import models
from django.core.validators import MinValueValidator

#Customer Details
class Customer(models.Model):
    full_name=models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name
    
#Product Details (Selection Field)

class Product(models.Model):
    name= models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
#Order 

class Order(models.Model):
    STATUS_CHOICES= [
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),


    ]
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
# Orfer Items 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(slef):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"
    