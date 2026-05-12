# finance/models.py

from django.db import models


class Invoice(models.Model):

    STATUS_CHOICES = [

        ('paid', 'Paid'),

        ('pending', 'Pending'),

        ('overdue', 'Overdue'),

    ]

    client_name = models.CharField(max_length=200)

    invoice_number = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.invoice_number