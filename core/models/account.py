from core.models import User
from django.db import models

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='account')
    balance = models.DecimalField(decimal_places=2, max_digits=12,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.balance}"