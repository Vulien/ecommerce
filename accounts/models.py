from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"  # Sử dụng email thay vì username
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
