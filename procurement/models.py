from django.db import models


class Supplier(models.Model):

    SEGMENT_CHOICES = [
        ('hardware', 'Hardware'),
        ('logistics', 'Logistics'),
        ('software', 'Software'),
        ('raw_material', 'Raw Material'),
    ]

    PERFORMANCE_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
    ]

    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    segment = models.CharField(
        max_length=50,
        choices=SEGMENT_CHOICES
    )

    performance = models.CharField(
        max_length=20,
        choices=PERFORMANCE_CHOICES,
        default='good'
    )

    score = models.IntegerField(default=80)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_transit', 'In Transit'),
        ('delayed', 'Delayed'),
        ('delivered', 'Delivered'),
    ]

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(max_length=200)

    quantity = models.IntegerField()

    estimated_delivery = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO-{self.id}"