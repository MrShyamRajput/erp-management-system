from django.db import models


class ReportLog(models.Model):

    REPORT_TYPES = [
        ('finance', 'Finance'),
        ('sales', 'Sales'),
        ('procurement', 'Procurement'),
        ('inventory', 'Inventory'),
    ]

    title = models.CharField(max_length=200)

    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title