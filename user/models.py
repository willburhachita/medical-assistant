from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wallet_address = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    first_name = None
    last_name = None


    class Meta:
        db_table = "user"
        verbose_name = 'User'
        verbose_name_plural = 'Users'
 

    
    def __str__(self):
        return f"{self.wallet_address or self.email_address}"