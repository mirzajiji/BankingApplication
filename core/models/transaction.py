from django.db import models
from core.models import User


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('admin_credit', 'Admin Credit'),
        ('user_transfer', 'User Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    sender = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_transactions'
    )
    receiver = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type=models.CharField(max_length=20, choices=TYPE_CHOICES, default='user_transfer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} → {self.receiver.email if self.receiver else 'N/A'} | {self.type} | {self.amount}"
