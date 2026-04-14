from django.db import models
from cgi import maxlen

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return