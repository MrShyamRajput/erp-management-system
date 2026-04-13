from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLES_CHOICES=(
        ("admin","Admin"),
        ("manager","Manager"),
        ("employee","Employee")
    )

    role=models.CharField(max_length=20,choices=ROLES_CHOICES)
    phone=models.CharField(max_length=15,blank=True)
    profile_image=models.ImageField(upload_to="progiles")

    def __str__(self):
        return self.username