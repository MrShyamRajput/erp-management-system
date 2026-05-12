from django.db import models

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    product = models.CharField(max_length=200)

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name